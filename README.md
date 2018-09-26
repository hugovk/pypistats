# pypistats

[![Build Status](https://travis-ci.org/hugovk/pypistats.svg?branch=master)](https://travis-ci.org/hugovk/pypistats)
[![codecov](https://codecov.io/gh/hugovk/pypistats/branch/master/graph/badge.svg)](https://codecov.io/gh/hugovk/pypistats)
[![GitHub](https://img.shields.io/github/license/hugovk/pypistats.svg)](LICENSE.txt)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Python 3.6+ interface to [PyPI Stats API](https://pypistats.org/api).

## Installation

### From source

```bash
git clone https://github.com/hugovk/pypistats
cd pypistats
pip install .
```

## Example use

Return values are from the JSON responses documented in the API: 
https://pypistats.org/api/

```python
import pypistats
from pprint import pprint

# Call the API
print(pypistats.recent("pillow"))
print(pypistats.recent("pillow", "day", output="table"))
pprint(pypistats.recent("pillow", "week", output="json"))
print(pypistats.recent("pillow", "month"))

print(pypistats.overall("pillow"))
print(pypistats.overall("pillow", mirrors=True, output="table"))
pprint(pypistats.overall("pillow", mirrors=False, output="json"))

print(pypistats.python_major("pillow"))
print(pypistats.python_major("pillow", version=2, output="table"))
pprint(pypistats.python_major("pillow", version="3", output="json"))

print(pypistats.python_minor("pillow"))
print(pypistats.python_minor("pillow", version=2.7, output="table"))
pprint(pypistats.python_minor("pillow", version="3.7", output="json"))

print(pypistats.system("pillow"))
print(pypistats.system("pillow", os="darwin", output="table"))
pprint(pypistats.system("pillow", os="linux", output="json"))
```
