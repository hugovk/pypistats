#!/usr/bin/env python3
from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()


def version_scheme(version):
    from setuptools_scm.version import guess_next_dev_version

    version = guess_next_dev_version(version)
    return version.replace("+", ".")


setup(
    name="pypistats",
    description="Python interface to PyPI Stats API https://pypistats.org/api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="hugovk",
    url="https://github.com/hugovk/pypistats",
    license="MIT",
    keywords=["PyPI", "downloads", "statistics", "stats", "BigQuery"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={"console_scripts": ["pypistats = pypistats.cli:main"]},
    zip_safe=True,
    use_scm_version={"version_scheme": version_scheme},
    setup_requires=["setuptools_scm"],
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
