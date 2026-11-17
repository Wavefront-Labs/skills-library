---
id: computing-software.qa-testing-engineering.jest-pytest.pytest-hooks-and-local-plugins
name: pytest-hooks-and-local-plugins
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [pytest, pytest-hooks, pytest-plugins, conftest, pytest-collection-modifyitems, pytest-addoption, python]
level: practitioner
status: verified
description: "Customise pytest with conftest hooks and local plugins: add CLI options, modify collection, attach report data, and package a plugin with an entry point."
sources:
  - https://docs.pytest.org/en/stable/how-to/writing_hook_functions.html
  - https://docs.pytest.org/en/stable/how-to/writing_plugins.html
  - https://docs.pytest.org/en/stable/reference/reference.html#hooks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pytest hooks and local plugins

**Goal:** adapt pytest to your project's conventions without forking or wrapping it.

## Common hooks in conftest.py
```python
import pytest

def pytest_addoption(parser):
    parser.addoption("--env", default="local", choices=["local", "staging"])

def pytest_configure(config):
    config.addinivalue_line("markers", "prod_safe: may run against production")

def pytest_collection_modifyitems(config, items):
    if config.getoption("--env") == "staging":
        skip = pytest.mark.skip(reason="not prod_safe")
        for item in items:
            if "prod_safe" not in item.keywords:
                item.add_marker(skip)
    items.sort(key=lambda i: "slow" in i.keywords)   # run slow tests last

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        item.user_properties.append(("env", item.config.getoption("--env")))
```
Other useful hooks: `pytest_sessionstart/finish`, `pytest_report_header` (print env info), `pytest_runtest_setup`, `pytest_terminal_summary`, `pytest_generate_tests` (dynamic parametrisation).

`junitxml` reads `user_properties` from the teardown report, not the call report, so append to `item.user_properties` (as above) for the value to appear as a `<property>` in the XML. Appending to `rep.user_properties` only changes that one report object (other report consumers can read it).

## conftest scoping
`conftest.py` applies to its directory and below; root conftest for global hooks. `pytest_addoption` only works in the rootdir/initial conftests or plugins: an option defined in `sub/conftest.py` is accepted by `pytest sub` but `pytest . --subopt=y` fails with `unrecognized arguments` (run).

## Packaging a plugin
```toml
[project.entry-points.pytest11]
shop_testing = "shop_testing.plugin"
```
Test plugins with the `pytester` fixture (`pytest_plugins = ["pytester"]`).

## Gotchas
- `hookwrapper=True` hooks must `yield` exactly once (or use `wrapper=True` new-style with `return`).
- Register custom markers (as `pytest_configure` does above) or pytest emits `PytestUnknownMarkWarning` for them; the example's `slow` marker needs the same line.
- Heavy work in collection hooks slows every run, even `--collect-only`.

## Verify
`pytest --help` shows your option (`--env={local,staging}`); `pytest -q -rs --env staging` runs the suite and lists the skips (`--collect-only` still lists the skipped tests as collected and does not show skips). `pytester` (`pytest_plugins = ["pytester"]` in the root conftest, `pytester.runpytest().assert_outcomes(passed=1)`) ran correctly.
