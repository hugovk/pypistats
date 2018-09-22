#!/usr/bin/env python3
from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

version_dict = {}
with open("pypistats/version.py") as f:
    exec(f.read(), version_dict)
    version = version_dict["__version__"]

setup(
    name="pypistats",
    version=version,
    description="Python interface to PyPI Stats API https://pypistats.org/api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="hugovk",
    url="https://github.com/hugovk/pypistats",
    packages=["pypistats"],
    install_requires=["requests"],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)

# End of file
