#!/usr/bin/env python3
# encoding: utf-8
"""
CLI with subcommands for pypistats
"""
import argparse
from datetime import date

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
        parser = parent.add_parser(func.__name__, description=func2.__doc__)
        for arg in args:
            parser.add_argument(*arg[0], **arg[1])
        parser.set_defaults(func=func)

    return decorator


arg_start_date = argument("-sd", "--start-date", help="yyyy-mm-dd")
arg_end_date = argument("-ed", "--end-date", help="yyyy-mm-dd")
arg_month = argument("-m", "--month", help="Shortcut for -sd & -ed for a yyyy-mm")
arg_last_month = argument(
    "-l",
    "--last-month",
    help="Shortcut for -sd & -ed for last month",
    action="store_true",
)
arg_json = argument("-j", "--json", action="store_true", help="Output JSON")
arg_daily = argument("-d", "--daily", action="store_true", help="Show daily downloads")


@subcommand(
    [
        argument("package"),
        argument("-p", "--period", choices=("day", "week", "month")),
        argument("-j", "--json", action="store_true", help="Output JSON"),
    ]
)
def recent(args):
    print(
        pypistats.recent(
            args.package, period=args.period, output="json" if args.json else "table"
        )
    )


@subcommand(
    [
        argument("package"),
        argument("--mirrors", choices=("true", "false", "with", "without")),
        arg_start_date,
        arg_end_date,
        arg_month,
        arg_last_month,
        arg_json,
        arg_daily,
    ]
)
def overall(args):
    if args.mirrors in ["with", "without"]:
        args.mirrors = args.mirrors == "with"
    print(
        pypistats.overall(
            args.package,
            mirrors=args.mirrors,
            start_date=args.start_date,
            end_date=args.end_date,
            output="json" if args.json else "table",
            total=False if args.daily else True,
        )
    )


@subcommand(
    [
        argument("package"),
        argument("-v", "--version", help="eg. 2 or 3"),
        arg_start_date,
        arg_end_date,
        arg_month,
        arg_last_month,
        arg_json,
        arg_daily,
    ]
)
def python_major(args):
    print(
        pypistats.python_major(
            args.package,
            version=args.version,
            start_date=args.start_date,
            end_date=args.end_date,
            output="json" if args.json else "table",
            total=False if args.daily else True,
        )
    )


@subcommand(
    [
        argument("package"),
        argument("-v", "--version", help="eg. 2.7 or 3.6"),
        arg_start_date,
        arg_end_date,
        arg_month,
        arg_last_month,
        arg_json,
        arg_daily,
    ]
)
def python_minor(args):

    print(
        pypistats.python_minor(
            args.package,
            version=args.version,
            start_date=args.start_date,
            end_date=args.end_date,
            output="json" if args.json else "table",
            total=False if args.daily else True,
        )
    )


@subcommand(
    [
        argument("package"),
        argument("-o", "--os", help="eg. windows, linux, darwin or other"),
        arg_start_date,
        arg_end_date,
        arg_month,
        arg_last_month,
        arg_json,
        arg_daily,
    ]
)
def system(args):
    print(
        pypistats.system(
            args.package,
            os=args.os,
            start_date=args.start_date,
            end_date=args.end_date,
            output="json" if args.json else "table",
            total=False if args.daily else True,
        )
    )


def _month(yyyy_mm):
    """Helper to return start_date and end_date of a month as yyyy-mm-dd"""
    year, month = map(int, yyyy_mm.split("-"))
    first = date(year, month, 1)
    last = date(year, month + 1, 1) - relativedelta(days=1)
    return str(first), str(last)


def _last_month():
    """Helper to return start_date and end_date of the previous month as yyyy-mm-dd"""
    today = date.today()
    d = today - relativedelta(months=1)
    return _month(d.isoformat()[:7])


def main():
    cli.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {pypistats.__version__}"
    )
    args = cli.parse_args()
    if args.subcommand is None:
        cli.print_help()
    else:
        if hasattr(args, "month") and args.month:
            args.start_date, args.end_date = _month(args.month)
        if hasattr(args, "last_month") and args.last_month:
            args.start_date, args.end_date = _last_month()

        args.func(args)


if __name__ == "__main__":
    main()
