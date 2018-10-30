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
    class __Args:
        def __init__(self):
            self.json = False  # type: bool
            self.format = "markdown"  # type: str

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

    def test__define_format_default(self):
        # Setup
        args = self.__Args()
        args.json = False

        _format = cli._define_format(args)
        self.assertEqual(_format, "markdown")

    def test__define_format_json_flag(self):
        args = self.__Args()
        args.json = True

        _format = cli._define_format(args)
        self.assertEqual(_format, "json")

    def test__define_format_json(self):
        args = self.__Args()
        args.json = False
        args.format = "json"

        _format = cli._define_format(args)
        self.assertEqual(_format, "json")

    def test__define_format_markdown(self):
        args = self.__Args()
        args.json = False
        args.format = "markdown"

        _format = cli._define_format(args)
        self.assertEqual(_format, "markdown")
