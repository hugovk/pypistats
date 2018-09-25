#!/usr/bin/env python3
# encoding: utf-8
"""
Unit tests for pypistats
"""
import unittest

import pypistats


class TestPypiStats(unittest.TestCase):
    def test__filter_no_filters_no_change(self):
        # Arrange
        from data.python_minor import data

        # Act
        output = pypistats._filter(data)

        # Assert
        self.assertEqual(data, output)

    def test__filter_start_date(self):
        # Arrange
        from data.python_minor import data

        start_date = "2018-09-22"

        # Act
        output = pypistats._filter(data, start_date=start_date)

        # Assert
        self.assertEqual(len(output), 20)
        for row in output:
            self.assertGreaterEqual(row["date"], start_date)

    def test__filter_end_date(self):
        # Arrange
        from data.python_minor import data

        end_date = "2018-04-22"

        # Act
        output = pypistats._filter(data, end_date=end_date)

        # Assert
        self.assertEqual(len(output), 62)
        for row in output:
            self.assertLessEqual(row["date"], end_date)

    def test__filter_start_and_end_date(self):
        # Arrange
        from data.python_minor import data

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

    def test__tabulate(self):
        # Arrange
        data = [
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
        expected_output = """
| category |    date    | downloads |
|----------|------------|----------:|
|      2.6 | 2018-08-15 |        51 |
|      2.7 | 2018-08-15 |     63749 |
|      3.2 | 2018-08-15 |         2 |
|      3.3 | 2018-08-15 |        40 |
|      3.4 | 2018-08-15 |      6095 |
|      3.5 | 2018-08-15 |     20358 |
|      3.6 | 2018-08-15 |     35274 |
|      3.7 | 2018-08-15 |      6595 |
|      3.8 | 2018-08-15 |         3 |
| null     | 2018-08-15 |      1019 |
"""

        # Act
        output = pypistats._tabulate(data)

        # Assert
        self.assertEqual(output.strip(), expected_output.strip())

    def test__total(self):
        # Arrange
        from data.python_minor import data

        # Act
        output = pypistats._total(data)

        # Assert
        self.assertEqual(len(output), 12)
        self.assertEqual(output[0]["category"], "2.4")
        self.assertEqual(output[0]["downloads"], 9)
