# pypistats

[![PyPI version](https://img.shields.io/pypi/v/pypistats.svg)](https://pypi.org/project/pypistats/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/pypistats.svg)](https://pypi.org/project/pypistats/)
[![PyPI downloads](https://img.shields.io/pypi/dm/pypistats.svg)](https://pypistats.org/packages/pypistats)
[![Build Status](https://travis-ci.org/hugovk/pypistats.svg?branch=master)](https://travis-ci.org/hugovk/pypistats)
[![codecov](https://codecov.io/gh/hugovk/pypistats/branch/master/graph/badge.svg)](https://codecov.io/gh/hugovk/pypistats)
[![GitHub](https://img.shields.io/github/license/hugovk/pypistats.svg)](LICENSE.txt)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Python 3.6+ interface to [PyPI Stats API](https://pypistats.org/api).

## Installation

### From PyPI

```bash
pip install -U pypistats
```

### From source

```bash
git clone https://github.com/hugovk/pypistats
cd pypistats
pip install .
```

## Example command-line use

Run `pypistats` with a subcommand (corresponding to [PyPI Stats endpoints](https://pypistats.org/api/#endpoints)),
then options for that subcommand.

Top-level help:

```console
$ pypistats --help
usage: pypistats [-h] [-v]
                 {recent,overall,python_major,python_minor,system} ...

positional arguments:
  {recent,overall,python_major,python_minor,system}

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
```

Help for a subcommand:

```console
$ pypistats recent --help
usage: pypistats recent [-h] [-p {day,week,month}]
                        [-f {json,markdown,rst,html}] [-j]
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
```

Get recent downloads:

```console
$ pypistats recent pillow
| last_day | last_month | last_week |
|---------:|-----------:|----------:|
|    61877 |    3527341 |    865484 |
```

Help for another subcommand:

```console
$ pypistats python_minor --help
usage: pypistats python_minor [-h] [-v VERSION] [-f {json,markdown,rst,html}]
                              [-j] [-sd yyyy-mm-dd] [-ed yyyy-mm-dd]
                              [-m yyyy-mm] [-l] [-d]
                              package

Retrieve the aggregate daily download time series by Python minor version
number

positional arguments:
  package

optional arguments:
  -h, --help            show this help message and exit
  -v VERSION, --version VERSION
                        eg. 2.7 or 3.6 (default: None)
  -f {json,markdown,rst,html}, --format {json,markdown,rst,html}
                        The format of output (default: markdown)
  -j, --json            Shortcut for "-f json" (default: False)
  -sd yyyy-mm-dd, --start-date yyyy-mm-dd
                        Start date (default: None)
  -ed yyyy-mm-dd, --end-date yyyy-mm-dd
                        End date (default: None)
  -m yyyy-mm, --month yyyy-mm
                        Shortcut for -sd & -ed for a single month (default:
                        None)
  -l, --last-month      Shortcut for -sd & -ed for last month (default: False)
  -d, --daily           Show daily downloads (default: False)
```

Get version downloads:

```console
$ pypistats python_minor pillow --last-month
| category | percent | downloads |
|----------|--------:|----------:|
|      2.7 |  46.64% | 1,512,429 |
|      3.6 |  30.34% |   983,838 |
|      3.5 |  12.53% |   406,429 |
|      3.7 |   6.12% |   198,558 |
|      3.4 |   3.41% |   110,552 |
| null     |   0.84% |    27,380 |
|      3.3 |   0.05% |     1,599 |
|      2.6 |   0.05% |     1,581 |
|      3.2 |   0.01% |       246 |
|      3.8 |   0.00% |       133 |
|      2.4 |   0.00% |         7 |
| Total    |         | 3,242,752 |
```

The table is Markdown, ready for pasting in GitHub issues and PRs:

| category | percent | downloads |
|----------|--------:|----------:|
|      2.7 |  46.64% | 1,512,429 |
|      3.6 |  30.34% |   983,838 |
|      3.5 |  12.53% |   406,429 |
|      3.7 |   6.12% |   198,558 |
|      3.4 |   3.41% |   110,552 |
| null     |   0.84% |    27,380 |
|      3.3 |   0.05% |     1,599 |
|      2.6 |   0.05% |     1,581 |
|      3.2 |   0.01% |       246 |
|      3.8 |   0.00% |       133 |
|      2.4 |   0.00% |         7 |
| Total    |         | 3,242,752 |


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
