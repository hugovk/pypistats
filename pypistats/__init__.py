#!/usr/bin/env python3
# encoding: utf-8
"""
Python interface to PyPI Stats API
https://pypistats.org/api
"""
import pytablewriter
import requests

from . import version

__version__ = version.__version__

BASE_URL = "https://pypistats.org/api/"


def pypi_stats_api(
    endpoint, params=None, output="table", start_date=None, end_date=None
):
    """Call the API and return JSON"""
    if params:
        params = "?" + params
    else:
        params = ""
    url = BASE_URL + endpoint + params

    r = requests.get(url)

    if r.status_code != 200:
        return None

    res = r.json()

    if start_date or end_date:
        res["data"] = _filter(res["data"], start_date, end_date)

    if output == "json":
        return res

    data = res["data"]
    return _tabulate(data)


def _filter(data, start_date, end_date):
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


def _tabulate(data):
    writer = pytablewriter.MarkdownTableWriter()
    writer.margin = 1

    if isinstance(data, dict):
        writer.header_list = list(data.keys())
        writer.value_matrix = [data]
    elif isinstance(data, list):
        writer.header_list = list(set().union(*(d.keys() for d in data)))
        writer.value_matrix = data

    return writer.dumps()


def _paramify(param_name, param_value):
    """If param_value, append &param_name=param_value to params"""
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
