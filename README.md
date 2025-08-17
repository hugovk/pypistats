# pypistats

[![PyPI version](https://img.shields.io/pypi/v/pypistats.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/pypistats/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/pypistats.svg?logo=python&logoColor=FFE873)](https://pypi.org/project/pypistats/)
[![PyPI downloads](https://img.shields.io/pypi/dm/pypistats.svg)](https://pypistats.org/packages/pypistats)
[![Azure Pipelines status](https://dev.azure.com/hugovk/hugovk/_apis/build/status/hugovk.pypistats?branchName=main)](https://dev.azure.com/hugovk/hugovk/_build?definitionId=1)
[![GitHub Actions status](https://github.com/hugovk/pypistats/workflows/Test/badge.svg)](https://github.com/hugovk/pypistats/actions)
[![Codecov](https://codecov.io/gh/hugovk/pypistats/branch/main/graph/badge.svg)](https://codecov.io/gh/hugovk/pypistats)
[![Licence](https://img.shields.io/github/license/hugovk/pypistats.svg)](LICENSE.txt)
[![DOI](https://zenodo.org/badge/149862343.svg)](https://zenodo.org/badge/latestdoi/149862343)
[![Code style: Black](https://img.shields.io/badge/code%20style-Black-000000.svg)](https://github.com/psf/black)

Python interface to [PyPI Stats API](https://pypistats.org/api) to get aggregate
download statistics on Python packages on the Python Package Index without having to
execute queries directly against Google BigQuery.

Data is available for the [last 180 days](https://pypistats.org/about#data). (For longer
time periods, [pypinfo](https://github.com/ofek/pypinfo) can help, you'll need an API
key and get free quota.)

## Installation

### From PyPI

```bash
python3 -m pip install --upgrade pypistats
```

### From source

```bash
git clone https://github.com/hugovk/pypistats
cd pypistats
python3 -m pip install .
```

## Example command-line use

Run `pypistats` with a subcommand (corresponding to
[PyPI Stats endpoints](https://pypistats.org/api/#endpoints)), then options for that
subcommand.

Top-level help:

<!-- [[[cog
from scripts.run_command import run
run("pypistats --help")
]]] -->

```console
$ pypistats --help
usage: pypistats [-h] [-V] {recent,overall,python_major,python_minor,system} ...

positional arguments:
  {recent,overall,python_major,python_minor,system}

options:
  -h, --help            show this help message and exit
  -V, --version         show program's version number and exit
```

<!-- [[[end]]] -->

Help for a subcommand:

<!-- [[[cog run("pypistats recent --help") ]]] -->

```console
$ pypistats recent --help
usage: pypistats recent [-h] [-p {day,week,month}]
                        [-f {html,json,pretty,md,markdown,rst,tsv}] [-j] [-v]
                        package

Retrieve the aggregate download quantities for the last 1/7/30 days,
excluding downloads from mirrors

positional arguments:
  package               package name, or dir to check pyproject.toml/setup.cfg (default: .)

options:
  -h, --help            show this help message and exit
  -p, --period {day,week,month}
  -f, --format {html,json,pretty,md,markdown,rst,tsv}
                        The format of output (default: pretty)
  -j, --json            Shortcut for "-f json" (default: False)
  -v, --verbose         Print debug messages to stderr (default: False)
```

<!-- [[[end]]] -->

Get recent downloads:

<!-- [[[cog run("pypistats recent pillow") ]]] -->

```console
$ pypistats recent pillow
┌───────────┬─────────────┬────────────┐
│  last_day │  last_month │  last_week │
├───────────┼─────────────┼────────────┤
│ 7,099,431 │ 184,980,272 │ 43,134,813 │
└───────────┴─────────────┴────────────┘
```

<!-- [[[end]]] -->

Help for another subcommand:

<!-- [[[cog run("pypistats python_minor --help") ]]] -->

```console
$ pypistats python_minor --help
usage: pypistats python_minor [-h] [-V VERSION]
                              [-f {html,json,pretty,md,markdown,rst,tsv}] [-j]
                              [-sd yyyy-mm[-dd]|name] [-ed yyyy-mm[-dd]|name]
                              [-m yyyy-mm|name] [-l] [-t] [-d] [--monthly]
                              [-c {yes,no,auto}] [-v]
                              package

Retrieve the aggregate daily download time series by Python minor version number

positional arguments:
  package               package name, or dir to check pyproject.toml/setup.cfg (default: .)

options:
  -h, --help            show this help message and exit
  -V, --version VERSION
                        eg. 2.7 or 3.6 (default: None)
  -f, --format {html,json,pretty,md,markdown,rst,tsv}
                        The format of output (default: pretty)
  -j, --json            Shortcut for "-f json" (default: False)
  -sd, --start-date yyyy-mm[-dd]|name
                        Start date (default: None)
  -ed, --end-date yyyy-mm[-dd]|name
                        End date (default: None)
  -m, --month yyyy-mm|name
                        Shortcut for -sd & -ed for a single month (default: None)
  -l, --last-month      Shortcut for -sd & -ed for last month (default: False)
  -t, --this-month      Shortcut for -sd for this month (default: False)
  -d, --daily           Show daily downloads (default: False)
  --monthly             Show monthly downloads (default: False)
  -c, --color {yes,no,auto}
                        Color terminal output (default: auto)
  -v, --verbose         Print debug messages to stderr (default: False)
```

<!-- [[[end]]] -->

Get version downloads:

<!-- [[[cog run("pypistats python_minor pillow --last-month") ]]] -->

```console
$ pypistats python_minor pillow --last-month
┌──────────┬─────────┬─────────────┐
│ category │ percent │   downloads │
├──────────┼─────────┼─────────────┤
│ 3.11     │  21.79% │  39,303,874 │
│ 3.12     │  18.85% │  34,005,926 │
│ 3.10     │  16.91% │  30,503,181 │
│ 3.9      │  12.22% │  22,039,674 │
│ 3.7      │   9.35% │  16,857,870 │
│ 3.13     │   8.24% │  14,866,029 │
│ 3.8      │   5.47% │   9,860,598 │
│ null     │   4.99% │   9,003,488 │
│ 3.6      │   1.86% │   3,360,527 │
│ 2.7      │   0.30% │     550,163 │
│ 3.14     │   0.01% │      19,461 │
│ 3.5      │   0.01% │      17,119 │
│ 3.4      │   0.00% │         579 │
│ 3.15     │   0.00% │         398 │
│ 2.6      │   0.00% │          20 │
│ 3.3      │   0.00% │          19 │
│ 3.1      │   0.00% │           1 │
│ Total    │         │ 180,388,927 │
└──────────┴─────────┴─────────────┘

Date range: 2025-07-01 - 2025-07-31
```

<!-- [[[end]]] -->

You can format in Markdown, ready for pasting in GitHub issues and PRs:

<!-- [[[cog run("pypistats python_minor pillow --last-month --format md", with_console=False) ]]] -->

| category | percent |   downloads |
| :------- | ------: | ----------: |
| 3.11     |  21.79% |  39,303,874 |
| 3.12     |  18.85% |  34,005,926 |
| 3.10     |  16.91% |  30,503,181 |
| 3.9      |  12.22% |  22,039,674 |
| 3.7      |   9.35% |  16,857,870 |
| 3.13     |   8.24% |  14,866,029 |
| 3.8      |   5.47% |   9,860,598 |
| null     |   4.99% |   9,003,488 |
| 3.6      |   1.86% |   3,360,527 |
| 2.7      |   0.30% |     550,163 |
| 3.14     |   0.01% |      19,461 |
| 3.5      |   0.01% |      17,119 |
| 3.4      |   0.00% |         579 |
| 3.15     |   0.00% |         398 |
| 2.6      |   0.00% |          20 |
| 3.3      |   0.00% |          19 |
| 3.1      |   0.00% |           1 |
| Total    |         | 180,388,927 |

Date range: 2025-07-01 - 2025-07-31

<!-- [[[end]]] -->

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

Alternatively, use a local path as the package to look up the name from `pyproject.toml`
or `setup.cfg`:

<!-- [[[cog run("pypistats recent .") ]]] -->

```console
$ pypistats recent .
┌──────────┬────────────┬───────────┐
│ last_day │ last_month │ last_week │
├──────────┼────────────┼───────────┤
│    1,557 │     75,440 │     8,864 │
└──────────┴────────────┴───────────┘
```

<!-- [[[end]]] -->

<!-- [[[cog run("pypistats recent ../Pillow") ]]] -->

```console
$ pypistats recent ../Pillow
┌───────────┬─────────────┬────────────┐
│  last_day │  last_month │  last_week │
├───────────┼─────────────┼────────────┤
│ 7,099,431 │ 184,980,272 │ 43,134,813 │
└───────────┴─────────────┴────────────┘
```

<!-- [[[end]]] -->

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
numpy_array = pypistats.overall("pyvista", total="daily", format="numpy")
print(type(numpy_array))
# <class 'numpy.ndarray'>
print(numpy_array)
#[['with_mirrors' '2025-04-09' '1.40%' 40033]
# ['without_mirrors' '2025-04-09' '1.39%' 39906]
# ['with_mirrors' '2025-04-07' '1.36%' 39014]
# ...
# ['with_mirrors' '2025-01-18' '0.17%' 4827]
# ['without_mirrors' '2025-01-18' '0.17%' 4795]
# ['Total' None None 2869617]]
```

Or in a pandas DataFrame:

```python
import pypistats
pandas_dataframe = pypistats.overall("pyvista", total="daily", format="pandas")
print(type(pandas_dataframe))
# <class 'pandas.core.frame.DataFrame'>
print(pandas_dataframe)
#             category        date percent  downloads
# 0       with_mirrors  2025-04-09   1.40%      40033
# 1    without_mirrors  2025-04-09   1.39%      39906
# 2       with_mirrors  2025-04-07   1.36%      39014
# 3    without_mirrors  2025-04-07   1.35%      38837
# 4       with_mirrors  2025-04-06   1.08%      30988
# ..               ...         ...     ...        ...
# 358     with_mirrors  2024-12-28   0.17%       5011
# 359  without_mirrors  2024-12-28   0.17%       4987
# 360     with_mirrors  2025-01-18   0.17%       4827
# 361  without_mirrors  2025-01-18   0.17%       4795
# 362            Total        None    None    2869617
#
# [363 rows x 4 columns]
```

For example, create charts with pandas:

```python
# Show overall downloads over time, excluding mirrors
import pypistats
data = pypistats.overall("pillow", total="daily", format="pandas")
data = data.groupby("category").get_group("without_mirrors").sort_values("date")

chart = data.plot(x="date", y="downloads", figsize=(10, 2))
chart.figure.show()
chart.figure.savefig("overall.png")  # alternatively
```

![overall.png](example/overall.png)

```python
# Show Python 3 downloads over time
import pypistats
data = pypistats.python_major("pillow", total="daily", format="pandas")
data = data.groupby("category").get_group(3).sort_values("date")

chart = data.plot(x="date", y="downloads", figsize=(10, 2))
chart.figure.show()
chart.figure.savefig("python3.png")  # alternatively
```

![python3.png](example/python3.png)

## See also

Related projects

- https://github.com/ofek/pypinfo
- https://github.com/scivision/pypistats-plots
