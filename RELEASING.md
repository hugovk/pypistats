# Release checklist

- [ ] Get `main` to the appropriate code release state.
      [GitHub Actions](https://github.com/hugovk/pypistats/actions) should be running
      cleanly for all merges to `main`.
      [![GitHub Actions status](https://github.com/hugovk/pypistats/workflows/Test/badge.svg)](https://github.com/hugovk/pypistats/actions)

- [ ] Edit release draft, adjust text if needed:
      https://github.com/hugovk/pypistats/releases

- [ ] Check next tag is correct, amend if needed

- [ ] Publish release

- [ ] Check the tagged
      [GitHub Actions build](https://github.com/hugovk/pypistats/actions/workflows/deploy.yml)
      has deployed to [PyPI](https://pypi.org/project/pypistats/#history)

- [ ] Check installation:

```bash
pip3 uninstall -y pypistats && pip3 install -U pypistats && pypistats --version
```
