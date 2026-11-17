---
id: computing-software.qa-testing-engineering.jest-pytest.pytest-skip-skipif-xfail
name: pytest-skip-skipif-xfail
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [pytest, xfail, skipif, pytest-markers, skip, strict-xfail, custom-markers, python]
level: practitioner
status: verified
description: "Use pytest skip, skipif and xfail correctly: conditions with reasons, strict xfail for known bugs, importorskip, and registering custom markers with --strict-markers."
sources:
  - https://docs.pytest.org/en/stable/how-to/skipping.html
  - https://docs.pytest.org/en/stable/how-to/mark.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pytest skip, skipif, xfail and custom markers

**Goal:** tests that cannot or should not run are marked honestly with reasons, and known bugs are tracked.

## Skip
```python
import sys, pytest
@pytest.mark.skipif(sys.platform == "win32", reason="uses fork()")
def test_worker_pool(): ...

def test_gpu_path():
    if not has_gpu(): pytest.skip("no GPU on this runner")

np = pytest.importorskip("numpy", minversion="1.26")   # skip module if missing
```

## xfail
```python
@pytest.mark.xfail(reason="PAY-321 rounding bug", strict=True, raises=AssertionError)
def test_rounding_half_even(): ...
```
- `strict=True` (or `xfail_strict = true` in config): an unexpected pass (XPASS) fails the run, prompting removal of the marker when the bug is fixed.
- `raises=` limits the expected failure type; another exception is a real failure.
- `run=False` for tests that crash the interpreter.

## Custom markers
```toml
# pyproject.toml
[tool.pytest.ini_options]
addopts = "--strict-markers"
markers = ["smoke: fast critical checks", "slow: > 5s", "integration: needs docker"]
```
```bash
pytest -m "smoke and not slow"
pytest -rsxX         # report reasons for skipped, xfailed, xpassed
```

## Gotchas
- Without `--strict-markers`, a typo (`@pytest.mark.smoek`) only emits a `PytestUnknownMarkWarning`, the test runs but is never selected by `-m smoke`; with `--strict-markers` collection fails.
- Skips piling up are hidden test debt; review `-rs` output periodically.

## Verify
`pytest -rsxX` shows reasons for every skip/xfail; fixing a bug turns its strict xfail into a failure that reminds you to remove the marker.
