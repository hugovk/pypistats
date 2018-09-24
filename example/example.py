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

    # Call the API
    print(pypistats.recent("pillow"))
    # print(pypistats.recent("pillow", "day", output="table"))
    # pprint(pypistats.recent("pillow", "week", output="json"))
    # print(pypistats.recent("pillow", "month"))

    # print(pypistats.overall("pillow"))
    # print(pypistats.overall("pillow", mirrors=True, output="table"))
    # pprint(pypistats.overall("pillow", mirrors=False, output="json"))

    # print(pypistats.python_major("pillow"))
    # print(pypistats.python_major("pillow", version=2, output="table"))
    # pprint(pypistats.python_major("pillow", version="3", output="json"))

    # print(pypistats.python_minor("pillow"))
    # print(pypistats.python_minor("pillow", version=2.7, output="table"))
    # pprint(pypistats.python_minor("pillow", version="3.7", output="json"))

    # print(pypistats.system("pillow"))
    # print(pypistats.system("pillow", os="darwin", output="table"))
    # pprint(pypistats.system("pillow", os="linux", output="json"))
