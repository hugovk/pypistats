# Release Checklist

* [ ] Get master to the appropriate code release state. [Travis CI](https://travis-ci.org/hugovk/pypistats) and [Azure Pipelines](https://dev.azure.com/hugovk/hugovk/_build/latest?definitionId=1?branchName=master) should be running cleanly for all merges to master. [![Build Status](https://travis-ci.org/hugovk/pypistats.svg?branch=master)](https://travis-ci.org/hugovk/pypistats) [![Build Status](https://dev.azure.com/hugovk/hugovk/_apis/build/status/hugovk.pypistats?branchName=master)](https://dev.azure.com/hugovk/hugovk/_build/latest?definitionId=1?branchName=master)

* [ ] Tag with the version number:
```bash
git tag -a 0.1.0 -m "Release 0.1.0"
```

* [ ] Push tag:
 ```bash
git push --tags
```

* [ ] Create new GitHub release: https://github.com/hugovk/pypistats/releases/new
  * Tag: Pick existing tag "0.1.0"
  * Title: "Release 0.1.0"

* [ ] Check the tagged [Travis CI build](https://travis-ci.org/hugovk/pypistats) has deployed to [PyPI](https://pypi.org/project/pypistats/#history)

* [ ] Check installation:
```bash
pip3 uninstall -y pypistats && pip3 install -U pypistats
```
