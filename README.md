# pypistats

Python 3.6+ interface to [PyPI Stats API](https://pypistats.org/api).

## Installation

### From source

```bash
git clone https://github.com/hugovk/pypistats
pip install .
```

## Example use

Return values are the JSON responses documented in the API: 
https://pypistats.org/api/

```python
# Initialise the API
api = PyPiStats()

# Call the API
pprint(api.recent("pillow"))
pprint(api.recent("pillow", "day"))
pprint(api.recent("pillow", "week"))
pprint(api.recent("pillow", "month"))

pprint(api.overall("pillow"))
pprint(api.overall("pillow", mirrors=True))
pprint(api.overall("pillow", mirrors=False))

pprint(api.python_major("pillow"))
pprint(api.python_major("pillow", version=2))
pprint(api.python_major("pillow", version="3"))

pprint(api.python_minor("pillow"))
pprint(api.python_minor("pillow", version=2.7))
pprint(api.python_minor("pillow", version="3.7"))

pprint(api.system("pillow"))
pprint(api.system("pillow", os="darwin"))
pprint(api.system("pillow", os="linux"))
```
