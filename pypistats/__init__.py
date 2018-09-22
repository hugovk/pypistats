#!/usr/bin/env python3
# encoding: utf-8
"""
Python interface to PyPI Stats API
https://pypistats.org/api
"""
import requests
import pytablewriter

from . import version

__version__ = version.__version__


class PyPiStats(object):
    """Python interface to PyPI Stats API"""

    def __init__(self):
        self.base_url = "https://pypistats.org/api/"

    def pypi_stats_api(self, endpoint, params=None, output="table"):
        """Call the API and return JSON"""
        if params:
            params = "?" + params
        else:
            params = ""
        url = self.base_url + endpoint + params

        r = requests.get(url)

        if r.status_code != 200:
            return None

        if output == "json":
            return r.json()

        data = r.json()["data"]
        return self._tabulate(data)

    def _tabulate(self, data):
        writer = pytablewriter.MarkdownTableWriter()
        writer.margin = 1

        if isinstance(data, dict):
            writer.header_list = list(data.keys())
            writer.value_matrix = [data]
        elif isinstance(data, list):
            writer.header_list = list(set().union(*(d.keys() for d in data)))
            writer.value_matrix = data

        return writer.dumps()

    def _paramify(self, param_name, param_value):
        """If param_value, append &param_name=param_value to params"""
        if isinstance(param_value, bool):
            param_value = str(param_value).lower()

        if param_value:
            return "&" + param_name + "=" + str(param_value)

        return ""

    def recent(self, package, period=None, **kwargs):
        """Retrieve the aggregate download quantities for the last day/week/month"""
        endpoint = f"packages/{package}/recent"

        params = self._paramify("period", period)
        return self.pypi_stats_api(endpoint, params, **kwargs)

    def overall(self, package, mirrors=None, **kwargs):
        """Retrieve the aggregate daily download time series with or without mirror
        downloads"""
        endpoint = f"packages/{package}/overall"
        params = self._paramify("mirrors", mirrors)
        return self.pypi_stats_api(endpoint, params, **kwargs)

    def python_major(self, package, version=None, **kwargs):
        """Retrieve the aggregate daily download time series by Python major version
        number"""
        endpoint = f"packages/{package}/python_major"
        params = self._paramify("version", version)
        return self.pypi_stats_api(endpoint, params, **kwargs)

    def python_minor(self, package, version=None, **kwargs):
        """Retrieve the aggregate daily download time series by Python minor version
        number"""
        endpoint = f"packages/{package}/python_minor"
        params = self._paramify("version", version)
        return self.pypi_stats_api(endpoint, params, **kwargs)

    def system(self, package, os=None, **kwargs):
        """Retrieve the aggregate daily download time series by operating system"""
        endpoint = f"packages/{package}/system"
        params = self._paramify("os", os)
        return self.pypi_stats_api(endpoint, params, **kwargs)
