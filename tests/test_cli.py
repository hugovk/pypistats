#!/usr/bin/env python3
# encoding: utf-8
"""
Unit tests for cli
"""
import argparse
import unittest

from freezegun import freeze_time

from pypistats import cli


class TestCli(unittest.TestCase):
    def test__month(self):
        # Arrange
        yyyy_mm = "2018-07"

        # Act
        first, last = cli._month(yyyy_mm)

        # Assert
        self.assertEqual(first, "2018-07-01")
        self.assertEqual(last, "2018-07-31")

    @freeze_time("2018-09-25")
    def test__last_month(self):
        # Arrange
        # Act
        first, last = cli._last_month()

        # Assert
        self.assertEqual(first, "2018-08-01")
        self.assertEqual(last, "2018-08-31")

    def test__valid_yyyy_mm_dd(self):
        # Arrange
        input = "2018-07-12"

        # Act
        output = cli._valid_yyyy_mm_dd(input)

        # Assert
        self.assertEqual(input, output)

    def test__valid_yyyy_mm_dd_invalid(self):
        # Arrange
        input = "asdfsdssd"

        # Act / Assert
        with self.assertRaises(argparse.ArgumentTypeError):
            cli._valid_yyyy_mm_dd(input)

    def test__valid_yyyy_mm_dd_invalid2(self):
        # Arrange
        input = "2018-99-99"

        # Act / Assert
        with self.assertRaises(argparse.ArgumentTypeError):
            cli._valid_yyyy_mm_dd(input)

    def test__valid_yyyy_mm(self):
        # Arrange
        input = "2018-07"

        # Act
        output = cli._valid_yyyy_mm(input)

        # Assert
        self.assertEqual(input, output)

    def test__valid_yyyy_mm_invalid(self):
        # Arrange
        input = "dfkgjskfjgk"

        # Act / Assert
        with self.assertRaises(argparse.ArgumentTypeError):
            cli._valid_yyyy_mm(input)

    def test__valid_yyyy_mm_invalid2(self):
        # Arrange
        input = "2018-99"

        # Act / Assert
        with self.assertRaises(argparse.ArgumentTypeError):
            cli._valid_yyyy_mm(input)
