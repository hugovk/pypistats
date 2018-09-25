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
    return (list(name_or_flags), kwargs)


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


@subcommand(
    [argument("package"), argument("-p", "--period", choices=("day", "week", "month"))]
)
def recent(args):
    print(pypistats.recent(args.package, period=args.period))


@subcommand(
    [
        argument("package"),
        argument("-m", "--mirrors", choices=("true", "false", "with", "without")),
        argument("-sd", "--start-date", help="yyyy-mm-dd"),
        argument("-ed", "--end-date", help="yyyy-mm-dd"),
        argument("-l", "--last-month", action="store_true"),
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
        )
    )


@subcommand(
    [
        argument("package"),
        argument("-v", "--version", help="e.g. 2 or 3"),
        argument("-sd", "--start-date", help="yyyy-mm-dd"),
        argument("-ed", "--end-date", help="yyyy-mm-dd"),
        argument("-l", "--last-month", action="store_true"),
    ]
)
def python_major(args):
    print(
        pypistats.python_major(
            args.package,
            version=args.version,
            start_date=args.start_date,
            end_date=args.end_date,
        )
    )


@subcommand(
    [
        argument("package"),
        argument("-v", "--version", help="e.g. 2.7 or 3.6"),
        argument("-sd", "--start-date", help="yyyy-mm-dd"),
        argument("-ed", "--end-date", help="yyyy-mm-dd"),
        argument("-l", "--last-month", action="store_true"),
    ]
)
def python_minor(args):
    print(
        pypistats.python_minor(
            args.package,
            version=args.version,
            start_date=args.start_date,
            end_date=args.end_date,
        )
    )


@subcommand(
    [
        argument("package"),
        argument("-o", "--os", help="e.g. windows, linux, darwin or other"),
        argument("-sd", "--start-date", help="yyyy-mm-dd"),
        argument("-ed", "--end-date", help="yyyy-mm-dd"),
        argument("-l", "--last-month", action="store_true"),
    ]
)
def system(args):
    print(
        pypistats.system(
            args.package, os=args.os, start_date=args.start_date, end_date=args.end_date
        )
    )


def _last_month():
    """Helper to return start_date and end_date of the previous month as yyyy-mm-dd"""
    today = date.today()
    d = today - relativedelta(months=1)
    first = date(d.year, d.month, 1)
    last = date(today.year, today.month, 1) - relativedelta(days=1)
    return str(first), str(last)


def main():
    args = cli.parse_args()
    if args.subcommand is None:
        cli.print_help()
    else:
        if args.last_month:
            args.start_date, args.end_date = _last_month()

        args.func(args)


if __name__ == "__main__":
    main()
