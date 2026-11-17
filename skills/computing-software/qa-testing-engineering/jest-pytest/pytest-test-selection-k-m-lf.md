---
id: computing-software.qa-testing-engineering.jest-pytest.pytest-test-selection-k-m-lf
name: pytest-test-selection-k-m-lf
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [pytest-k, pytest-lf, pytest-cli, node-ids, stepwise]
level: practitioner
status: verified
description: "Select and rerun pytest tests efficiently: node ids, -k expressions, -m markers, --lf/--ff, --sw stepwise, -x/--maxfail, --deselect and --collect-only."
sources:
  - https://docs.pytest.org/en/stable/how-to/usage.html
  - https://docs.pytest.org/en/stable/how-to/cache.html
  - https://docs.pytest.org/en/stable/reference/reference.html#command-line-flags
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Selecting tests (-k, -m, --lf, --sw, node ids)

## Node ids
```bash
pytest tests/test_cart.py::TestCheckout::test_pay
pytest "tests/test_fmt.py::test_format[0-NZD]"     # quote parametrized ids
pytest tests/test_cart.py::TestCheckout            # whole class
```

## -k expressions (names, case-insensitive substring)
```bash
pytest -k "checkout and not slow"
pytest -k "NZD or JPY"
```
Matches test names, class/module names, parametrize ids and markers' names on the test (keywords).

## -m markers
```bash
pytest -m "smoke and not integration"
```
Register markers to avoid typos: `markers = ["smoke: fast checks", "integration: needs services"]` and `--strict-markers` in `addopts`.

## Cache-based reruns
```bash
pytest --lf          # last failed only (all tests if none failed; --lfnf=none to run nothing)
pytest --ff          # failed first, then the rest
pytest --sw          # stepwise: stop at first failure; next run resumes from it
pytest --sw-skip     # skip the first failing test, continue
pytest --nf          # new files first
```
Cache lives in `.pytest_cache/`; `--cache-clear` resets. In CI, the cache isn't there between jobs unless you persist it.

## Stop early / exclude
```bash
pytest -x                       # first failure
pytest --maxfail=5
pytest --deselect tests/test_x.py::test_flaky
pytest --ignore=tests/e2e --ignore-glob="*_slow.py"
pytest --collect-only -q        # list ids without running
```

## Gotchas
- `-k` with a parametrized id containing spaces or brackets: quote the whole expression.
- `--lf` works with xdist (`-n 2 --lf` ran only the failures). `--sw` with `-n 2` stopped after the first failure but not in a defined order; use `-n 0` for stepwise runs.
- `--sw-skip` is the short form of `--stepwise-skip`.

## Verify
`pytest --collect-only -q -m smoke | tail -1` shows the expected count; `--strict-markers` fails on unregistered markers.
