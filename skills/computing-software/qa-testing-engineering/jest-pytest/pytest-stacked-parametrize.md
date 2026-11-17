---
id: computing-software.qa-testing-engineering.jest-pytest.pytest-stacked-parametrize
name: pytest-stacked-parametrize
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [stacked-parametrize, parametrize, cartesian-product, pytest-parametrize]
level: practitioner
status: verified
description: "Stack pytest.mark.parametrize decorators for cartesian products, combine with class/module parametrization and fixtures, and control explosion with ids and filters."
sources:
  - https://docs.pytest.org/en/stable/how-to/parametrize.html
  - https://docs.pytest.org/en/stable/example/parametrize.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stacked parametrize and cartesian products

```python
@pytest.mark.parametrize("currency", ["NZD", "USD", "JPY"])
@pytest.mark.parametrize("amount", [0, 1, 999_999])
def test_format(amount, currency):
    assert format_money(amount, currency)
```
Generates 3 x 3 = 9 tests with ids like `test_format[0-NZD]`: the decorator closest to the function supplies the first id part.

## Class and module level
```python
pytestmark = pytest.mark.parametrize("backend", ["sqlite", "postgres"])

@pytest.mark.parametrize("role", ["admin", "viewer"])
class TestPermissions:
    def test_read(self, role, backend): ...
```
Every test in the class/module receives the parameter (must accept it).

## With parametrized fixtures
A parametrized fixture (`@pytest.fixture(params=[...])`) multiplies with direct `parametrize` too. Total = product of all axes: check `pytest --collect-only -q | tail -1` before committing.

## Controlling the explosion
- Use pairwise selection for >3 axes (generate combos with allpairspy and pass as one `parametrize("a,b,c", combos)`).
- Skip invalid combos explicitly:
```python
@pytest.mark.parametrize("os_,browser", [
    pytest.param("mac", "safari"),
    pytest.param("linux", "safari", marks=pytest.mark.skip(reason="no safari on linux")),
])
```
- Or filter in `pytest_generate_tests`/`pytest_collection_modifyitems`.

## Readable ids
`ids=["zero", "one", "max"]` or `ids=lambda v: f"amt{v}"`; ids appear in `-k` selection (`-k "JPY and 0"`).

## Gotchas
- Mutable parameter values (lists, dicts) are shared across generated tests: don't mutate them in tests.
- Stacking with `indirect=True` on one axis applies only to that axis's names.

## Verify
`pytest --collect-only -q` shows the expected count and readable ids.
