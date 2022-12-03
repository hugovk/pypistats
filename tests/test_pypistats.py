"""
Unit tests for pypistats
"""
import copy
import json
import os
from pathlib import Path
from unittest import mock

import pytest
import respx

import pypistats

from .data.expected_tabulated import (
    EXPECTED_TABULATED_BORDER,
    EXPECTED_TABULATED_HTML,
    EXPECTED_TABULATED_MD,
    EXPECTED_TABULATED_RST,
    EXPECTED_TABULATED_TSV,
)
from .data.python_minor import DATA as PYTHON_MINOR_DATA

try:
    import numpy
except ImportError:  # pragma: no cover
    numpy = None
try:
    import pandas
except ImportError:  # pragma: no cover
    pandas = None


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


class TestPypiStats:
    def setup_method(self) -> None:
        # Stub caching. Caches are tested in another class.
        self.original__cache_filename = pypistats._cache_filename
        self.original__save_cache = pypistats._save_cache
        pypistats._cache_filename = stub__cache_filename
        pypistats._save_cache = stub__save_cache

    def teardown_method(self) -> None:
        # Unstub caching
        pypistats._cache_filename = self.original__cache_filename
        pypistats._save_cache = self.original__save_cache

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

    @respx.mock
    def test_warn_if_start_date_before_earliest_available(self) -> None:
        # Arrange
        start_date = "2000-01-01"
        package = "pip"
        mocked_url = "https://pypistats.org/api/packages/pip/python_major"
        mocked_response = """{
            "data": [
                {"category": "2", "date": "2018-11-01", "downloads": 2008344},
                {"category": "3", "date": "2018-11-01", "downloads": 280299},
                {"category": "null", "date": "2018-11-01", "downloads": 7122}
            ],
            "package": "pip",
            "type": "python_major_downloads"
        }"""

        respx.get(mocked_url).respond(content=mocked_response)
        # Act / Assert
        with pytest.warns(
            UserWarning,
            match=r"Requested start date \(2000-01-01\) is before earliest available "
            r"data \(2018-11-01\), because data is only available for 180 days. "
            "See https://pypistats.org/about#data",
        ):
            pypistats.python_major(package, start_date=start_date)

    @respx.mock
    def test_error_if_end_date_before_earliest_available(self) -> None:
        # Arrange
        end_date = "2000-01-01"
        package = "pip"
        mocked_url = "https://pypistats.org/api/packages/pip/python_major"
        mocked_response = """{
            "data": [
                {"category": "2", "date": "2018-11-01", "downloads": 2008344},
                {"category": "3", "date": "2018-11-01", "downloads": 280299},
                {"category": "null", "date": "2018-11-01", "downloads": 7122}
            ],
            "package": "pip",
            "type": "python_major_downloads"
        }"""

        respx.get(mocked_url).respond(content=mocked_response)
        # Act / Assert
        with pytest.raises(
            ValueError,
            match=r"Requested end date \(2000-01-01\) is before earliest available "
            r"data \(2018-11-01\), because data is only available for 180 days. "
            "See https://pypistats.org/about#data",
        ):
            pypistats.python_major(package, end_date=end_date)

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

    @mock.patch.dict(os.environ, {"NO_COLOR": "TRUE"})
    def test__can_do_colour_no_color(self) -> None:
        # Act / Assert
        assert pypistats._can_do_colour() is False

    @mock.patch.dict(os.environ, {"FORCE_COLOR": "TRUE"})
    def test__can_do_colour_force_colour(self) -> None:
        # Act / Assert
        assert pypistats._can_do_colour() is True

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
        data = pypistats._percent(data)
        data = pypistats._grand_total(data)
        monkeypatch.setenv("FORCE_COLOR", "1")

        # Act
        output = pypistats._colourify(data)

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
            pytest.param("border", EXPECTED_TABULATED_BORDER, id="border"),
            pytest.param("markdown", EXPECTED_TABULATED_MD, id="markdown"),
            pytest.param("rst", EXPECTED_TABULATED_RST, id="rst"),
            pytest.param("tsv", EXPECTED_TABULATED_TSV, id="tsv"),
        ],
    )
    def test__tabulate(self, test_input: str, expected: str) -> None:
        # Arrange
        data = copy.deepcopy(SAMPLE_DATA)

        # Act
        output = pypistats._tabulate(data, format=test_input)

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

    @respx.mock
    def test_valid_json(self) -> None:
        # Arrange
        package = "pip"
        mocked_url = "https://pypistats.org/api/packages/pip/recent?&period=day"
        mocked_response = """
        {"data": {"last_day": 1956060}, "package": "pip", "type": "recent_downloads"}
        """

        # Act
        respx.get(mocked_url).respond(content=mocked_response)
        output = pypistats.recent(package, period="day", format="json")

        # Assert
        # Should not raise any errors eg. TypeError
        json.loads(output)
        assert json.loads(output) == json.loads(mocked_response)

    @respx.mock
    @pytest.mark.parametrize(
        "test_format, expected_output",
        [
            pytest.param(
                "markdown",
                """
|  last_day | last_month |  last_week |
|----------:|-----------:|-----------:|
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
    def test_recent_tabular(self, test_format, expected_output) -> None:
        # Arrange
        package = "pip"
        mocked_url = "https://pypistats.org/api/packages/pip/recent"
        mocked_response = """{
            "data":
                {"last_day": 2295765, "last_month": 67759913, "last_week": 15706750},
            "package": "pip", "type": "recent_downloads"
        }"""

        # Act
        respx.get(mocked_url).respond(content=mocked_response)
        output = pypistats.recent(package, format=test_format)

        # Assert
        assert output.strip() == expected_output.strip()

    @respx.mock
    def test_overall_tabular_start_date(self) -> None:
        # Arrange
        package = "pip"
        mocked_url = "https://pypistats.org/api/packages/pip/overall?&mirrors=false"
        mocked_response = SAMPLE_RESPONSE_OVERALL
        expected_output = """
| category        | percent | downloads |
|:----------------|--------:|----------:|
| with_mirrors    | 100.00% | 1,487,218 |
| without_mirrors |  99.24% | 1,475,979 |
| Total           |         | 1,487,218 |

Date range: 2020-05-02 - 2020-05-02
"""

        # Act
        respx.get(mocked_url).respond(content=mocked_response)
        output = pypistats.overall(
            package, mirrors=False, start_date="2020-05-02", format="md"
        )

        # Assert
        assert output.strip() == expected_output.strip()

    @respx.mock
    def test_overall_tabular_end_date(self) -> None:
        # Arrange
        package = "pip"
        mocked_url = "https://pypistats.org/api/packages/pip/overall?&mirrors=false"
        mocked_response = SAMPLE_RESPONSE_OVERALL
        expected_output = """
| category        | percent | downloads |
|:----------------|--------:|----------:|
| with_mirrors    | 100.00% | 2,100,139 |
| without_mirrors |  99.21% | 2,083,472 |
| Total           |         | 2,100,139 |

Date range: 2020-05-01 - 2020-05-01
"""

        # Act
        respx.get(mocked_url).respond(content=mocked_response)
        output = pypistats.overall(
            package, mirrors=False, end_date="2020-05-01", format="md"
        )

        # Assert
        assert output.strip() == expected_output.strip()

    @respx.mock
    def test_python_major_json(self) -> None:
        # Arrange
        package = "pip"
        mocked_url = "https://pypistats.org/api/packages/pip/python_major"
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
        respx.get(mocked_url).respond(content=mocked_response)
        output = pypistats.python_major(package, format="json")

        # Assert
        assert json.loads(output) == json.loads(expected_output)

    @respx.mock
    def test_python_minor_json(self) -> None:
        # Arrange
        package = "pip"
        mocked_url = "https://pypistats.org/api/packages/pip/python_minor"
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
        respx.get(mocked_url).respond(content=mocked_response)
        output = pypistats.python_minor(package, format="json")

        # Assert
        assert json.loads(output) == json.loads(expected_output)

    @respx.mock
    def test_system_tabular(self) -> None:
        # Arrange
        package = "pip"
        mocked_url = "https://pypistats.org/api/packages/pip/system"
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
|:---------|--------:|------------:|
| Linux    |  83.14% | 236,502,274 |
| null     |  10.75% |  30,579,325 |
| Darwin   |   3.77% |  10,734,594 |
| Windows  |   2.29% |   6,527,978 |
| other    |   0.04% |     111,243 |
| Total    |         | 284,455,414 |
"""

        # Act
        respx.get(mocked_url).respond(content=mocked_response)
        output = pypistats.system(package, format="md")

        # Assert
        assert output.strip() == expected_output.strip()

    @respx.mock
    def test_python_minor_monthly(self) -> None:
        # Arrange
        package = "pip"
        mocked_url = "https://pypistats.org/api/packages/pip/python_minor"
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
        respx.get(mocked_url).respond(content=mocked_response)
        output = pypistats.python_minor(package, total="monthly", format="json")

        # Assert
        assert json.loads(output) == json.loads(expected_output)

    @respx.mock
    def test_versions_are_strings(self) -> None:
        # Arrange
        data = copy.deepcopy(SAMPLE_DATA_VERSION_STRINGS)
        expected_output = """
| category |    date    | downloads |
|:---------|:----------:|----------:|
| 3.1      | 2018-08-15 |        10 |
| 3.10     | 2018-08-15 |         1 |
"""

        # Act
        output = pypistats._tabulate(data, format="markdown")

        # Assert
        assert output.strip() == expected_output.strip()

    @pytest.mark.skipif(numpy is None, reason="NumPy is not installed")
    @respx.mock
    def test_format_numpy(self) -> None:
        # Arrange
        package = "pip"
        mocked_url = "https://pypistats.org/api/packages/pip/overall"
        mocked_response = SAMPLE_RESPONSE_OVERALL
        expected_output = """
[['with_mirrors' '100.00%' 3587357]
 ['without_mirrors' '99.22%' 3559451]
 ['Total' None 3587357]]
"""

        # Act
        respx.get(mocked_url).respond(content=mocked_response)
        output = pypistats.overall(package, format="numpy")

        # Assert
        assert isinstance(output, numpy.ndarray)
        assert str(output).strip() == expected_output.strip()

    @pytest.mark.skipif(pandas is None, reason="pandas is not installed")
    @respx.mock
    def test_format_pandas(self) -> None:
        # Arrange
        package = "pip"
        mocked_url = "https://pypistats.org/api/packages/pip/overall"
        mocked_response = SAMPLE_RESPONSE_OVERALL
        expected_output = """
          category  percent  downloads
0     with_mirrors  100.00%    3587357
1  without_mirrors   99.22%    3559451
2            Total     None    3587357
"""

        # Act
        respx.get(mocked_url).respond(content=mocked_response)
        output = pypistats.overall(package, format="pandas")

        # Assert
        assert isinstance(output, pandas.DataFrame)
        assert str(output).strip() == expected_output.strip()
