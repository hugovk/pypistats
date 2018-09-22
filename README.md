# pypistats

[![Build Status](https://travis-ci.org/hugovk/pypistats.svg?branch=master)](https://travis-ci.org/hugovk/pypistats)
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

Return values are the JSON responses documented in the API: 
https://pypistats.org/api/

```python
import pypistats
from pprint import pprint

# Initialise the API
api = pypistats.PyPiStats()

# Call the API
print(api.recent("pillow"))
print(api.recent("pillow", "day", output="table"))
pprint(api.recent("pillow", "week", output="json"))
print(api.recent("pillow", "month"))

print(api.overall("pillow"))
print(api.overall("pillow", mirrors=True, output="table"))
pprint(api.overall("pillow", mirrors=False, output="json"))

print(api.python_major("pillow"))
print(api.python_major("pillow", version=2, output="table"))
pprint(api.python_major("pillow", version="3", output="json"))

print(api.python_minor("pillow"))
print(api.python_minor("pillow", version=2.7, output="table"))
pprint(api.python_minor("pillow", version="3.7", output="json"))

print(api.system("pillow"))
print(api.system("pillow", os="darwin", output="table"))
pprint(api.system("pillow", os="linux", output="json"))
```
