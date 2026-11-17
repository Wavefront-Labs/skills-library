---
id: computing-software.software-engineering.python.pytest-markers-skip-and-xfail
name: pytest-markers-skip-and-xfail
category: computing-software
field: software-engineering
product: python
tags: [python, pytest, pytest-markers, xfail, skipif, test-selection, strict-markers]
level: practitioner
status: verified
description: "Organise and select pytest tests with markers: skip/skipif, strict xfail, registered custom markers, -m and -k expressions, keeping slow tests out of the fast loop."
sources: ["https://docs.pytest.org/en/stable/how-to/mark.html", "https://docs.pytest.org/en/stable/how-to/skipping.html", "https://docs.pytest.org/en/stable/how-to/usage.html#specifying-which-tests-to-run"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pytest markers, skip and xfail

**Goal:** a fast default test run, opt-in slow/integration suites, and honest tracking
of known failures.

## Register custom markers (and make typos fail)
```toml
[tool.pytest.ini_options]
addopts = "--strict-markers -ra"
markers = [
  "slow: takes >1s; deselect with -m 'not slow'",
  "integration: needs docker services",
]
```
`--strict-markers` turns `@pytest.mark.integraton` (typo) into an error instead of a
silently unselected test. `-ra` prints a summary of skips/xfails with reasons.

## Selecting
```bash
pytest -m "not slow and not integration"   # default dev loop
pytest -m integration
pytest -k "parse and not unicode"          # substring match on test names/classes/files
pytest tests/test_api.py::TestAuth::test_expired_token
pytest --lf          # last failed     --ff  failed first     -x  stop on first failure
```

## Skip
```python
import sys, pytest
@pytest.mark.skipif(sys.platform == "win32", reason="uses fork()")
def test_daemonize(): ...

def test_gpu():
    torch = pytest.importorskip("torch")    # skip if optional dependency missing
    if not torch.cuda.is_available():
        pytest.skip("no CUDA device")
```
Module-level: `pytestmark = pytest.mark.integration` (or a list) applies to every test in the file.

## xfail: known bugs, tracked
```python
@pytest.mark.xfail(reason="bug #412: rounding off by one cent", strict=True, raises=AssertionError)
def test_invoice_total(): ...
```
- `strict=True`: when the bug gets fixed and the test passes (XPASS), the run fails, forcing
  removal of the marker. Set globally: `xfail_strict = true` in ini options.
- `raises=` limits the expected failure type, so an unrelated crash still fails.
- Never use xfail for flaky tests; quarantine them separately with an issue link.

## Markers on parametrized cases
```python
@pytest.mark.parametrize("value,expected", [
    ("1", 1),
    pytest.param("1e3", 1000, marks=pytest.mark.xfail(reason="sci notation unsupported")),
    pytest.param("9" * 400, None, marks=pytest.mark.slow, id="huge"),
])
def test_parse(value, expected): ...
```

## Auto-marking by location
```python
# conftest.py
def pytest_collection_modifyitems(config, items):
    for item in items:
        if "tests/integration" in str(item.path):
            item.add_marker(pytest.mark.integration)
```

## Verify
- [ ] `pytest --markers` lists every custom marker; `--strict-markers` in addopts.
- [ ] CI runs both the fast selection and the marked suites; `-ra` output shows no stale skips.
