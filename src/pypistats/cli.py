#!/usr/bin/env python3
# encoding: utf-8
"""
CLI with subcommands for pypistats
"""
import argparse
from datetime import date, datetime

from dateutil.relativedelta import relativedelta

import pypistats

cli = argparse.ArgumentParser()
subparsers = cli.add_subparsers(dest="subcommand")


def argument(*name_or_flags, **kwargs):
    """Convenience function to properly format arguments to pass to the
    subcommand decorator.

    """
    return list(name_or_flags), kwargs


def subcommand(args=None, parent=subparsers):
    """Decorator to define a new subcommand in a sanity-preserving way.
    The function will be stored in the ``func`` variable when the parser
    parses arguments so that it can be called directly like so::

        args = cli.parse_args()
        args.func(args)

    Usage example::

        @subcommand([argument("-d", help="Enable debug mode", action="store_true")])
        def subcommand(args):
            print(args)

    Then on the command line::

        $ python cli.py subcommand -d

    https://mike.depalatis.net/blog/simplifying-argparse.html
    """
    if args is None:
        args = []

    def decorator(func):
        func2 = getattr(pypistats, func.__name__)
        parser = parent.add_parser(
            func.__name__,
            description=func2.__doc__,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        for arg in args:
            parser.add_argument(*arg[0], **arg[1])
        parser.set_defaults(func=func)

    return decorator


def _month_name_to_yyyy_mm(date_string, date_format):
    """Given a month name, return yyyy-dd for the most recent month in the past"""
    today = date.today()
    new = datetime.strptime(f"{date_string} {today.year}", f"{date_format} %Y").date()
    if new < today:
        return new.isoformat()[:7]

    new = datetime.strptime(f"{date_string} {today.year-1}", f"{date_format} %Y").date()
    return new.isoformat()[:7]


def _valid_date(date_string, date_format):
    try:
        datetime.strptime(date_string, date_format)
        return date_string
    except ValueError:
        msg = f"Not a valid date: '{date_string}'."
        raise argparse.ArgumentTypeError(msg)


def _valid_yyyy_mm_dd(date_string):
    return _valid_date(date_string, "%Y-%m-%d")


def _valid_yyyy_mm(date_string):
    try:
        # eg. jan, feb
        date_string = _month_name_to_yyyy_mm(date_string, "%b")
    except ValueError:
        pass

    try:
        # eg. january, february
        date_string = _month_name_to_yyyy_mm(date_string, "%B")
    except ValueError:
        pass

    return _valid_date(date_string, "%Y-%m")


def _valid_yyyy_mm_optional_dd(date_string):
    try:
        return _valid_yyyy_mm_dd(date_string)
    except argparse.ArgumentTypeError:
        return _valid_yyyy_mm(date_string)


def _define_format(args) -> str:
    if args.json:
        return "json"

    return args.format


FORMATS = ("json", "markdown", "rst", "html")

arg_start_date = argument(
    "-sd",
    "--start-date",
    metavar="yyyy-mm[-dd]|name",
    type=_valid_yyyy_mm_optional_dd,
    help="Start date",
)
arg_end_date = argument(
    "-ed",
    "--end-date",
    metavar="yyyy-mm[-dd]|name",
    type=_valid_yyyy_mm_optional_dd,
    help="End date",
)
arg_month = argument(
    "-m",
    "--month",
    metavar="yyyy-mm|name",
    type=_valid_yyyy_mm,
    help="Shortcut for -sd & -ed for a single month",
)
arg_last_month = argument(
    "-l",
    "--last-month",
    help="Shortcut for -sd & -ed for last month",
    action="store_true",
)
arg_this_month = argument(
    "-t", "--this-month", help="Shortcut for -sd for this month", action="store_true"
)
arg_json = argument("-j", "--json", action="store_true", help='Shortcut for "-f json"')
arg_daily = argument("-d", "--daily", action="store_true", help="Show daily downloads")
arg_monthly = argument("--monthly", action="store_true", help="Show monthly downloads")
arg_format = argument(
    "-f", "--format", default="markdown", choices=FORMATS, help="The format of output"
)
arg_verbose = argument(
    "-v", "--verbose", action="store_true", help="Print debug messages to stderr"
)

# These are used by all except the 'recent' subcommand
common_arguments = [
    arg_format,
    arg_json,
    arg_start_date,
    arg_end_date,
    arg_month,
    arg_last_month,
    arg_this_month,
    arg_daily,
    arg_monthly,
    arg_verbose,
]


@subcommand(
    [
        argument("package"),
        argument("-p", "--period", choices=("day", "week", "month")),
        arg_format,
        arg_json,
        arg_verbose,
    ]
)
def recent(args):  # pragma: no cover
    print(
        pypistats.recent(
            args.package, period=args.period, format=args.format, verbose=args.verbose
        )
    )


@subcommand(
    [
        argument("package"),
        argument("--mirrors", choices=("true", "false", "with", "without")),
        *common_arguments,
    ]
)
def overall(args):  # pragma: no cover
    if args.mirrors in ["with", "without"]:
        args.mirrors = args.mirrors == "with"

    print(
        pypistats.overall(
            args.package,
            mirrors=args.mirrors,
            start_date=args.start_date,
            end_date=args.end_date,
            format=args.format,
            total="daily" if args.daily else ("monthly" if args.monthly else "all"),
            verbose=args.verbose,
        )
    )


@subcommand(
    [
        argument("package"),
        argument("-V", "--version", help="eg. 2 or 3"),
        *common_arguments,
    ]
)
def python_major(args):  # pragma: no cover
    print(
        pypistats.python_major(
            args.package,
            version=args.version,
            start_date=args.start_date,
            end_date=args.end_date,
            format=args.format,
            total="daily" if args.daily else ("monthly" if args.monthly else "all"),
            verbose=args.verbose,
        )
    )


@subcommand(
    [
        argument("package"),
        argument("-V", "--version", help="eg. 2.7 or 3.6"),
        *common_arguments,
    ]
)
def python_minor(args):  # pragma: no cover
    print(
        pypistats.python_minor(
            args.package,
            version=args.version,
            start_date=args.start_date,
            end_date=args.end_date,
            format=args.format,
            total="daily" if args.daily else ("monthly" if args.monthly else "all"),
            verbose=args.verbose,
        )
    )


@subcommand(
    [
        argument("package"),
        argument("-o", "--os", help="eg. windows, linux, darwin or other"),
        *common_arguments,
    ]
)
def system(args):  # pragma: no cover
    print(
        pypistats.system(
            args.package,
            os=args.os,
            start_date=args.start_date,
            end_date=args.end_date,
            format=args.format,
            total="daily" if args.daily else ("monthly" if args.monthly else "all"),
            verbose=args.verbose,
        )
    )


def _month(yyyy_mm):
    """Helper to return start_date and end_date of a month as yyyy-mm-dd"""
    year, month = map(int, yyyy_mm.split("-"))
    first = date(year, month, 1)
    last = first + relativedelta(months=1) - relativedelta(days=1)
    return str(first), str(last)


def _last_month():
    """Helper to return start_date and end_date of the previous month as yyyy-mm-dd"""
    today = date.today()
    d = today - relativedelta(months=1)
    return _month(d.isoformat()[:7])


def _this_month():
    """Helper to return start_date of the current month as yyyy-mm-dd.
    No end_date needed."""
    today = date.today()
    return _month(today.isoformat()[:7])[0]


def main():
    cli.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {pypistats.__version__}"
    )
    args = cli.parse_args()
    if args.subcommand is None:
        cli.print_help()
    else:

        # Convert yyyy-mm to yyyy-mm-dd
        if hasattr(args, "start_date") and args.start_date:
            try:
                # yyyy-mm
                args.start_date, _ = _month(args.start_date)
            except ValueError:
                # yyyy-mm-dd
                pass

        # Convert yyyy-mm to yyyy-mm-dd
        if hasattr(args, "end_date") and args.end_date:
            try:
                # yyyy-mm
                _, args.end_date = _month(args.end_date)
            except ValueError:
                # yyyy-mm-dd
                pass

        if hasattr(args, "month") and args.month:
            args.start_date, args.end_date = _month(args.month)
        elif hasattr(args, "last_month") and args.last_month:
            args.start_date, args.end_date = _last_month()
        elif hasattr(args, "this_month") and args.this_month:
            args.start_date = _this_month()

        args.format = _define_format(args)

        args.func(args)


if __name__ == "__main__":
    main()
