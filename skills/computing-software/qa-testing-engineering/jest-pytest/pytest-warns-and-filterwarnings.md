---
id: computing-software.qa-testing-engineering.jest-pytest.pytest-warns-and-filterwarnings
name: pytest-warns-and-filterwarnings
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [pytest-warns, filterwarnings, deprecation-warnings, recwarn]
level: practitioner
status: verified
description: "Assert warnings with pytest.warns and recwarn, turn warnings into errors with filterwarnings (ini and marker), and manage third-party deprecation noise."
sources:
  - https://docs.pytest.org/en/stable/how-to/capture-warnings.html
  - https://docs.python.org/3/library/warnings.html#the-warnings-filter
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Asserting warnings and filterwarnings

## Assert a warning is emitted
```python
def test_old_api_warns():
    with pytest.warns(DeprecationWarning, match=r"use new_api\(\)"):
        old_api()

def test_collects(recwarn):
    legacy()
    assert len(recwarn) == 1
    w = recwarn.pop(UserWarning)
    assert "slow" in str(w.message)
```
Assert no warning: `with warnings.catch_warnings(): warnings.simplefilter("error"); fn()`.

## Warnings as errors (project policy)
```toml
[tool.pytest.ini_options]
filterwarnings = [
  "error",                                               # every warning fails the test
  "ignore::DeprecationWarning:botocore.*",                # third-party noise by module
  "ignore:.*pkg_resources is deprecated.*:DeprecationWarning",
]
```
Filter format: `action:message-regex:category:module-regex:lineno`. Later entries take precedence over earlier ones.

Per test:
```python
@pytest.mark.filterwarnings("ignore:.*legacy.*:UserWarning")
def test_legacy(): ...
```
CLI: `-W error::DeprecationWarning`.

## Why "error" by default
New deprecations from upgraded dependencies fail the build early, while the fix is small, instead of becoming removals that break production later.

## Summary
Without filters pytest shows a "warnings summary" at the end; `-p no:warnings` disables capture (rarely wise).

## Gotchas
- Message regex matches from the start of the message (`re.match`); use `.*` prefix for substring.
- Warnings emitted at import/collection time are not affected by test-level markers; use ini filters.
- `pytest.warns(None)` was removed; use `warnings.catch_warnings`.

## Verify
Adding a `warnings.warn("x", DeprecationWarning)` in app code fails the suite under the `error` policy.
