# Release Checklist

* [ ] Get master to the appropriate code release state. [Travis CI](https://travis-ci.org/hugovk/pypistats) should be running cleanly for all merges to master. [![Build Status](https://travis-ci.org/hugovk/pypistats.svg?branch=master)](https://travis-ci.org/hugovk/pypistats)
* [ ] Remove `.dev0` suffix from the version:
```bash
git checkout master
edit pypistats/version.py
```
* [ ] Tag the last commit with the version number:
```bash
git add pypistats/version.py
git commit -m "Release 0.1.0"
git tag -a 0.1.0 -m "Release 0.1.0"
```
* [ ] Create a distribution and release on PyPI:
```bash
pip install -U pip setuptools wheel twine keyring
rm -rf build
python setup.py sdist --format=gztar bdist_wheel
twine check dist/*
twine upload -r pypi dist/pypistats-0.1.0*
```
* [ ] Check installation: `pip install -U pypistats`
* [ ] Push commits and tags:
 ```bash
git push
git push --tags
```
* [ ] Create new GitHub release: https://github.com/hugovk/pypistats/releases/new
  * Tag: Pick existing tag "0.1.0"
  * Title: "Release 0.1.0"
* [ ] Increment version and append `.dev0`:
```bash
git checkout master
edit pypistats/version.py
```
* [ ] Commit and push:
```bash
git add pypistats/version.py
git commit -m "Start new release cycle"
git push
```
