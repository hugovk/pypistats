# Release Checklist

- [ ] Get master to the appropriate code release state.
      [Travis CI](https://travis-ci.org/hugovk/pypistats) and
      [GitHub Actions](https://github.com/hugovk/pypistats/actions) should be running
      cleanly for all merges to master.
      [![Build Status](https://travis-ci.org/hugovk/pypistats.svg?branch=master)](https://travis-ci.org/hugovk/pypistats)
      [![GitHub Actions status](https://github.com/hugovk/pypistats/workflows/Test/badge.svg)](https://github.com/hugovk/pypistats/actions)

- [ ] Tag with the version number:

```bash
git tag -a 0.1.0 -m "Release 0.1.0"
```

- [ ] Push tag:

```bash
git push --tags
```

- [ ] Create new GitHub release: https://github.com/hugovk/pypistats/releases/new

  - Tag: Pick existing tag "0.1.0"

- [ ] Check the tagged [Travis CI build](https://travis-ci.org/hugovk/pypistats) has
      deployed to [PyPI](https://pypi.org/project/pypistats/#history)

- [ ] Check installation:

```bash
pip3 uninstall -y pypistats && pip3 install -U pypistats
```
