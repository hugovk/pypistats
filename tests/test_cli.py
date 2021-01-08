"""
Unit tests for cli
"""
import argparse

import pytest
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
def test__valid_yyyy_mm_dd_valid(test_input):
    assert test_input == cli._valid_yyyy_mm_dd(test_input)


@pytest.mark.parametrize("test_input", ["asdfsdssd", "2018-99-99", "2018-xx"])
def test__valid_yyyy_mm_dd_invalid(test_input):
    with pytest.raises(argparse.ArgumentTypeError):
        cli._valid_yyyy_mm_dd(test_input)


@pytest.mark.parametrize("test_input", ["2018-01", "2018-07", "2018-12"])
def test__valid_yyyy_mm_valid(test_input):
    assert test_input == cli._valid_yyyy_mm(test_input)


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
def test__valid_yyyy_mm_valid_name(test_input, expected):
    assert expected == cli._valid_yyyy_mm(test_input)


@pytest.mark.parametrize("test_input", ["dfkgjskfjgk", "2018-99", "2018-xx"])
def test__valid_yyyy_mm_invalid(test_input):
    with pytest.raises(argparse.ArgumentTypeError):
        cli._valid_yyyy_mm(test_input)


@pytest.mark.parametrize("test_input", ["2019-01-21", "2019-01"])
def test__valid_yyyy_mm_optional_dd_valid(test_input):
    assert test_input == cli._valid_yyyy_mm_optional_dd(test_input)


@freeze_time("2019-05-08")
@pytest.mark.parametrize(
    "test_input, expected", [("jan", "2019-01"), ("february", "2019-02")]
)
def test__valid_yyyy_mm_optional_dd_valid_name(test_input, expected):
    assert expected == cli._valid_yyyy_mm_optional_dd(test_input)


@pytest.mark.parametrize("test_input", ["dkvnf", "2018-99", "2018-xx"])
def test__valid_yyyy_mm_optional_dd_invalid(test_input):
    with pytest.raises(argparse.ArgumentTypeError):
        cli._valid_yyyy_mm_optional_dd(test_input)


class __Args:
    def __init__(self):
        self.json = False  # type: bool
        self.format = "markdown"  # type: str


@pytest.mark.parametrize("test_input, expected", [(False, "markdown"), (True, "json")])
def test__define_format_json_flag(test_input, expected):
    # Arrange
    args = __Args()
    args.json = test_input

    # Act
    _format = cli._define_format(args)

    # Assert
    assert expected == _format


@pytest.mark.parametrize("test_input", ["json", "markdown"])
def test__define_format_format_flag(test_input):
    # Arrange
    args = __Args()
    args.json = False
    args.format = test_input

    # Act
    _format = cli._define_format(args)

    # Assert
    assert test_input == _format
