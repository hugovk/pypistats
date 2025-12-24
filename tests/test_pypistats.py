"""
Unit tests for pypistats
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from unittest import mock

import pytest
from termcolor import termcolor

import pypistats
from pypistats import _cache

from .data.expected_tabulated import (
    EXPECTED_TABULATED_HTML,
    EXPECTED_TABULATED_MD,
    EXPECTED_TABULATED_PRETTY,
    EXPECTED_TABULATED_RST,
    EXPECTED_TABULATED_TSV,
)
from .data.python_minor import DATA as PYTHON_MINOR_DATA

SAMPLE_DATA = [
    {"category": "2.6", "date": "2018-08-15", "downloads": 51},
    {"category": "2.7", "date": "2018-08-15", "downloads": 63749},
    {"category": "3.2", "date": "2018-08-15", "downloads": 2},
    {"category": "3.3", "date": "2018-08-15", "downloads": 40},
    {"category": "3.4", "date": "2018-08-15", "downloads": 6095},
    {"category": "3.5", "date": "2018-08-15", "downloads": 20358},
    {"category": "3.6", "date": "2018-08-15", "downloads": 35274},
    {"category": "3.7", "date": "2018-08-15", "downloads": 6595},
    {"category": "3.8", "date": "2018-08-15", "downloads": 3},
    {"category": "null", "date": "2018-08-15", "downloads": 1019},
]
SAMPLE_DATA_ONE_ROW = [{"category": "with_mirrors", "downloads": 11_497_042}]
SAMPLE_DATA_RECENT = {
    "last_day": 123_002,
    "last_month": 3_254_221,
    "last_week": 761_649,
}
SAMPLE_DATA_VERSION_STRINGS = [
    {"category": "3.1", "date": "2018-08-15", "downloads": 10},
    {"category": "3.10", "date": "2018-08-15", "downloads": 1},
]
SAMPLE_RESPONSE_OVERALL = """{
          "data": [
            {"category": "with_mirrors", "date": "2020-05-01", "downloads": 2100139},
            {"category": "with_mirrors", "date": "2020-05-02", "downloads": 1487218},
            {"category": "without_mirrors", "date": "2020-05-01", "downloads": 2083472},
            {"category": "without_mirrors", "date": "2020-05-02", "downloads": 1475979}
          ],
          "package": "pip",
          "type": "overall_downloads"
        }"""


def stub__cache_filename(*args) -> Path:
    return Path("/this/does/not/exist")


def stub__save_cache(*args) -> None:
    pass


def mock_urllib3_response(content: str, status: int = 200) -> mock.Mock:
    """Helper to create a mock urllib3 response."""
    response = mock.Mock()
    response.status = status
    response.data = content.encode()
    return response


def assert_called_with_url(mock_request: mock.Mock, url: str) -> None:
    """Assert that urllib3.request was called once with the given URL."""
    mock_request.assert_called_once_with("GET", url, headers=mock.ANY)


class TestPypiStats:
    def setup_method(self) -> None:
        # Stub caching. Caches are tested in another class.
        self.original__cache_filename = _cache.filename
        self.original__save_cache = _cache.save
        _cache.filename = stub__cache_filename  # type: ignore[assignment]
        _cache.save = stub__save_cache  # type: ignore[assignment]

    def teardown_method(self) -> None:
        # Unstub caching
        _cache.filename = self.original__cache_filename
        _cache.save = self.original__save_cache
        termcolor.can_colorize.cache_clear()

    def test__filter_no_filters_no_change(self) -> None:
        # Arrange
        data = copy.deepcopy(PYTHON_MINOR_DATA)

        # Act
        output = pypistats._filter(data)

        # Assert
        assert data == output

    def test__filter_start_date(self) -> None:
        # Arrange
        data = copy.deepcopy(PYTHON_MINOR_DATA)
        start_date = "2018-09-22"

        # Act
        output = pypistats._filter(data, start_date=start_date)

        # Assert
        assert len(output) == 20
        for row in output:
            assert row["date"] >= start_date

    def test__filter_end_date(self) -> None:
        # Arrange
        data = copy.deepcopy(PYTHON_MINOR_DATA)
        end_date = "2018-04-22"

        # Act
        output = pypistats._filter(data, end_date=end_date)

        # Assert
        assert len(output) == 62
        for row in output:
            assert row["date"] <= end_date

    def test__filter_start_and_end_date(self) -> None:
        # Arrange
        data = copy.deepcopy(PYTHON_MINOR_DATA)
        start_date = "2018-09-01"
        end_date = "2018-09-11"

        # Act
        output = pypistats._filter(data, start_date=start_date, end_date=end_date)

        # Assert
        assert len(output) == 112
        for row in output:
            assert row["date"] >= start_date
            assert row["date"] <= end_date

    @mock.patch("urllib3.request")
    def test_warn_if_start_date_before_earliest_available(self, mock_request) -> None:
        # Arrange
        start_date = "2000-01-01"
        package = "pip"
        mocked_response = """{
            "data": [
                {"category": "2", "date": "2018-11-01", "downloads": 2008344},
                {"category": "3", "date": "2018-11-01", "downloads": 280299},
                {"category": "null", "date": "2018-11-01", "downloads": 7122}
            ],
            "package": "pip",
            "type": "python_major_downloads"
        }"""

        mock_request.return_value = mock_urllib3_response(mocked_response)
        # Act / Assert
        with pytest.warns(
            UserWarning,
            match=r"Requested start date \(2000-01-01\) is before earliest available "
            r"data \(2018-11-01\), because data is only available for 180 days. "
            "See https://pypistats.org/about#data",
        ):
            pypistats.python_major(package, start_date=start_date)
        assert_called_with_url(
            mock_request, "https://pypistats.org/api/packages/pip/python_major"
        )

    @mock.patch("urllib3.request")
    def test_error_if_end_date_before_earliest_available(self, mock_request) -> None:
        # Arrange
        end_date = "2000-01-01"
        package = "pip"
        mocked_response = """{
            "data": [
                {"category": "2", "date": "2018-11-01", "downloads": 2008344},
                {"category": "3", "date": "2018-11-01", "downloads": 280299},
                {"category": "null", "date": "2018-11-01", "downloads": 7122}
            ],
            "package": "pip",
            "type": "python_major_downloads"
        }"""

        mock_request.return_value = mock_urllib3_response(mocked_response)
        # Act / Assert
        with pytest.raises(
            ValueError,
            match=r"Requested end date \(2000-01-01\) is before earliest available "
            r"data \(2018-11-01\), because data is only available for 180 days. "
            "See https://pypistats.org/about#data",
        ):
            pypistats.python_major(package, end_date=end_date)
        assert_called_with_url(
            mock_request, "https://pypistats.org/api/packages/pip/python_major"
        )

    @pytest.mark.parametrize(
        "test_name, test_value, expected",
        [
            ("period", None, ""),
            ("period", "day", "&period=day"),
            ("mirrors", True, "&mirrors=true"),
            ("version", 3, "&version=3"),
            ("version", 3.7, "&version=3.7"),
        ],
    )
    def test__paramify(self, test_name, test_value, expected) -> None:
        # Act
        param = pypistats._paramify(test_name, test_value)

        # Assert
        assert param == expected

    def test__colourify(self, monkeypatch) -> None:
        # Arrange
        data = [
            {"category": "2.7", "downloads": 1},
            {"category": "3.5", "downloads": 10},
            {"category": "3.10", "downloads": 89},
        ]
        expected_output = [
            # red
            {"category": "2.7", "downloads": 1, "percent": "\x1b[31m1.00%\x1b[0m"},
            # yellow
            {"category": "3.5", "downloads": 10, "percent": "\x1b[33m10.00%\x1b[0m"},
            # green
            {"category": "3.10", "downloads": 89, "percent": "\x1b[32m89.00%\x1b[0m"},
            {"category": "Total", "downloads": 100},
        ]
        percent_data = pypistats._percent(data)
        total_data = pypistats._grand_total(percent_data)
        monkeypatch.setenv("FORCE_COLOR", "1")

        # Act
        output = pypistats._colourify(total_data)

        # Assert
        assert output == expected_output

    def test__tabulate_noarg(self) -> None:
        # Arrange
        data = copy.deepcopy(SAMPLE_DATA)
        expected_output = EXPECTED_TABULATED_MD

        # Act
        output = pypistats._tabulate(data)

        # Assert
        assert output.strip() == expected_output.strip()

    @pytest.mark.parametrize(
        "test_input, expected",
        [
            pytest.param("html", EXPECTED_TABULATED_HTML, id="html"),
            pytest.param("markdown", EXPECTED_TABULATED_MD, id="markdown"),
            pytest.param("pretty", EXPECTED_TABULATED_PRETTY, id="pretty"),
            pytest.param("rst", EXPECTED_TABULATED_RST, id="rst"),
            pytest.param("tsv", EXPECTED_TABULATED_TSV, id="tsv"),
        ],
    )
    def test__tabulate(self, test_input: str, expected: str, monkeypatch) -> None:
        # Arrange
        data = copy.deepcopy(SAMPLE_DATA)
        monkeypatch.setenv("NO_COLOR", "1")

        # Act
        output = pypistats._tabulate(data, format_=test_input)

        # Assert
        assert output.strip() == expected.strip()

    def test__sort(self) -> None:
        # Arrange
        data = copy.deepcopy(SAMPLE_DATA)
        expected_output = [
            {"category": "2.7", "date": "2018-08-15", "downloads": 63749},
            {"category": "3.6", "date": "2018-08-15", "downloads": 35274},
            {"category": "3.5", "date": "2018-08-15", "downloads": 20358},
            {"category": "3.7", "date": "2018-08-15", "downloads": 6595},
            {"category": "3.4", "date": "2018-08-15", "downloads": 6095},
            {"category": "null", "date": "2018-08-15", "downloads": 1019},
            {"category": "2.6", "date": "2018-08-15", "downloads": 51},
            {"category": "3.3", "date": "2018-08-15", "downloads": 40},
            {"category": "3.8", "date": "2018-08-15", "downloads": 3},
            {"category": "3.2", "date": "2018-08-15", "downloads": 2},
        ]

        # Act
        output = pypistats._sort(data)

        # Assert
        assert output == expected_output

    def test__sort_recent(self) -> None:
        # Arrange
        data = copy.deepcopy(SAMPLE_DATA_RECENT)

        # Act
        output = pypistats._sort(data)

        # Assert
        assert output == SAMPLE_DATA_RECENT

    def test__monthly_total(self) -> None:
        # Arrange
        data = copy.deepcopy(PYTHON_MINOR_DATA)

        # Act
        output = pypistats._monthly_total(data)

        # Assert
        assert len(output) == 64

        assert output[0]["category"] == "2.4"
        assert output[0]["downloads"] == 1
        assert output[0]["date"] == "2018-04"

        assert output[10]["category"] == "2.7"
        assert output[10]["downloads"] == 489_163
        assert output[10]["date"] == "2018-05"

    def test__total(self) -> None:
        # Arrange
        data = copy.deepcopy(PYTHON_MINOR_DATA)

        # Act
        output = pypistats._total(data)

        # Assert
        assert len(output) == 12
        assert output[0]["category"] == "2.4"
        assert output[0]["downloads"] == 9

    def test__validate_total(self) -> None:
        """Test the _validate_total method with valid and invalid inputs."""
        valid_values = ("daily", "monthly", "all")
        for value in valid_values:
            pypistats._validate_total(value)

        with pytest.raises(ValueError, match="total must be one of"):
            pypistats._validate_total("weekly")

    def test__total_recent(self) -> None:
        # Arrange
        data = copy.deepcopy(SAMPLE_DATA_RECENT)

        # Act
        output = pypistats._total(data)

        # Assert
        assert output == SAMPLE_DATA_RECENT

    def test__date_range(self) -> None:
        # Arrange
        data = copy.deepcopy(PYTHON_MINOR_DATA)

        # Act
        first, last = pypistats._date_range(data)

        # Assert
        assert first == "2018-04-16"
        assert last == "2018-09-23"

    def test__date_range_no_dates_in_data(self) -> None:
        # Arrange
        # recent
        data = [
            {
                "data": {"last_day": 70, "last_month": 445, "last_week": 268},
                "package": "dapy",
                "type": "recent_downloads",
            }
        ]

        # Act
        first, last = pypistats._date_range(data)

        # Assert
        assert first is None
        assert last is None

    def test__grand_total(self) -> None:
        # Arrange
        data = copy.deepcopy(PYTHON_MINOR_DATA)
        original_len = len(data)

        # Act
        output = pypistats._grand_total(data)

        # Assert
        assert len(output) == original_len + 1
        assert output[-1]["category"] == "Total"
        assert output[-1]["downloads"] == 9_355_317

    def test__grand_total_one_row(self) -> None:
        # Arrange
        data = copy.deepcopy(SAMPLE_DATA_ONE_ROW)

        # Act
        output = pypistats._grand_total(data)

        # Assert
        assert output == SAMPLE_DATA_ONE_ROW

    def test__grand_total_recent(self) -> None:
        # Arrange
        data = copy.deepcopy(SAMPLE_DATA_RECENT)

        # Act
        output = pypistats._grand_total(data)

        # Assert
        assert output == SAMPLE_DATA_RECENT

    def test__grand_total_value_mirrors(self) -> None:
        """Test the _grand_total_value logic for with_mirrors/without_mirrors."""
        # Use only max when both with_mirrors and without_mirrors are present
        data1 = [
            {"category": "with_mirrors", "downloads": 100},
            {"category": "without_mirrors", "downloads": 80},
        ]
        assert pypistats._grand_total_value(data1) == 100

        # Non-mirror data should be summed normally
        data2 = [
            {"category": "3.7", "downloads": 100},
            {"category": "3.8", "downloads": 200},
        ]
        assert pypistats._grand_total_value(data2) == 300

    def test__percent(self) -> None:
        # Arrange
        data = [
            {"category": "2.7", "downloads": 63749},
            {"category": "3.6", "downloads": 35274},
            {"category": "2.6", "downloads": 51},
            {"category": "3.2", "downloads": 2},
        ]
        expected_output = [
            {"category": "2.7", "percent": "64.34%", "downloads": 63749},
            {"category": "3.6", "percent": "35.60%", "downloads": 35274},
            {"category": "2.6", "percent": "0.05%", "downloads": 51},
            {"category": "3.2", "percent": "0.00%", "downloads": 2},
        ]

        # Act
        output = pypistats._percent(data)

        # Assert
        assert output == expected_output

    def test__percent_one_row(self) -> None:
        # Arrange
        data = copy.deepcopy(SAMPLE_DATA_ONE_ROW)

        # Act
        output = pypistats._percent(data)

        # Assert
        assert output == SAMPLE_DATA_ONE_ROW

    def test__percent_recent(self) -> None:
        # Arrange
        data = copy.deepcopy(SAMPLE_DATA_RECENT)

        # Act
        output = pypistats._percent(data)

        # Assert
        assert output == SAMPLE_DATA_RECENT

    @mock.patch("urllib3.request")
    def test_valid_json(self, mock_request) -> None:
        # Arrange
        package = "pip"
        mocked_response = """
        {"data": {"last_day": 1956060}, "package": "pip", "type": "recent_downloads"}
        """

        # Act
        mock_request.return_value = mock_urllib3_response(mocked_response)
        output = pypistats.recent(package, period="day", format="json")

        # Assert
        # Should not raise any errors eg. TypeError
        json.loads(output)
        assert json.loads(output) == json.loads(mocked_response)
        assert_called_with_url(
            mock_request, "https://pypistats.org/api/packages/pip/recent?&period=day"
        )

    @mock.patch("urllib3.request")
    @pytest.mark.parametrize(
        "test_format, expected_output",
        [
            pytest.param(
                "markdown",
                """
|  last_day | last_month |  last_week |
|---------: |----------: |----------: |
| 2,295,765 | 67,759,913 | 15,706,750 |
""",
                id="markdown",
            ),
            pytest.param(
                "tsv",
                """
"last_day"\t"last_month"\t"last_week"
2,295,765\t67,759,913\t15,706,750
""",
                id="tsv",
            ),
        ],
    )
    def test_recent_tabular(self, mock_request, test_format, expected_output) -> None:
        # Arrange
        package = "pip"
        mocked_response = """{
            "data":
                {"last_day": 2295765, "last_month": 67759913, "last_week": 15706750},
            "package": "pip", "type": "recent_downloads"
        }"""

        # Act
        mock_request.return_value = mock_urllib3_response(mocked_response)
        output = pypistats.recent(package, format=test_format)

        # Assert
        assert output.strip() == expected_output.strip()
        assert_called_with_url(
            mock_request, "https://pypistats.org/api/packages/pip/recent"
        )

    @mock.patch("urllib3.request")
    def test_overall_tabular_start_date(self, mock_request, monkeypatch) -> None:
        # Arrange
        package = "pip"
        mocked_response = SAMPLE_RESPONSE_OVERALL
        expected_output = """
| category        | percent | downloads |
| :---------------|-------: |---------: |
| with_mirrors    | 100.00% | 1,487,218 |
| without_mirrors |  99.24% | 1,475,979 |
| Total           |         | 1,487,218 |

Date range: 2020-05-02 - 2020-05-02
"""
        monkeypatch.setenv("NO_COLOR", "1")

        # Act
        mock_request.return_value = mock_urllib3_response(mocked_response)
        output = pypistats.overall(
            package, mirrors=False, start_date="2020-05-02", format="md"
        )

        # Assert
        assert output.strip() == expected_output.strip()
        assert_called_with_url(
            mock_request,
            "https://pypistats.org/api/packages/pip/overall?&mirrors=false",
        )

    @mock.patch("urllib3.request")
    def test_overall_tabular_end_date(self, mock_request, monkeypatch) -> None:
        # Arrange
        package = "pip"
        mocked_response = SAMPLE_RESPONSE_OVERALL
        expected_output = """
| category        | percent | downloads |
| :---------------|-------: |---------: |
| with_mirrors    | 100.00% | 2,100,139 |
| without_mirrors |  99.21% | 2,083,472 |
| Total           |         | 2,100,139 |

Date range: 2020-05-01 - 2020-05-01
"""
        monkeypatch.setenv("NO_COLOR", "1")

        # Act
        mock_request.return_value = mock_urllib3_response(mocked_response)
        output = pypistats.overall(
            package, mirrors=False, end_date="2020-05-01", format="md"
        )

        # Assert
        assert output.strip() == expected_output.strip()
        assert_called_with_url(
            mock_request,
            "https://pypistats.org/api/packages/pip/overall?&mirrors=false",
        )

    @mock.patch("urllib3.request")
    def test_python_major_json(self, mock_request) -> None:
        # Arrange
        package = "pip"
        mocked_response = """{
            "data": [
                {"category": "2", "date": "2018-11-01", "downloads": 2008344},
                {"category": "3", "date": "2018-11-01", "downloads": 280299},
                {"category": "null", "date": "2018-11-01", "downloads": 7122}
            ],
            "package": "pip",
            "type": "python_major_downloads"
        }"""
        expected_output = """{
            "data": [
                {"category": "2", "downloads": 2008344},
                {"category": "3", "downloads": 280299},
                {"category": "null", "downloads": 7122}
            ],
            "package": "pip",
            "type": "python_major_downloads"
        }"""

        # Act
        mock_request.return_value = mock_urllib3_response(mocked_response)
        output = pypistats.python_major(package, format="json")

        # Assert
        assert json.loads(output) == json.loads(expected_output)
        assert_called_with_url(
            mock_request, "https://pypistats.org/api/packages/pip/python_major"
        )

    @mock.patch("urllib3.request")
    def test_python_minor_json(self, mock_request) -> None:
        # Arrange
        package = "pip"
        mocked_response = """{
            "data": [
                {"category": "2.6", "date": "2018-11-01", "downloads": 6863},
                {"category": "2.7", "date": "2018-11-01", "downloads": 2001481},
                {"category": "3.2", "date": "2018-11-01", "downloads": 9},
                {"category": "3.3", "date": "2018-11-01", "downloads": 414},
                {"category": "3.4", "date": "2018-11-01", "downloads": 62166},
                {"category": "3.5", "date": "2018-11-01", "downloads": 79425},
                {"category": "3.6", "date": "2018-11-01", "downloads": 112266},
                {"category": "3.7", "date": "2018-11-01", "downloads": 25961},
                {"category": "3.8", "date": "2018-11-01", "downloads": 58},
                {"category": "null", "date": "2018-11-01", "downloads": 7122}
            ],
            "package": "pip",
            "type": "python_minor_downloads"
        }"""
        expected_output = """{
            "data": [
                {"category": "2.6", "downloads": 6863},
                {"category": "2.7", "downloads": 2001481},
                {"category": "3.2", "downloads": 9},
                {"category": "3.3", "downloads": 414},
                {"category": "3.4", "downloads": 62166},
                {"category": "3.5", "downloads": 79425},
                {"category": "3.6", "downloads": 112266},
                {"category": "3.7", "downloads": 25961},
                {"category": "3.8", "downloads": 58},
                {"category": "null", "downloads": 7122}
            ],
            "package": "pip",
            "type": "python_minor_downloads"
        }"""

        # Act
        mock_request.return_value = mock_urllib3_response(mocked_response)
        output = pypistats.python_minor(package, format="json")

        # Assert
        assert json.loads(output) == json.loads(expected_output)
        assert_called_with_url(
            mock_request, "https://pypistats.org/api/packages/pip/python_minor"
        )

    @mock.patch("urllib3.request")
    def test_system_tabular(self, mock_request, monkeypatch) -> None:
        # Arrange
        package = "pip"
        mocked_response = """{
            "data": [
                {"category": "Darwin", "downloads": 10734594},
                {"category": "Linux", "downloads": 236502274},
                {"category": "null", "downloads": 30579325},
                {"category": "other", "downloads": 111243},
                {"category": "Windows", "downloads": 6527978}
            ],
            "package": "pip",
            "type": "system_downloads"
        }"""
        expected_output = """
| category | percent |   downloads |
| :--------|-------: |-----------: |
| Linux    |  83.14% | 236,502,274 |
| null     |  10.75% |  30,579,325 |
| Darwin   |   3.77% |  10,734,594 |
| Windows  |   2.29% |   6,527,978 |
| other    |   0.04% |     111,243 |
| Total    |         | 284,455,414 |
"""
        monkeypatch.setenv("NO_COLOR", "1")

        # Act
        mock_request.return_value = mock_urllib3_response(mocked_response)
        output = pypistats.system(package, format="md")

        # Assert
        assert output.strip() == expected_output.strip()
        assert_called_with_url(
            mock_request, "https://pypistats.org/api/packages/pip/system"
        )

    @mock.patch("urllib3.request")
    def test_python_minor_monthly(self, mock_request) -> None:
        # Arrange
        package = "pip"
        mocked_response = """{
            "data": [
                {"category": "2.6", "date": "2018-11-01", "downloads": 1},
                {"category": "2.6", "date": "2018-11-02", "downloads": 2},
                {"category": "2.6", "date": "2018-12-11", "downloads": 3},
                {"category": "2.6", "date": "2018-12-12", "downloads": 4},
                {"category": "2.7", "date": "2018-11-01", "downloads": 10},
                {"category": "2.7", "date": "2018-11-02", "downloads": 20},
                {"category": "2.7", "date": "2018-12-11", "downloads": 30},
                {"category": "2.7", "date": "2018-12-12", "downloads": 40}
            ],
            "package": "pip",
            "type": "python_minor_downloads"
        }"""
        expected_output = """{
            "data": [
                {"category": "2.6", "date": "2018-11", "downloads": 3},
                {"category": "2.6", "date": "2018-12", "downloads": 7},
                {"category": "2.7", "date": "2018-11", "downloads": 30},
                {"category": "2.7", "date": "2018-12", "downloads": 70}
            ],
            "package": "pip",
            "type": "python_minor_downloads"
        }"""

        # Act
        mock_request.return_value = mock_urllib3_response(mocked_response)
        output = pypistats.python_minor(package, total="monthly", format="json")

        # Assert
        assert json.loads(output) == json.loads(expected_output)
        assert_called_with_url(
            mock_request, "https://pypistats.org/api/packages/pip/python_minor"
        )

    def test_versions_are_strings(self) -> None:
        # Arrange
        data = copy.deepcopy(SAMPLE_DATA_VERSION_STRINGS)
        expected_output = """
| category |    date    | downloads |
| :--------| :--------: |---------: |
| 3.1      | 2018-08-15 |        10 |
| 3.10     | 2018-08-15 |         1 |
"""

        # Act
        output = pypistats._tabulate(data, format_="markdown")

        # Assert
        assert output.strip() == expected_output.strip()

    @mock.patch("urllib3.request")
    def test_format_numpy(self, mock_request) -> None:
        # Arrange
        numpy = pytest.importorskip("numpy", reason="NumPy is not installed")
        package = "pip"
        mocked_response = SAMPLE_RESPONSE_OVERALL
        expected_output = """
[['with_mirrors' '100.00%' 3587357]
 ['without_mirrors' '99.22%' 3559451]
 ['Total' None 3587357]]
"""

        # Act
        mock_request.return_value = mock_urllib3_response(mocked_response)
        output = pypistats.overall(package, format="numpy")

        # Assert
        assert isinstance(output, numpy.ndarray)
        assert str(output).strip() == expected_output.strip()
        assert_called_with_url(
            mock_request, "https://pypistats.org/api/packages/pip/overall"
        )

    @mock.patch("urllib3.request")
    def test_format_pandas(self, mock_request) -> None:
        # Arrange
        pandas = pytest.importorskip("pandas", reason="pandas is not installed")
        package = "pip"
        mocked_response = SAMPLE_RESPONSE_OVERALL
        expected_output = """
          category  percent  downloads
0     with_mirrors  100.00%    3587357
1  without_mirrors   99.22%    3559451
2            Total     None    3587357
"""

        # Act
        mock_request.return_value = mock_urllib3_response(mocked_response)
        output = pypistats.overall(package, format="pandas")

        # Assert
        assert isinstance(output, pandas.DataFrame)
        assert str(output).strip() == expected_output.strip()
        assert_called_with_url(
            mock_request, "https://pypistats.org/api/packages/pip/overall"
        )

    @mock.patch("urllib3.request")
    def test_format_none(self, mock_request) -> None:
        # Arrange
        package = "pip"
        mocked_response = SAMPLE_RESPONSE_OVERALL
        expected_output = {
            "category": "with_mirrors",
            "downloads": 3587357,
            "percent": "100.00%",
        }

        # Act
        mock_request.return_value = mock_urllib3_response(mocked_response)
        output = pypistats.overall(package, format=None)

        # Assert
        assert output[0] == expected_output
        assert_called_with_url(
            mock_request, "https://pypistats.org/api/packages/pip/overall"
        )

    @mock.patch("urllib3.request")
    def test_package_not_exist(self, mock_request) -> None:
        # Arrange
        package = "a" * 100
        mocked_response = f"""{{
            "data":[],
            "package":"{package}",
            "type":"python_major_downloads"
        }}"""
        expected_output = f"No data found for https://pypi.org/project/{package}/"

        # Act
        mock_request.return_value = mock_urllib3_response(mocked_response)
        output = pypistats.python_major(package)

        # Assert
        assert output == expected_output
        assert_called_with_url(
            mock_request,
            f"https://pypistats.org/api/packages/{package}/python_major",
        )
