# pypistats

[![PyPI version](https://img.shields.io/pypi/v/pypistats.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/pypistats/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/pypistats.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/pypistats/)
[![PyPI downloads](https://img.shields.io/pypi/dm/pypistats.svg)](https://pypistats.org/packages/pypistats)
[![Travis CI status](https://img.shields.io/travis/hugovk/pypistats/master?label=Travis%20CI&logo=travis)](https://travis-ci.org/hugovk/pypistats)
[![Azure Pipelines status](https://dev.azure.com/hugovk/hugovk/_apis/build/status/hugovk.pypistats?branchName=master)](https://dev.azure.com/hugovk/hugovk/_build?definitionId=1)
[![GitHub Actions status](https://github.com/hugovk/pypistats/workflows/Test/badge.svg)](https://github.com/hugovk/pypistats/actions)
[![codecov](https://codecov.io/gh/hugovk/pypistats/branch/master/graph/badge.svg)](https://codecov.io/gh/hugovk/pypistats)
[![GitHub](https://img.shields.io/github/license/hugovk/pypistats.svg)](LICENSE.txt)
[![DOI](https://zenodo.org/badge/149862343.svg)](https://zenodo.org/badge/latestdoi/149862343)
[![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Python 3.6+ interface to [PyPI Stats API](https://pypistats.org/api) to get aggregate
download statistics on Python packages on the Python Package Index without having to
execute queries directly against Google BigQuery.

Data is available for the [last 180 days](https://pypistats.org/about#data). (For longer
time periods, [pypinfo](https://github.com/ofek/pypinfo) can help, you'll need an API
key and get free quota.)

## Installation

### From PyPI

```bash
pip install --upgrade pypistats
```

### From source

```bash
git clone https://github.com/hugovk/pypistats
cd pypistats
pip install .
```

## Example command-line use

Run `pypistats` with a subcommand (corresponding to
[PyPI Stats endpoints](https://pypistats.org/api/#endpoints)), then options for that
subcommand.

Top-level help:

```console
$ pypistats --help
usage: pypistats [-h] [-V]
                 {recent,overall,python_major,python_minor,system} ...

positional arguments:
  {recent,overall,python_major,python_minor,system}

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
```

Help for a subcommand:

```console
$ pypistats recent --help
usage: pypistats recent [-h] [-p {day,week,month}]
                        [-f {json,markdown,rst,html}] [-j] [-v]
                        package

Retrieve the aggregate download quantities for the last day/week/month

positional arguments:
  package

optional arguments:
  -h, --help            show this help message and exit
  -p {day,week,month}, --period {day,week,month}
  -f {json,markdown,rst,html}, --format {json,markdown,rst,html}
                        The format of output (default: markdown)
  -j, --json            Shortcut for "-f json" (default: False)
  -v, --verbose         Print debug messages to stderr (default: False)
```

Get recent downloads:

```console
$ pypistats recent pillow
| last_day | last_month | last_week |
|---------:|-----------:|----------:|
|  280,842 |  7,065,928 | 1,709,689 |
```

Help for another subcommand:

```console
$ pypistats python_minor --help
usage: pypistats python_minor [-h] [-V VERSION] [-f {json,markdown,rst,html}]
                              [-j] [-sd yyyy-mm[-dd]|name]
                              [-ed yyyy-mm[-dd]|name] [-m yyyy-mm|name] [-l]
                              [-t] [-d] [--monthly] [-v]
                              package

Retrieve the aggregate daily download time series by Python minor version
number

positional arguments:
  package

optional arguments:
  -h, --help            show this help message and exit
  -V VERSION, --version VERSION
                        eg. 2.7 or 3.6 (default: None)
  -f {json,markdown,rst,html}, --format {json,markdown,rst,html}
                        The format of output (default: markdown)
  -j, --json            Shortcut for "-f json" (default: False)
  -sd yyyy-mm[-dd]|name, --start-date yyyy-mm[-dd]|name
                        Start date (default: None)
  -ed yyyy-mm[-dd]|name, --end-date yyyy-mm[-dd]|name
                        End date (default: None)
  -m yyyy-mm|name, --month yyyy-mm|name
                        Shortcut for -sd & -ed for a single month (default:
                        None)
  -l, --last-month      Shortcut for -sd & -ed for last month (default: False)
  -t, --this-month      Shortcut for -sd for this month (default: False)
  -d, --daily           Show daily downloads (default: False)
  --monthly             Show monthly downloads (default: False)
  -v, --verbose         Print debug messages to stderr (default: False)
```

Get version downloads:

```console
$ pypistats python_minor pillow --last-month
| category | percent | downloads |
|----------|--------:|----------:|
| 2.7      |  35.94% | 2,189,327 |
| 3.6      |  31.83% | 1,938,870 |
| 3.7      |  18.71% | 1,139,642 |
| 3.5      |  11.29% |   687,782 |
| 3.4      |   1.23% |    74,673 |
| null     |   0.94% |    57,476 |
| 3.8      |   0.04% |     2,147 |
| 2.6      |   0.01% |       826 |
| 3.3      |   0.00% |       212 |
| 3.2      |   0.00% |        28 |
| 2.4      |   0.00% |         6 |
| 3.9      |   0.00% |         5 |
| 2.8      |   0.00% |         1 |
| Total    |         | 6,090,995 |
```

The table is Markdown, ready for pasting in GitHub issues and PRs:

| category | percent | downloads |
| -------- | ------: | --------: |
| 2.7      |  35.94% | 2,189,327 |
| 3.6      |  31.83% | 1,938,870 |
| 3.7      |  18.71% | 1,139,642 |
| 3.5      |  11.29% |   687,782 |
| 3.4      |   1.23% |    74,673 |
| null     |   0.94% |    57,476 |
| 3.8      |   0.04% |     2,147 |
| 2.6      |   0.01% |       826 |
| 3.3      |   0.00% |       212 |
| 3.2      |   0.00% |        28 |
| 2.4      |   0.00% |         6 |
| 3.9      |   0.00% |         5 |
| 2.8      |   0.00% |         1 |
| Total    |         | 6,090,995 |

These are equivalent (in May 2019):

```sh
pypistats python_major pip --last-month
pypistats python_major pip --month april
pypistats python_major pip --month apr
pypistats python_major pip --month 2019-04
```

And:

```sh
pypistats python_major pip --start-date december --end-date january
pypistats python_major pip --start-date dec      --end-date jan
pypistats python_major pip --start-date 2018-12  --end-date 2019-01
```

## Example programmatic use

Return values are from the JSON responses documented in the API:
https://pypistats.org/api/

```python
import pypistats
from pprint import pprint

# Call the API
print(pypistats.recent("pillow"))
print(pypistats.recent("pillow", "day", format="markdown"))
print(pypistats.recent("pillow", "week", format="rst"))
print(pypistats.recent("pillow", "month", format="html"))
pprint(pypistats.recent("pillow", "week", format="json"))
print(pypistats.recent("pillow", "day"))

print(pypistats.overall("pillow"))
print(pypistats.overall("pillow", mirrors=True, format="markdown"))
print(pypistats.overall("pillow", mirrors=False, format="rst"))
print(pypistats.overall("pillow", mirrors=True, format="html"))
pprint(pypistats.overall("pillow", mirrors=False, format="json"))

print(pypistats.python_major("pillow"))
print(pypistats.python_major("pillow", version=2, format="markdown"))
print(pypistats.python_major("pillow", version=3, format="rst"))
print(pypistats.python_major("pillow", version="2", format="html"))
pprint(pypistats.python_major("pillow", version="3", format="json"))

print(pypistats.python_minor("pillow"))
print(pypistats.python_minor("pillow", version=2.7, format="markdown"))
print(pypistats.python_minor("pillow", version="2.7", format="rst"))
print(pypistats.python_minor("pillow", version=3.7, format="html"))
pprint(pypistats.python_minor("pillow", version="3.7", format="json"))

print(pypistats.system("pillow"))
print(pypistats.system("pillow", os="darwin", format="markdown"))
print(pypistats.system("pillow", os="linux", format="rst"))
print(pypistats.system("pillow", os="darwin", format="html"))
pprint(pypistats.system("pillow", os="linux", format="json"))
```

### NumPy and pandas

To use with either NumPy or pandas, make sure they are first installed, or:

```bash
pip install --upgrade "pypistats[numpy]"
pip install --upgrade "pypistats[pandas]"
pip install --upgrade "pypistats[numpy,pandas]"
```

Return data in a NumPy array for further processing:

```python
import pypistats
numpy_array = pypistats.overall("pyvista", total=True, format="numpy")
print(type(numpy_array))
# <class 'numpy.ndarray'>
print(numpy_array)
# [['with_mirrors' '2019-09-20' '2.23%' 1204]
#  ['without_mirrors' '2019-09-20' '2.08%' 1122]
#  ['with_mirrors' '2019-09-19' '0.92%' 496]
#  ...
#  ['with_mirrors' '2019-10-26' '0.02%' 13]
#  ['without_mirrors' '2019-10-26' '0.02%' 12]
#  ['Total' None None 54041]]
```

Or in a pandas DataFrame:

```python
import pypistats
pandas_dataframe = pypistats.overall("pyvista", total=True, format="pandas")
print(type(pandas_dataframe))
# <class 'pandas.core.frame.DataFrame'>
print(pandas_dataframe)
#             category        date percent  downloads
# 0       with_mirrors  2019-09-20   2.23%       1204
# 1    without_mirrors  2019-09-20   2.08%       1122
# 2       with_mirrors  2019-09-19   0.92%        496
# 3       with_mirrors  2019-08-22   0.90%        489
# 4    without_mirrors  2019-09-19   0.86%        466
# ..               ...         ...     ...        ...
# 354  without_mirrors  2019-11-03   0.03%         15
# 355  without_mirrors  2019-11-16   0.03%         15
# 356     with_mirrors  2019-10-26   0.02%         13
# 357  without_mirrors  2019-10-26   0.02%         12
# 358            Total        None    None      54041
#
# [359 rows x 4 columns]
```

For example, create charts with pandas:

```python
# Show overall downloads over time, excluding mirrors
import pypistats
data = pypistats.overall("pillow", total=True, format="pandas")
data = data.groupby("category").get_group("without_mirrors").sort_values("date")

chart = data.plot(x="date", y="downloads", figsize=(10, 2))
chart.figure.show()
chart.figure.savefig("overall.png")  # alternatively
```

![overall.png](example/overall.png)

```python
# Show Python 3 downloads over time
import pypistats
data = pypistats.python_major("pillow", total=True, format="pandas")
data = data.groupby("category").get_group(3).sort_values("date")

chart = data.plot(x="date", y="downloads", figsize=(10, 2))
chart.figure.show()
chart.figure.savefig("python3.png")  # alternatively
```

![python3.png](example/python3.png)
