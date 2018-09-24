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
        from data.python_minor import data as input

        # Act
        output = pypistats._filter(input)

        # Assert
        self.assertEqual(input, output)

    def test__filter_start_date(self):
        # Arrange
        from data.python_minor import data as input

        start_date = "2018-09-22"

        # Act
        output = pypistats._filter(input, start_date=start_date)

        # Assert
        self.assertEqual(len(output), 20)
        for row in output:
            self.assertGreaterEqual(row["date"], start_date)

    def test__filter_end_date(self):
        # Arrange
        from data.python_minor import data as input

        end_date = "2018-04-22"

        # Act
        output = pypistats._filter(input, end_date=end_date)

        # Assert
        self.assertEqual(len(output), 62)
        for row in output:
            self.assertLessEqual(row["date"], end_date)

    def test__filter_start_and_end_date(self):
        # Arrange
        from data.python_minor import data as input

        start_date = "2018-09-01"
        end_date = "2018-09-11"

        # Act
        output = pypistats._filter(input, start_date=start_date, end_date=end_date)

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
        param = pypistats._paramify("version", 3)

        # Assert
        self.assertEqual(param, "&version=3")

    def test__paramify_float(self):
        # Arrange
        version = 3.7

        # Act
        param = pypistats._paramify("version", 3.7)

        # Assert
        self.assertEqual(param, "&version=3.7")
