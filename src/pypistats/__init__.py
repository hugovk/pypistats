#!/usr/bin/env python3
# encoding: utf-8
"""
Python interface to PyPI Stats API
https://pypistats.org/api
"""
import atexit
import json
import sys
from datetime import datetime
from pathlib import Path

import requests
from appdirs import user_cache_dir
from pytablewriter import HtmlTableWriter, MarkdownTableWriter, RstSimpleTableWriter
from pytablewriter.style import Align, Style
from slugify import slugify

from . import version

__version__ = version.__version__

BASE_URL = "https://pypistats.org/api/"
CACHE_DIR = Path(user_cache_dir("pypistats"))


def _print_verbose(verbose, *args, **kwargs):
    """Print if verbose"""
    if verbose:
        _print_stderr(*args, **kwargs)


def _print_stderr(*args, **kwargs):
    """Print to stderr"""
    print(*args, file=sys.stderr, **kwargs)


def _cache_filename(url):
    """yyyy-mm-dd-url-slug.json"""
    today = datetime.utcnow().strftime("%Y-%m-%d")
    slug = slugify(url)
    filename = CACHE_DIR / f"{today}-{slug}.json"

    return filename


def _load_cache(cache_file):
    if not cache_file.exists():
        return {}

    with cache_file.open("r") as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            return {}

    return data


def _save_cache(cache_file, data):
    try:
        if not CACHE_DIR.exists():
            CACHE_DIR.mkdir(parents=True)

        with cache_file.open("w") as f:
            json.dump(data, f)

    except OSError:
        pass


def _clear_cache():
    """Delete old cache files, run as last task"""
    cache_files = CACHE_DIR.glob("**/*.json")
    this_month = datetime.utcnow().strftime("%Y-%m")
    for cache_file in cache_files:
        if not cache_file.name.startswith(this_month):
            cache_file.unlink()


atexit.register(_clear_cache)


def pypi_stats_api(
    endpoint,
    params=None,
    format="markdown",
    start_date=None,
    end_date=None,
    sort=True,
    total="all",
    verbose=False,
):
    """Call the API and return JSON"""
    if params:
        params = "?" + params
    else:
        params = ""
    url = BASE_URL + endpoint.lower() + params
    cache_file = _cache_filename(url)
    _print_verbose(verbose, "API URL:", url)
    _print_verbose(verbose, "Cache file:", cache_file)

    res = {}
    if cache_file.is_file():
        _print_verbose(verbose, "Cache file exists")
        res = _load_cache(cache_file)

    if res == {}:
        # No cache, or couldn't load cache
        r = requests.get(url)

        # Raise if we made a bad request
        # (4XX client error or 5XX server error response)
        _print_verbose(verbose, "HTTP status code:", r.status_code)
        r.raise_for_status()

        res = r.json()

        _save_cache(cache_file, res)

    if start_date or end_date:
        res["data"] = _filter(res["data"], start_date, end_date)

    if total == "monthly":
        res["data"] = _monthly_total(res["data"])
    elif total == "all":
        res["data"] = _total(res["data"])

    if format == "json":
        return json.dumps(res)

    # These only for tables, like markdown and rst
    data = res["data"]
    if sort:
        data = _sort(data)

    data = _percent(data)
    data = _grand_total(data)

    return _tabulate(data, format)


def _filter(data, start_date=None, end_date=None):
    """Only return data with dates between start_date and end_date"""
    temp_data = []
    if start_date:
        for row in data:
            if "date" in row and row["date"] >= start_date:
                temp_data.append(row)
        data = temp_data

    temp_data = []
    if end_date:
        for row in data:
            if "date" in row and row["date"] <= end_date:
                temp_data.append(row)
        data = temp_data

    return data


def _sort(data):
    """Sort by downloads"""

    # Only for lists of dicts, not a single dict
    if isinstance(data, dict):
        return data

    data = sorted(data, key=lambda k: k["downloads"], reverse=True)
    return data


def _monthly_total(data):
    """Sum all downloads per category, by month"""

    totalled = {}
    for row in data:
        category = row["category"]
        downloads = row["downloads"]
        month = row["date"][:7]

        if category in totalled:
            if month in totalled[category]:
                totalled[category][month] += downloads
            else:
                totalled[category][month] = downloads
        else:
            totalled[category] = {month: downloads}

    data = []
    for category, month_downloads in totalled.items():
        for month, downloads in month_downloads.items():
            data.append({"category": category, "date": month, "downloads": downloads})

    return data


def _total(data):
    """Sum all downloads per category, regardless of date"""

    # Only for lists of dicts, not a single dict
    if isinstance(data, dict):
        return data

    totalled = {}
    for row in data:
        try:
            totalled[row["category"]] += row["downloads"]
        except KeyError:
            totalled[row["category"]] = row["downloads"]

    data = []
    for k, v in totalled.items():
        data.append({"category": k, "downloads": v})

    return data


def _grand_total(data):
    """Add a grand total row"""

    # Only for lists of dicts, not a single dict
    if isinstance(data, dict):
        return data

    # No need when there's only one row
    if len(data) == 1:
        return data

    grand_total = sum(row["downloads"] for row in data)
    new_row = {"category": "Total", "downloads": grand_total}
    data.append(new_row)

    return data


def _percent(data):
    """Add a percent column"""

    # Only for lists of dicts, not a single dict
    if isinstance(data, dict):
        return data

    # No need when there's only one row
    if len(data) == 1:
        return data

    grand_total = sum(row["downloads"] for row in data)

    for row in data:
        row["percent"] = "{:.2%}".format(row["downloads"] / grand_total)

    return data


def _tabulate(data, format="markdown"):
    """Return data in specified format"""

    format_writers = {
        "markdown": MarkdownTableWriter,
        "rst": RstSimpleTableWriter,
        "html": HtmlTableWriter,
    }

    writer = format_writers[format]()
    if format != "html":
        writer.margin = 1

    if isinstance(data, dict):
        header_list = list(data.keys())
        writer.value_matrix = [data]
    else:  # isinstance(data, list):
        header_list = sorted(set().union(*(d.keys() for d in data)))
        writer.value_matrix = data

    # Move downloads last
    header_list.append("downloads")
    header_list.remove("downloads")
    writer.header_list = header_list

    # Custom alignment and format
    if header_list[0] in ["last_day", "last_month", "last_week"]:
        # Special case for 'recent'
        writer.style_list = len(header_list) * [Style(thousand_separator=",")]
    else:
        style_list = []

        for item in header_list:
            align = None
            thousand_separator = None
            if item == "percent":
                align = Align.RIGHT
            elif item == "downloads":
                thousand_separator = ","
            style = Style(align=align, thousand_separator=thousand_separator)
            style_list.append(style)

        writer.style_list = style_list

    return writer.dumps()


def _paramify(param_name, param_value):
    """If param_value, return &param_name=param_value"""
    if isinstance(param_value, bool):
        param_value = str(param_value).lower()

    if param_value:
        return "&" + param_name + "=" + str(param_value)

    return ""


def recent(package, period=None, **kwargs):
    """Retrieve the aggregate download quantities for the last day/week/month"""
    endpoint = f"packages/{package}/recent"
    params = _paramify("period", period)
    return pypi_stats_api(endpoint, params, **kwargs)


def overall(package, mirrors=None, **kwargs):
    """Retrieve the aggregate daily download time series with or without mirror
    downloads"""
    endpoint = f"packages/{package}/overall"
    params = _paramify("mirrors", mirrors)
    return pypi_stats_api(endpoint, params, **kwargs)


def python_major(package, version=None, **kwargs):
    """Retrieve the aggregate daily download time series by Python major version
    number"""
    endpoint = f"packages/{package}/python_major"
    params = _paramify("version", version)
    return pypi_stats_api(endpoint, params, **kwargs)


def python_minor(package, version=None, **kwargs):
    """Retrieve the aggregate daily download time series by Python minor version
    number"""
    endpoint = f"packages/{package}/python_minor"
    params = _paramify("version", version)
    return pypi_stats_api(endpoint, params, **kwargs)


def system(package, os=None, **kwargs):
    """Retrieve the aggregate daily download time series by operating system"""
    endpoint = f"packages/{package}/system"
    params = _paramify("os", os)
    return pypi_stats_api(endpoint, params, **kwargs)
