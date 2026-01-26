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
                        [package]

Retrieve the aggregate download quantities for the last 1/7/30 days, excluding
downloads from mirrors

positional arguments:
  package               package name, or dir to check pyproject.toml/setup.cfg
                        (default: .)

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
│ 5,537,706 │ 225,816,599 │ 58,094,476 │
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
                              [-m yyyy-mm|name] [-l] [-t] [-d] [--monthly] [-s SORT]
                              [-c {yes,no,auto}] [-v]
                              [package]

Retrieve the aggregate daily download time series by Python minor version number

positional arguments:
  package               package name, or dir to check pyproject.toml/setup.cfg
                        (default: .)

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
  -s, --sort SORT       Column to sort by (for example: downloads, date, category)
                        (default: downloads)
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
│ 3.12     │  29.56% │  70,503,800 │
│ 3.11     │  20.43% │  48,711,283 │
│ 3.10     │  14.74% │  35,149,431 │
│ 3.13     │  10.35% │  24,680,814 │
│ 3.9      │   8.24% │  19,640,729 │
│ 3.7      │   5.27% │  12,565,151 │
│ 3.8      │   3.45% │   8,231,134 │
│ null     │   3.24% │   7,734,467 │
│ 3.14     │   2.17% │   5,170,747 │
│ 3.6      │   1.85% │   4,406,662 │
│ 2.7      │   0.70% │   1,658,402 │
│ 3.5      │   0.01% │      19,506 │
│ 3.15     │   0.00% │       5,946 │
│ 3.4      │   0.00% │         866 │
│ 3.3      │   0.00% │          20 │
│ 3.2      │   0.00% │           1 │
│ Total    │         │ 238,478,959 │
└──────────┴─────────┴─────────────┘

Date range: 2025-12-01 - 2025-12-31
```

<!-- [[[end]]] -->

You can format in Markdown, ready for pasting in GitHub issues and PRs:

<!-- [[[cog run("pypistats python_minor pillow --last-month --format md", with_console=False) ]]] -->

| category | percent |   downloads |
| :------- | ------: | ----------: |
| 3.12     |  29.56% |  70,503,800 |
| 3.11     |  20.43% |  48,711,283 |
| 3.10     |  14.74% |  35,149,431 |
| 3.13     |  10.35% |  24,680,814 |
| 3.9      |   8.24% |  19,640,729 |
| 3.7      |   5.27% |  12,565,151 |
| 3.8      |   3.45% |   8,231,134 |
| null     |   3.24% |   7,734,467 |
| 3.14     |   2.17% |   5,170,747 |
| 3.6      |   1.85% |   4,406,662 |
| 2.7      |   0.70% |   1,658,402 |
| 3.5      |   0.01% |      19,506 |
| 3.15     |   0.00% |       5,946 |
| 3.4      |   0.00% |         866 |
| 3.3      |   0.00% |          20 |
| 3.2      |   0.00% |           1 |
| Total    |         | 238,478,959 |

Date range: 2025-12-01 - 2025-12-31

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
│    1,852 │     51,264 │    15,494 │
└──────────┴────────────┴───────────┘
```

<!-- [[[end]]] -->

<!-- [[[cog run("pypistats recent ../Pillow") ]]] -->

```console
$ pypistats recent ../Pillow
┌───────────┬─────────────┬────────────┐
│  last_day │  last_month │  last_week │
├───────────┼─────────────┼────────────┤
│ 5,537,706 │ 225,816,599 │ 58,094,476 │
└───────────┴─────────────┴────────────┘
```

<!-- [[[end]]] -->

The default is to sort by downloads. To sort chronologically, use `--sort date` with
`--daily` or `--monthly`:

<!-- [[[cog run("pypistats python_minor pillow --daily --last-month --sort date --version 3.14") ]]] -->

```console
$ pypistats python_minor pillow --daily --last-month --sort date --version 3.14
┌──────────┬────────────┬─────────┬───────────┐
│ category │    date    │ percent │ downloads │
├──────────┼────────────┼─────────┼───────────┤
│ 3.14     │ 2025-12-01 │   3.49% │   180,367 │
│ 3.14     │ 2025-12-02 │   4.08% │   210,894 │
│ 3.14     │ 2025-12-03 │   4.69% │   242,353 │
│ 3.14     │ 2025-12-04 │   3.98% │   205,681 │
│ 3.14     │ 2025-12-05 │   3.48% │   180,197 │
│ 3.14     │ 2025-12-06 │   2.50% │   129,155 │
│ 3.14     │ 2025-12-07 │   2.70% │   139,725 │
│ 3.14     │ 2025-12-08 │   4.19% │   216,851 │
│ 3.14     │ 2025-12-09 │   4.05% │   209,185 │
│ 3.14     │ 2025-12-10 │   4.20% │   217,293 │
│ 3.14     │ 2025-12-11 │   3.86% │   199,779 │
│ 3.14     │ 2025-12-12 │   3.20% │   165,700 │
│ 3.14     │ 2025-12-13 │   2.06% │   106,376 │
│ 3.14     │ 2025-12-14 │   2.40% │   124,187 │
│ 3.14     │ 2025-12-15 │   4.21% │   217,575 │
│ 3.14     │ 2025-12-16 │   3.91% │   202,199 │
│ 3.14     │ 2025-12-17 │   3.99% │   206,452 │
│ 3.14     │ 2025-12-18 │   3.80% │   196,669 │
│ 3.14     │ 2025-12-19 │   3.30% │   170,654 │
│ 3.14     │ 2025-12-20 │   2.17% │   112,086 │
│ 3.14     │ 2025-12-21 │   2.06% │   106,316 │
│ 3.14     │ 2025-12-22 │   3.01% │   155,770 │
│ 3.14     │ 2025-12-23 │   3.38% │   174,706 │
│ 3.14     │ 2025-12-24 │   2.57% │   132,813 │
│ 3.14     │ 2025-12-25 │   2.34% │   121,021 │
│ 3.14     │ 2025-12-26 │   2.23% │   115,560 │
│ 3.14     │ 2025-12-27 │   1.86% │    96,206 │
│ 3.14     │ 2025-12-28 │   2.06% │   106,483 │
│ 3.14     │ 2025-12-29 │   2.73% │   141,272 │
│ 3.14     │ 2025-12-30 │   4.09% │   211,290 │
│ 3.14     │ 2025-12-31 │   3.40% │   175,932 │
│ Total    │            │         │ 5,170,747 │
└──────────┴────────────┴─────────┴───────────┘

Date range: 2025-12-01 - 2025-12-31
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
