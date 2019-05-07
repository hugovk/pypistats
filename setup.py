#!/usr/bin/env python3
from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()

version_dict = {}
with open("src/pypistats/version.py") as f:
    exec(f.read(), version_dict)
    version = version_dict["__version__"]

setup(
    name="pypistats",
    description="Python interface to PyPI Stats API https://pypistats.org/api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version=version,
    author="hugovk",
    url="https://github.com/hugovk/pypistats",
    license="MIT",
    keywords=["PyPI", "downloads", "statistics", "stats", "BigQuery"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={"console_scripts": ["pypistats = pypistats.cli:main"]},
    zip_safe=True,
    install_requires=[
        "appdirs",
        "pytablewriter[html]>=0.41.2",
        "python-dateutil",
        "python-slugify",
        "requests",
    ],
    tests_require=[
        "black",
        "flake8",
        "freezegun",
        "pytest",
        "pytest-cov",
        "requests_mock",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
