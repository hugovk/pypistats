#!/usr/bin/env python3
# encoding: utf-8
"""
Unit tests for cli
"""
import argparse
import pytest
import unittest

from freezegun import freeze_time

from pypistats import cli


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("2018-07", ("2018-07-01", "2018-07-31")),
        ("2018-12", ("2018-12-01", "2018-12-31")),
    ],
)
def test__month(test_input, expected):
    # Act
    first, last = cli._month(test_input)

    # Assert
    assert expected == (first, last)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("2018-01-25", ("2017-12-01", "2017-12-31")),
        ("2018-09-25", ("2018-08-01", "2018-08-31")),
        ("2018-12-25", ("2018-11-01", "2018-11-30")),
    ],
)
def test__last_month(test_input, expected):
    # Act
    with freeze_time(test_input):
        first, last = cli._last_month()

    # Assert
    assert expected == (first, last)


@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("2019-03-10", "2019-03-01"),
        ("2019-05-08", "2019-05-01"),
        ("2019-12-25", "2019-12-01"),
    ],
)
def test__this_month(test_input, expected):
    # Act
    with freeze_time(test_input):
        first = cli._this_month()

    # Assert
    assert expected == first


@freeze_time("2019-05-08")
@pytest.mark.parametrize(
    "name, date_format, expected",
    [
        ("jan", "%b", "2019-01"),
        ("Jan", "%b", "2019-01"),
        ("january", "%B", "2019-01"),
        ("January", "%B", "2019-01"),
        ("feb", "%b", "2019-02"),
        ("february", "%B", "2019-02"),
        ("may", "%b", "2019-05"),
        ("dec", "%b", "2018-12"),
        ("december", "%B", "2018-12"),
    ],
)
def test__month_name_to_yyyy_mm(name, date_format, expected):
    # Act
    output = cli._month_name_to_yyyy_mm(name, date_format)

    # Assert
    assert expected == output


@pytest.mark.parametrize("test_input", ["2018-01-12", "2018-07-12", "2018-12-12"])
def test__valid_yyyy_mm_dd(test_input):
    assert test_input == cli._valid_yyyy_mm_dd(test_input)


@pytest.mark.parametrize("test_input", ["asdfsdssd", "2018-99-99", "2018-xx"])
def test__valid_yyyy_mm_dd_invalid(test_input):
    with pytest.raises(argparse.ArgumentTypeError):
        cli._valid_yyyy_mm_dd(test_input)


@freeze_time("2019-05-08")
@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("jan", "2019-01"),
        ("Jan", "2019-01"),
        ("january", "2019-01"),
        ("January", "2019-01"),
        ("feb", "2019-02"),
        ("february", "2019-02"),
        ("may", "2019-05"),
        ("dec", "2018-12"),
        ("december", "2018-12"),
    ],
)
def test__valid_yyyy_mm(test_input, expected):
    assert expected == cli._valid_yyyy_mm(test_input)


class TestCli(unittest.TestCase):
    class __Args:
        def __init__(self):
            self.json = False  # type: bool
            self.format = "markdown"  # type: str

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

    def test__valid_yyyy_mm_optional_dd1(self):
        # Arrange
        input = "2019-01-21"

        # Act
        output = cli._valid_yyyy_mm_optional_dd(input)

        # Assert
        self.assertEqual(input, output)

    def test__valid_yyyy_mm_optional_dd2(self):
        # Arrange
        input = "2019-01"

        # Act
        output = cli._valid_yyyy_mm_optional_dd(input)

        # Assert
        self.assertEqual(input, output)

    def test__valid_yyyy_mm_optional_dd_invalid(self):
        # Arrange
        input = "dkvnf"

        # Act / Assert
        with self.assertRaises(argparse.ArgumentTypeError):
            cli._valid_yyyy_mm_dd(input)

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
