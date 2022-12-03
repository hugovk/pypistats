"""
Python interface to PyPI Stats API
https://pypistats.org/api
"""
from __future__ import annotations

import atexit
import datetime as dt
import json
import os
import sys
import warnings
from pathlib import Path

from platformdirs import user_cache_dir
from slugify import slugify
from termcolor import colored

try:
    # Python 3.8+
    import importlib.metadata as importlib_metadata
except ImportError:
    # Python 3.7 and lower
    import importlib_metadata

__version__ = importlib_metadata.version(__name__)

BASE_URL = "https://pypistats.org/api/"
CACHE_DIR = Path(user_cache_dir("pypistats"))
USER_AGENT = f"pypistats/{__version__}"


def _print_verbose(verbose: bool, *args, **kwargs) -> None:
    """Print if verbose"""
    if verbose:
        _print_stderr(*args, **kwargs)


def _print_stderr(*args, **kwargs) -> None:
    """Print to stderr"""
    print(*args, file=sys.stderr, **kwargs)


def _cache_filename(url: str) -> Path:
    """yyyy-mm-dd-url-slug.json"""
    today = dt.datetime.utcnow().strftime("%Y-%m-%d")
    slug = slugify(url)
    filename = CACHE_DIR / f"{today}-{slug}.json"

    return filename


def _load_cache(cache_file: Path) -> dict:
    if not cache_file.exists():
        return {}

    with cache_file.open("r") as f:
        try:
            data = json.load(f)
        except json.decoder.JSONDecodeError:
            return {}

    return data


def _save_cache(cache_file: Path, data) -> None:
    try:
        if not CACHE_DIR.exists():
            CACHE_DIR.mkdir(parents=True)

        with cache_file.open("w") as f:
            json.dump(data, f)

    except OSError:
        pass


def _clear_cache() -> None:
    """Delete old cache files, run as last task"""
    cache_files = CACHE_DIR.glob("**/*.json")
    this_month = dt.datetime.utcnow().strftime("%Y-%m")
    for cache_file in cache_files:
        if not cache_file.name.startswith(this_month):
            cache_file.unlink()


atexit.register(_clear_cache)


def pypi_stats_api(
    endpoint: str,
    params: str | None = None,
    format: str = "pretty",
    start_date: str | None = None,
    end_date: str | None = None,
    sort: bool = True,
    total: str = "all",
    color: str = "yes",
    verbose: bool = False,
):
    """Call the API and return JSON"""
    if format == "md":
        format = "markdown"
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
        import httpx

        r = httpx.get(url, headers={"User-Agent": USER_AGENT})

        # Raise if we made a bad request
        # (4XX client error or 5XX server error response)
        _print_verbose(verbose, "HTTP status code:", r.status_code)
        r.raise_for_status()

        res = r.json()

        _save_cache(cache_file, res)

    # Actual first and last dates of the fetched data
    first, last = _date_range(res["data"])

    # Validate end date
    if end_date and end_date < first:
        raise ValueError(
            f"Requested end date ({end_date}) is before earliest available "
            f"data ({first}), because data is only available for 180 days. "
            "See https://pypistats.org/about#data"
        )

    # Validate start date
    if start_date and start_date < first:
        warnings.warn(
            f"Requested start date ({start_date}) is before earliest available "
            f"data ({first}), because data is only available for 180 days. "
            "See https://pypistats.org/about#data",
            stacklevel=3,
        )

    if start_date or end_date:
        res["data"] = _filter(res["data"], start_date, end_date)

    if start_date:
        first = start_date
    if end_date:
        last = end_date

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

    if (
        color != "no"
        and format in ("markdown", "pretty", "rst", "tsv")
        and _can_do_colour()
    ):
        data = _colourify(data)

    output = _tabulate(data, format)

    if first and format not in ["numpy", "pandas"]:
        return f"{output}\nDate range: {first} - {last}\n"
    else:
        return output


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


def _sort(data: dict | list) -> dict | list:
    """Sort by downloads"""

    # Only for lists of dicts, not a single dict
    if isinstance(data, dict):
        return data

    data = sorted(data, key=lambda k: k["downloads"], reverse=True)
    return data


def _monthly_total(data: list) -> list:
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


def _total(data: dict | list) -> dict | list:
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


def _date_range(data: dict | list) -> tuple[str | None, str | None]:
    """Return the first and last dates in data"""
    try:
        first = data[0]["date"]
        last = data[0]["date"]
    except KeyError:
        # /recent has no dates
        return None, None
    for row in data:
        date = row["date"]
        if date < first:
            first = date
        elif date > last:
            last = date

    return first, last


def _grand_total_value(data: list) -> int:
    """Return the grand total of the data"""

    # For "overall", without_mirrors is a subset of with_mirrors.
    # Only sum with_mirrors.
    if data[0]["category"] in ["with_mirrors", "without_mirrors"]:
        grand_total = sum(
            row["downloads"] for row in data if row["category"] == "with_mirrors"
        )
    else:
        grand_total = sum(row["downloads"] for row in data)

    return grand_total


def _grand_total(data: dict | list) -> dict | list:
    """Add a grand total row"""

    # Only for lists of dicts, not a single dict
    if isinstance(data, dict):
        return data

    # No need when there's only one row
    if len(data) == 1:
        return data

    grand_total = _grand_total_value(data)

    new_row = {"category": "Total", "downloads": grand_total}
    data.append(new_row)

    return data


def _percent(data: dict | list) -> dict | list:
    """Add a percent column"""

    # Only for lists of dicts, not a single dict
    if isinstance(data, dict):
        return data

    # No need when there's only one row
    if len(data) == 1:
        return data

    grand_total = _grand_total_value(data)

    for row in data:
        row["percent"] = "{:.2%}".format(row["downloads"] / grand_total)

    return data


def _can_do_colour() -> bool:
    """Check https://no-color.org env vars and for dumb terminal"""
    if "NO_COLOR" in os.environ:
        return False
    if "FORCE_COLOR" in os.environ:
        return True
    return (
        hasattr(sys.stdout, "isatty")
        and sys.stdout.isatty()
        and os.environ.get("TERM") != "dumb"
    )


def _colourify(data) -> list:
    """Add colour to percentages:
    red: 0% - 5%
    yellow: 6% - 15%
    green: 15% - 100%
    """

    for row in data:
        if "percent" not in row:
            continue
        percent = float(row["percent"].rstrip("%"))
        if percent <= 5:
            colour = "red"
        elif percent <= 15:
            colour = "yellow"
        else:
            colour = "green"
        row["percent"] = colored(row["percent"], colour)
    return data


def _tabulate(data: dict | list, format_: str = "markdown"):
    """Return data in specified format"""

    if isinstance(data, dict):
        headers = list(data.keys())
    else:  # isinstance(data, list):
        headers = sorted(set().union(*(d.keys() for d in data)))

    # Move downloads last
    headers.append("downloads")
    headers.remove("downloads")

    if format_ in ("markdown", "pretty"):
        return _prettytable(headers, data, format_)
    else:
        return _pytablewriter(headers, data, format_)


def _prettytable(headers: list[str], data: dict | list, format_: str) -> str:
    from prettytable import MARKDOWN, SINGLE_BORDER, PrettyTable

    x = PrettyTable()
    if format_ == "markdown":
        x.set_style(MARKDOWN)
    else:
        x.set_style(SINGLE_BORDER)

    if isinstance(data, dict):
        data = [data]
    for header in headers:
        col_data = [row[header] if header in row else "" for row in data]
        x.add_column(header, col_data)
        x.align["last_day"] = "r"
        x.align["last_month"] = "r"
        x.align["last_week"] = "r"
        x.align["category"] = "l"
        x.align["percent"] = "r"
        x.align["downloads"] = "r"
        x.custom_format["last_day"] = lambda f, v: f"{v:,}"
        x.custom_format["last_month"] = lambda f, v: f"{v:,}"
        x.custom_format["last_week"] = lambda f, v: f"{v:,}"
        x.custom_format["downloads"] = lambda f, v: f"{v:,}"

    return x.get_string() + "\n"


def _pytablewriter(headers, data, format_: str):
    from pytablewriter import (
        HtmlTableWriter,
        NumpyTableWriter,
        PandasDataFrameWriter,
        RstSimpleTableWriter,
        String,
        TsvTableWriter,
    )
    from pytablewriter.style import Align, Style, ThousandSeparator

    format_writers = {
        "html": HtmlTableWriter,
        "numpy": NumpyTableWriter,
        "pandas": PandasDataFrameWriter,
        "rst": RstSimpleTableWriter,
        "tsv": TsvTableWriter,
    }

    writer = format_writers[format_]()
    if format_ != "html":
        writer.margin = 1

    if isinstance(data, dict):
        writer.value_matrix = [data]
    else:  # isinstance(data, list):
        writer.value_matrix = data

    writer.headers = headers

    # Custom alignment and format
    if headers[0] in ["last_day", "last_month", "last_week"]:
        # Special case for 'recent'
        writer.column_styles = len(headers) * [Style(thousand_separator=",")]
    else:
        column_styles = []
        type_hints = []

        for header in headers:
            align = Align.AUTO
            thousand_separator = ThousandSeparator.NONE
            type_hint = None
            if header == "percent":
                align = Align.RIGHT
            elif header == "downloads" and (format_ not in ["numpy", "pandas"]):
                thousand_separator = ","
            elif header == "category":
                type_hint = String
            style = Style(align=align, thousand_separator=thousand_separator)
            column_styles.append(style)
            type_hints.append(type_hint)

        writer.column_styles = column_styles
        writer.type_hints = type_hints

    if format_ == "numpy":
        return writer.tabledata.as_dataframe().values
    elif format_ == "pandas":
        return writer.tabledata.as_dataframe()
    return writer.dumps()


def _paramify(param_name: str, param_value: float | str | None) -> str:
    """If param_value, return &param_name=param_value"""
    if isinstance(param_value, bool):
        param_value = str(param_value).lower()

    if param_value:
        return "&" + param_name + "=" + str(param_value)

    return ""


def recent(package: str, period: str | None = None, **kwargs: str):
    """Retrieve the aggregate download quantities for the last day/week/month"""
    endpoint = f"packages/{package}/recent"
    params = _paramify("period", period)
    return pypi_stats_api(endpoint, params, **kwargs)


def overall(package: str, mirrors: bool | str | None = None, **kwargs: str):
    """Retrieve the aggregate daily download time series with or without mirror
    downloads"""
    endpoint = f"packages/{package}/overall"
    params = _paramify("mirrors", mirrors)
    return pypi_stats_api(endpoint, params, **kwargs)


def python_major(package: str, version: str | None = None, **kwargs: str):
    """Retrieve the aggregate daily download time series by Python major version
    number"""
    endpoint = f"packages/{package}/python_major"
    params = _paramify("version", version)
    return pypi_stats_api(endpoint, params, **kwargs)


def python_minor(package: str, version: str | None = None, **kwargs) -> str:
    """Retrieve the aggregate daily download time series by Python minor version
    number"""
    endpoint = f"packages/{package}/python_minor"
    params = _paramify("version", version)
    return pypi_stats_api(endpoint, params, **kwargs)


def system(package: str, os: str | None = None, **kwargs):
    """Retrieve the aggregate daily download time series by operating system"""
    endpoint = f"packages/{package}/system"
    params = _paramify("os", os)
    return pypi_stats_api(endpoint, params, **kwargs)
