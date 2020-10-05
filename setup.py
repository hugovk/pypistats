from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()


def local_scheme(version):
    """Skip the local version (eg. +xyz of 0.6.1.dev4+gdf99fe2)
    to be able to upload to Test PyPI"""
    return ""


setup(
    name="pypistats",
    description="Python interface to PyPI Stats API https://pypistats.org/api",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="hugovk",
    url="https://github.com/hugovk/pypistats",
    project_urls={"Source": "https://github.com/hugovk/pypistats"},
    license="MIT",
    keywords=["PyPI", "downloads", "statistics", "stats", "BigQuery"],
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={"console_scripts": ["pypistats = pypistats.cli:main"]},
    zip_safe=True,
    use_scm_version={"local_scheme": local_scheme},
    setup_requires=["setuptools_scm"],
    install_requires=[
        "appdirs",
        "pytablewriter[html]>=0.48",
        "python-dateutil",
        "python-slugify",
        "requests",
    ],
    extras_require={
        "numpy": ["numpy"],
        "pandas": ["pandas"],
        "tests": ["freezegun", "pytest", "pytest-cov", "requests_mock"],
    },
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
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
