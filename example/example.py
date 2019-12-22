#!/usr/bin/env python3
"""
Example use of pypistats
"""
import argparse
from pprint import pprint  # noqa: F401

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
    # print(pypistats.recent("pillow", "day", format="markdown"))
    # pprint(pypistats.recent("pillow", "week", format="json"))
    # print(pypistats.recent("pillow", "month"))

    # print(pypistats.overall("pillow"))
    # print(pypistats.overall("pillow", mirrors=True, format="markdown"))
    # pprint(pypistats.overall("pillow", mirrors=False, format="json"))

    # print(pypistats.python_major("pillow"))
    # print(pypistats.python_major("pillow", version=2, format="markdown"))
    # pprint(pypistats.python_major("pillow", version="3", format="json"))

    # print(pypistats.python_minor("pillow"))
    # print(pypistats.python_minor("pillow", version=2.7, format="markdown"))
    # pprint(pypistats.python_minor("pillow", version="3.7", format="json"))
    # print(
    #     pypistats.python_minor(
    #         "pillow", format="json", start_date="2018-09-20", end_date="2018-09-22"
    #     )
    # )
    # print(
    #     pypistats.python_minor(
    #         "pillow", start_date="2018-08-01", end_date="2018-08-31", total=True
    #     )
    # )

    # print(pypistats.system("pillow"))
    # print(pypistats.system("pillow", os="darwin", format="markdown"))
    # pprint(pypistats.system("pillow", os="linux", format="json"))
