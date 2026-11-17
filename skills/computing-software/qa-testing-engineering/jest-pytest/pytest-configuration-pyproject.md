---
id: computing-software.qa-testing-engineering.jest-pytest.pytest-configuration-pyproject
name: pytest-configuration-pyproject
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [pytest, pytest-ini, addopts, pyproject-toml, testpaths, pytest-configuration, filterwarnings, python]
level: practitioner
status: verified
description: "Configure pytest in pyproject.toml or pytest.ini: testpaths, addopts, markers, filterwarnings, import mode, pythonpath and how rootdir and config discovery work."
sources:
  - https://docs.pytest.org/en/stable/reference/customize.html
  - https://docs.pytest.org/en/stable/reference/reference.html#ini-options-ref
  - https://docs.pytest.org/en/stable/explanation/pythonpath.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pytest configuration

**Goal:** a project config that makes `pytest` with no arguments do the right thing everywhere.

## pyproject.toml
```toml
[tool.pytest.ini_options]
minversion = "8.0"
testpaths = ["tests"]
addopts = "-ra --strict-markers --strict-config --import-mode=importlib"
pythonpath = ["src"]
markers = ["slow: long-running tests", "integration: needs docker"]
filterwarnings = [
  "error",                                    # warnings fail tests...
  "ignore::DeprecationWarning:thirdparty.*",  # ...except known third-party ones
]
xfail_strict = true
log_cli_level = "INFO"
junit_family = "xunit2"
```

## Discovery and rootdir
- Config file precedence: `pytest.ini` > `pyproject.toml` (with `[tool.pytest.ini_options]`) > `tox.ini` > `setup.cfg`. First found walking up from the common ancestor of args.
- `rootdir` determines node ids and where conftest lookup starts; print it in the header. `-c path` forces a config file. When two files exist, pytest prints `WARNING: ignoring pytest config in ...` in the header (checked: `pytest.ini` beat `pyproject.toml`, which beat `tox.ini` and `setup.cfg`).
- `testpaths` applies only when pytest runs from the rootdir without path arguments; from a subdirectory it collects that directory instead.

## Import modes
- `prepend` (default): inserts test dirs into `sys.path`; duplicate test file basenames in different dirs need `__init__.py`.
- `importlib`: no `sys.path` changes; use `pythonpath` for a src layout. The docs keep `prepend` as the default "for the foreseeable future" and list drawbacks of `importlib`, so choose it deliberately.

## Useful addopts
`-ra` (summary of non-passes), `-x`/`--maxfail=3` locally, `--durations=10` (slowest tests), `-p no:cacheprovider` in read-only CI.

## Gotchas
- `--strict-config` fails on unknown ini keys (catches typos like `testpath`).
- `filterwarnings = error` catches deprecations early but can break on dependency upgrades; maintain ignores.
- Setting `addopts` with `-n auto` makes debugging with `-s` painful; keep it in CI command instead.

## Verify
`pytest --co -q` from the repo root collects the `testpaths` tests; the header shows the expected rootdir and configfile (from a subfolder, collection starts at that folder, not `testpaths`).
