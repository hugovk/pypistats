#!/usr/bin/env python3
# encoding: utf-8
"""
Example use of pypistats
"""
import argparse
from pprint import pprint  # noqa

import pypistats

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Example use of pypistats",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    args = parser.parse_args()

    # Example use

    # Initialise the API
    api = pypistats.PyPiStats()

    # Call the API
    print(api.recent("pillow"))
    # print(api.recent("pillow", "day", output="table"))
    # pprint(api.recent("pillow", "week", output="json"))
    # print(api.recent("pillow", "month"))

    # print(api.overall("pillow"))
    # print(api.overall("pillow", mirrors=True, output="table"))
    # pprint(api.overall("pillow", mirrors=False, output="json"))

    # print(api.python_major("pillow"))
    # print(api.python_major("pillow", version=2, output="table"))
    # pprint(api.python_major("pillow", version="3", output="json"))

    # print(api.python_minor("pillow"))
    # print(api.python_minor("pillow", version=2.7, output="table"))
    # pprint(api.python_minor("pillow", version="3.7", output="json"))

    # print(api.system("pillow"))
    # print(api.system("pillow", os="darwin", output="table"))
    # pprint(api.system("pillow", os="linux", output="json"))
