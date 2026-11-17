---
id: computing-software.qa-testing-engineering.jest-pytest.pytest-param-ids-and-marks
name: pytest-param-ids-and-marks
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [pytest-param, pytest-parametrize, test-ids, pytest-marks, xfail]
level: practitioner
status: verified
description: "Make parametrized pytest cases readable and controllable: pytest.param with id and marks (xfail, skip), ids functions, and selecting cases with -k by id."
sources:
  - https://docs.pytest.org/en/stable/how-to/parametrize.html
  - https://docs.pytest.org/en/stable/reference/reference.html#pytest-param
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test ids and pytest.param marks

## pytest.param
```python
import pytest

@pytest.mark.parametrize(
    ("amount", "currency", "expected"),
    [
        pytest.param(10, "GBP", "£10.00", id="gbp-basic"),
        pytest.param(0, "GBP", "£0.00", id="zero"),
        pytest.param(1234.5, "EUR", "€1,234.50", id="eur-thousands"),
        pytest.param(10, "JPY", "¥10", id="jpy-no-decimals",
                     marks=pytest.mark.xfail(reason="BUG-812 JPY decimals", strict=True)),
        pytest.param(10, "BTC", None, id="unsupported",
                     marks=pytest.mark.skipif(sys.platform == "win32", reason="locale data")),
    ],
)
def test_format_money(amount, currency, expected):
    assert format_money(amount, currency) == expected
```
`strict=True` on xfail makes an unexpected pass fail the run, so you notice when the bug is fixed.

## ids for generated data
```python
CASES = load_cases("cases.yaml")
@pytest.mark.parametrize("case", CASES, ids=lambda c: c["name"])
def test_rules(case): ...

@pytest.mark.parametrize("n", [1, 10, 100], ids=lambda n: f"n{n}")
```
Without ids pytest uses the value for simple types (`test_x[10-GBP-£10.00]`, non-ASCII is escaped) and `argname0`, `argname1` for objects.

## Selecting
```bash
pytest -k "gbp-basic or zero"
pytest "tests/test_money.py::test_format_money[eur-thousands]"
pytest --collect-only -q        # check ids
```

## Rules
- Ids are stable names: CI history, flaky tracking and reruns depend on them. Avoid ids containing timestamps or random values.
- Keep ids ASCII and short; unicode in ids is escaped unless the ini option `disable_test_id_escaping_and_forfeit_all_rights_to_community_support` is set (name checked in pytest 9.1.1 source).
- Put a marker on the param, not a skip inside the test body, so reports show the reason.

## Verify
`--collect-only` lists readable ids, xfail cases are strict with a ticket, and single cases can be run by id.
