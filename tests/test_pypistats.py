#!/usr/bin/env python3
# encoding: utf-8
"""
Unit tests for pypistats
"""
import copy
import json
import unittest

import requests_mock

import pypistats
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
SAMPLE_DATA_ONE_ROW = [{"category": "with_mirrors", "downloads": 11497042}]
SAMPLE_DATA_RECENT = {"last_day": 123002, "last_month": 3254221, "last_week": 761649}


class TestPypiStats(unittest.TestCase):
    def test__filter_no_filters_no_change(self):
        # Arrange
        data = copy.deepcopy(PYTHON_MINOR_DATA)

        # Act
        output = pypistats._filter(data)

        # Assert
        self.assertEqual(data, output)

    def test__filter_start_date(self):
        # Arrange
        data = copy.deepcopy(PYTHON_MINOR_DATA)
        start_date = "2018-09-22"

        # Act
        output = pypistats._filter(data, start_date=start_date)

        # Assert
        self.assertEqual(len(output), 20)
        for row in output:
            self.assertGreaterEqual(row["date"], start_date)

    def test__filter_end_date(self):
        # Arrange
        data = copy.deepcopy(PYTHON_MINOR_DATA)
        end_date = "2018-04-22"

        # Act
        output = pypistats._filter(data, end_date=end_date)

        # Assert
        self.assertEqual(len(output), 62)
        for row in output:
            self.assertLessEqual(row["date"], end_date)

    def test__filter_start_and_end_date(self):
        # Arrange
        data = copy.deepcopy(PYTHON_MINOR_DATA)
        start_date = "2018-09-01"
        end_date = "2018-09-11"

        # Act
        output = pypistats._filter(data, start_date=start_date, end_date=end_date)

        # Assert
        self.assertEqual(len(output), 112)
        for row in output:
            self.assertGreaterEqual(row["date"], start_date)
            self.assertLessEqual(row["date"], end_date)

    def test__paramify_none(self):
        # Arrange
        period = None

        # Act
        param = pypistats._paramify("period", period)

        # Assert
        self.assertEqual(param, "")

    def test__paramify_string(self):
        # Arrange
        period = "day"

        # Act
        param = pypistats._paramify("period", period)

        # Assert
        self.assertEqual(param, "&period=day")

    def test__paramify_bool(self):
        # Arrange
        mirrors = True

        # Act
        param = pypistats._paramify("mirrors", mirrors)

        # Assert
        self.assertEqual(param, "&mirrors=true")

    def test__paramify_int(self):
        # Arrange
        version = 3

        # Act
        param = pypistats._paramify("version", version)

        # Assert
        self.assertEqual(param, "&version=3")

    def test__paramify_float(self):
        # Arrange
        version = 3.7

        # Act
        param = pypistats._paramify("version", version)

        # Assert
        self.assertEqual(param, "&version=3.7")

    def test__tabulate_noarg(self):
        # Arrange
        data = copy.deepcopy(SAMPLE_DATA)
        expected_output = """
| category |    date    | downloads |
|----------|------------|----------:|
|      2.6 | 2018-08-15 |        51 |
|      2.7 | 2018-08-15 |    63,749 |
|      3.2 | 2018-08-15 |         2 |
|      3.3 | 2018-08-15 |        40 |
|      3.4 | 2018-08-15 |     6,095 |
|      3.5 | 2018-08-15 |    20,358 |
|      3.6 | 2018-08-15 |    35,274 |
|      3.7 | 2018-08-15 |     6,595 |
|      3.8 | 2018-08-15 |         3 |
| null     | 2018-08-15 |     1,019 |
"""

        # Act
        output = pypistats._tabulate(data)

        # Assert
        self.assertEqual(output.strip(), expected_output.strip())

    def test__tabulate_markdown(self):
        # Arrange
        data = copy.deepcopy(SAMPLE_DATA)
        expected_output = """
| category |    date    | downloads |
|----------|------------|----------:|
|      2.6 | 2018-08-15 |        51 |
|      2.7 | 2018-08-15 |    63,749 |
|      3.2 | 2018-08-15 |         2 |
|      3.3 | 2018-08-15 |        40 |
|      3.4 | 2018-08-15 |     6,095 |
|      3.5 | 2018-08-15 |    20,358 |
|      3.6 | 2018-08-15 |    35,274 |
|      3.7 | 2018-08-15 |     6,595 |
|      3.8 | 2018-08-15 |         3 |
| null     | 2018-08-15 |     1,019 |
"""

        # Act
        output = pypistats._tabulate(data, format="markdown")

        # Assert
        self.assertEqual(output.strip(), expected_output.strip())

    def test__tabulate_rst(self):
        # Arrange
        data = copy.deepcopy(SAMPLE_DATA)
        expected_output = """
.. table:: 

    ==========  ============  ===========
     category       date       downloads 
    ==========  ============  ===========
          2.6    2018-08-15           51 
          2.7    2018-08-15       63,749 
          3.2    2018-08-15            2 
          3.3    2018-08-15           40 
          3.4    2018-08-15        6,095 
          3.5    2018-08-15       20,358 
          3.6    2018-08-15       35,274 
          3.7    2018-08-15        6,595 
          3.8    2018-08-15            3 
     null        2018-08-15        1,019 
    ==========  ============  ===========
"""  # noqa: W291

        # Act
        output = pypistats._tabulate(data, format="rst")

        # Assert
        self.assertEqual(output.strip(), expected_output.strip())

    def test__tabulate_html(self):
        # Arrange
        data = copy.deepcopy(SAMPLE_DATA)
        expected_output = """
<table>
    <thead>
        <tr>
            <th>category</th>
            <th>date</th>
            <th>downloads</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="right">2.6</td>
            <td align="left">2018-08-15</td>
            <td align="right">51</td>
        </tr>
        <tr>
            <td align="right">2.7</td>
            <td align="left">2018-08-15</td>
            <td align="right">63,749</td>
        </tr>
        <tr>
            <td align="right">3.2</td>
            <td align="left">2018-08-15</td>
            <td align="right">2</td>
        </tr>
        <tr>
            <td align="right">3.3</td>
            <td align="left">2018-08-15</td>
            <td align="right">40</td>
        </tr>
        <tr>
            <td align="right">3.4</td>
            <td align="left">2018-08-15</td>
            <td align="right">6,095</td>
        </tr>
        <tr>
            <td align="right">3.5</td>
            <td align="left">2018-08-15</td>
            <td align="right">20,358</td>
        </tr>
        <tr>
            <td align="right">3.6</td>
            <td align="left">2018-08-15</td>
            <td align="right">35,274</td>
        </tr>
        <tr>
            <td align="right">3.7</td>
            <td align="left">2018-08-15</td>
            <td align="right">6,595</td>
        </tr>
        <tr>
            <td align="right">3.8</td>
            <td align="left">2018-08-15</td>
            <td align="right">3</td>
        </tr>
        <tr>
            <td align="left">null</td>
            <td align="left">2018-08-15</td>
            <td align="right">1,019</td>
        </tr>
    </tbody>
</table>
        """

        # Act
        output = pypistats._tabulate(data, format="html")

        # Assert
        self.assertEqual(output.strip(), expected_output.strip())

    def test__sort(self):
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
        self.assertEqual(output, expected_output)

    def test__sort_recent(self):
        # Arrange
        data = copy.deepcopy(SAMPLE_DATA_RECENT)

        # Act
        output = pypistats._sort(data)

        # Assert
        self.assertEqual(output, SAMPLE_DATA_RECENT)

    def test__total(self):
        # Arrange
        data = copy.deepcopy(PYTHON_MINOR_DATA)

        # Act
        output = pypistats._total(data)

        # Assert
        self.assertEqual(len(output), 12)
        self.assertEqual(output[0]["category"], "2.4")
        self.assertEqual(output[0]["downloads"], 9)

    def test__total_recent(self):
        # Arrange
        data = copy.deepcopy(SAMPLE_DATA_RECENT)

        # Act
        output = pypistats._total(data)

        # Assert
        self.assertEqual(output, SAMPLE_DATA_RECENT)

    def test__grand_total(self):
        # Arrange
        data = copy.deepcopy(PYTHON_MINOR_DATA)
        original_len = len(data)

        # Act
        output = pypistats._grand_total(data)

        # Assert
        self.assertEqual(len(output), original_len + 1)
        self.assertEqual(output[-1]["category"], "Total")
        self.assertEqual(output[-1]["downloads"], 9355317)

    def test__grand_total_one_row(self):
        # Arrange
        data = copy.deepcopy(SAMPLE_DATA_ONE_ROW)

        # Act
        output = pypistats._grand_total(data)

        # Assert
        self.assertEqual(output, SAMPLE_DATA_ONE_ROW)

    def test__grand_total_recent(self):
        # Arrange
        data = copy.deepcopy(SAMPLE_DATA_RECENT)

        # Act
        output = pypistats._grand_total(data)

        # Assert
        self.assertEqual(output, SAMPLE_DATA_RECENT)

    def test__percent(self):
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
        self.assertEqual(output, expected_output)

    def test__percent_one_row(self):
        # Arrange
        data = copy.deepcopy(SAMPLE_DATA_ONE_ROW)

        # Act
        output = pypistats._percent(data)

        # Assert
        self.assertEqual(output, SAMPLE_DATA_ONE_ROW)

    def test__percent_recent(self):
        # Arrange
        data = copy.deepcopy(SAMPLE_DATA_RECENT)

        # Act
        output = pypistats._percent(data)

        # Assert
        self.assertEqual(output, SAMPLE_DATA_RECENT)

    def test__custom_list(self):
        # Arrange
        input_list = [1, 2, 3, 4]
        special_item = 3
        default_value = 0
        special_value = 100

        # Act
        output = pypistats._custom_list(
            input_list, special_item, default_value, special_value
        )

        # Assert
        self.assertEqual(output, [0, 0, 100, 0])

    def test_valid_json(self):
        # Arrange
        package = "pip"
        mocked_url = "https://pypistats.org/api/packages/pip/recent?&period=day"
        mocked_response = """
        {"data": {"last_day": 1956060}, "package": "pip", "type": "recent_downloads"}
        """

        # Act
        with requests_mock.Mocker() as m:
            m.get(mocked_url, text=mocked_response)
            output = pypistats.recent(package, period="day", format="json")

        # Assert
        # Should not raise any errors eg. TypeError
        json.loads(output)
        self.assertEqual(json.loads(output), json.loads(mocked_response))

    def test_recent_tabular(self):
        # Arrange
        package = "pip"
        mocked_url = "https://pypistats.org/api/packages/pip/recent"
        mocked_response = """{
            "data":
                {"last_day": 2295765, "last_month": 67759913, "last_week": 15706750},
            "package": "pip", "type": "recent_downloads"
        }"""
        expected_output = """
| last_day  | last_month | last_week  |
|----------:|-----------:|-----------:|
| 2,295,765 | 67,759,913 | 15,706,750 |
"""

        # Act
        with requests_mock.Mocker() as m:
            m.get(mocked_url, text=mocked_response)
            output = pypistats.recent(package)

        # Assert
        self.assertEqual(output.strip(), expected_output.strip())

    def test_overall_tabular_start_date(self):
        # Arrange
        package = "pip"
        mocked_url = "https://pypistats.org/api/packages/pip/overall"
        mocked_response = """{
          "data": [
            {"category": "without_mirrors", "date": "2018-11-01", "downloads": 2295765},
            {"category": "without_mirrors", "date": "2018-11-02", "downloads": 2297591}
          ],
          "package": "pip",
          "type": "overall_downloads"
        }"""
        expected_output = """
|    category     | downloads |
|-----------------|----------:|
| without_mirrors | 2,297,591 |
"""

        # Act
        with requests_mock.Mocker() as m:
            m.get(mocked_url, text=mocked_response)
            output = pypistats.overall(package, mirrors=False, start_date="2018-11-02")

        # Assert
        self.assertEqual(output.strip(), expected_output.strip())

    def test_python_major_json(self):
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
        with requests_mock.Mocker() as m:
            m.get(mocked_url, text=mocked_response)
            output = pypistats.python_major(package, format="json")

        # Assert
        self.assertEqual(json.loads(output), json.loads(expected_output))

    def test_python_minor_json(self):
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
        with requests_mock.Mocker() as m:
            m.get(mocked_url, text=mocked_response)
            output = pypistats.python_minor(package, format="json")

        # Assert
        self.assertEqual(json.loads(output), json.loads(expected_output))

    def test_system_tabular(self):
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
| category | percent |  downloads  |
|----------|--------:|------------:|
| Linux    |  83.14% | 236,502,274 |
| null     |  10.75% |  30,579,325 |
| Darwin   |   3.77% |  10,734,594 |
| Windows  |   2.29% |   6,527,978 |
| other    |   0.04% |     111,243 |
| Total    |         | 284,455,414 |
"""

        # Act
        with requests_mock.Mocker() as m:
            m.get(mocked_url, text=mocked_response)
            output = pypistats.system(package)

        # Assert
        self.assertEqual(output.strip(), expected_output.strip())
