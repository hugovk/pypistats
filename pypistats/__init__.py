#!/usr/bin/env python3
# encoding: utf-8
"""
Python interface to PyPI Stats API
https://pypistats.org/api
"""
import requests

from . import version

__version__ = version.__version__


class PyPiStats(object):
    """Python interface to PyPI Stats API"""

    def __init__(self):
        self.base_url = "https://pypistats.org/api/"

    def pypi_stats_api(self, endpoint, params=None):
        """Call the API and return JSON"""
        if params:
            params = "?" + params
        else:
            params = ""
        url = self.base_url + endpoint + params
        print(url)

        r = requests.get(url)

        if (r.status_code) == 200:
            return r.json()

        return None

    def _paramify(self, params, param_name, param_value):
        """If param_value, append &param_name=param_value to params"""
        if isinstance(param_value, bool):
            param_value = str(param_value).lower()

        if param_value:
            params += "&" + param_name + "=" + str(param_value)

        return params

    def recent(self, package, period=None):
        """Retrieve the aggregate download quantities for the last day/week/month"""
        endpoint = f"packages/{package}/recent"
        params = self._paramify("", "period", period)
        return self.pypi_stats_api(endpoint, params)

    def overall(self, package, mirrors=None):
        """Retrieve the aggregate daily download time series with or without mirror
        downloads"""
        endpoint = f"packages/{package}/overall"
        params = self._paramify("", "mirrors", mirrors)
        return self.pypi_stats_api(endpoint, params)

    def python_major(self, package, version=None):
        """Retrieve the aggregate daily download time series by Python major version
        number"""
        endpoint = f"packages/{package}/python_major"
        params = self._paramify("", "version", version)
        return self.pypi_stats_api(endpoint, params)

    def python_minor(self, package, version=None):
        """Retrieve the aggregate daily download time series by Python minor version
        number"""
        endpoint = f"packages/{package}/python_minor"
        params = self._paramify("", "version", version)
        return self.pypi_stats_api(endpoint, params)

    def system(self, package, os=None):
        """Retrieve the aggregate daily download time series by operating system"""
        endpoint = f"packages/{package}/system"
        params = self._paramify("", "os", os)
        return self.pypi_stats_api(endpoint, params)


if __name__ == "__main__":
    import argparse
    from pprint import pprint

    parser = argparse.ArgumentParser(
        description="Python interface for NYPL's What's on The Menu API.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    args = parser.parse_args()

    # TODO output JSON or table

    # Example use

    # Initialise the API
    api = PyPiStats()

    # Call the API
    pprint(api.recent("pillow"))
    # pprint(api.recent("pillow", "day"))
    # pprint(api.recent("pillow", "week"))
    # pprint(api.recent("pillow", "month"))

    # pprint(api.overall("pillow"))
    # pprint(api.overall("pillow", mirrors=True))
    # pprint(api.overall("pillow", mirrors=False))

    # pprint(api.python_major("pillow"))
    # pprint(api.python_major("pillow", version=2))
    # pprint(api.python_major("pillow", version="3"))

    # pprint(api.python_minor("pillow"))
    # pprint(api.python_minor("pillow", version=2.7))
    # pprint(api.python_minor("pillow", version="3.7"))

    # pprint(api.system("pillow"))
    # pprint(api.system("pillow", os="darwin"))
    # pprint(api.system("pillow", os="linux"))


# End of file
