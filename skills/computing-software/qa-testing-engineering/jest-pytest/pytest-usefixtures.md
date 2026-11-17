---
id: computing-software.qa-testing-engineering.jest-pytest.pytest-usefixtures
name: pytest-usefixtures
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [usefixtures, pytest-fixtures, pytestmark, side-effect-fixtures]
level: practitioner
status: verified
description: "Apply pytest fixtures that return nothing useful with @pytest.mark.usefixtures, pytestmark and ini usefixtures, and know where usefixtures does not work."
sources:
  - https://docs.pytest.org/en/stable/how-to/fixtures.html#use-fixtures-in-classes-and-modules-with-usefixtures
  - https://docs.pytest.org/en/stable/reference/reference.html#pytest-mark-usefixtures
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# usefixtures and fixture availability

## When
The test needs a fixture's side effect (clean directory, seeded DB, started server) but not its value.

```python
@pytest.mark.usefixtures("cleandir", "seeded_db")
class TestReports:
    def test_export(self): ...
    def test_import(self): ...

# whole module
pytestmark = pytest.mark.usefixtures("seeded_db")

# whole project (pytest.ini / pyproject)
[tool.pytest.ini_options]
usefixtures = ["_freeze_clock"]
```

## usefixtures vs autouse vs argument
| Mechanism | Explicit | Value available |
|---|---|---|
| test argument | yes | yes |
| `usefixtures` | yes (marker) | no |
| `autouse` | no | no (unless also requested) |
Prefer `usefixtures` over autouse when only some tests need the effect: it documents intent at the call site.

## Doesn't work
- On fixtures: applying any mark to a fixture function, including `@pytest.mark.usefixtures`, is an error at collection time in pytest 9 (`Failed: Marks cannot be applied to fixtures`); older versions only warned. Request the dependency as an argument instead.
- `pytest.param(..., marks=pytest.mark.usefixtures(...))` raises `ValueError: pytest.param cannot add pytest.mark.usefixtures`. Put the mark on the test or use `indirect` parametrisation.

## Availability errors
A typo such as `usefixtures("seded_db")` errors at setup with `fixture 'seded_db' not found` and lists available fixtures; usually the conftest defining it is not on the path of the test (sibling directory). Move the fixture up a level or into a plugin.

## Gotchas
- Typos in `usefixtures("seded_db")` error at setup time, good; but string names don't get IDE refactoring support.
- Class-level `usefixtures` applies to every method, including ones that don't need it.

## Verify
`pytest --setup-show tests/test_reports.py` shows `seeded_db` set up and torn down for each test in the class (run).
