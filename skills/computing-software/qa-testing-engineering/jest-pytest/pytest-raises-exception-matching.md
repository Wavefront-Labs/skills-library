---
id: computing-software.qa-testing-engineering.jest-pytest.pytest-raises-exception-matching
name: pytest-raises-exception-matching
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [pytest-raises, exception-testing, excinfo, exceptiongroup]
level: practitioner
status: verified
description: "Test exceptions with pytest.raises: match regex, inspect excinfo, check notes and causes, ExceptionGroup with RaisesGroup, and avoid over-broad try blocks."
sources:
  - https://docs.pytest.org/en/stable/how-to/assert.html#assertions-about-expected-exceptions
  - https://docs.pytest.org/en/stable/reference/reference.html#pytest-raises
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pytest.raises and exception matching

```python
def test_invalid_amount():
    with pytest.raises(ValueError, match=r"amount must be >= 0, got -1"):
        charge(-1)
```
`match` is `re.search` against `str(exc)`; escape special chars (`re.escape(msg)`) when matching literal text.

## Inspect the exception
```python
with pytest.raises(HTTPError) as excinfo:
    client.get("/missing")
assert excinfo.value.response.status_code == 404
assert excinfo.type is HTTPError
assert isinstance(excinfo.value.__cause__, TimeoutError)   # raise ... from ...
assert "retry" in excinfo.value.__notes__[0]               # add_note (3.11+)
```
`excinfo.match(r"...")` after the block; `excinfo.group_contains(ValueError)` for exception groups (works on pytest 9.1.1; the version that added it was not confirmed).

## Tight blocks
Only the call expected to raise goes inside the `with`:
```python
order = make_order()           # outside: if this raises, the test errors clearly
with pytest.raises(StockError):
    order.ship()
```

## Tuples and subclasses
`pytest.raises((KeyError, IndexError))`. Subclasses match: `pytest.raises(Exception)` passes for almost anything: too broad.

## ExceptionGroup (`pytest.RaisesGroup` added in pytest 8.4.0)
```python
with pytest.RaisesGroup(ValueError, TypeError):
    run_tasks()
```

## Parametrized expectations
```python
@pytest.mark.parametrize("x,expectation", [
    (1, contextlib.nullcontext(2)),
    (0, pytest.raises(ZeroDivisionError)),
])
def test_div(x, expectation):
    with expectation as e:
        assert 2 / x == e
```

## Gotchas
- Code after the raising line inside the `with` never runs; asserts placed there are silently skipped.
- `pytest.raises(..., match=)` checks the message, which is fragile across versions; prefer attributes when available.

## Verify
Temporarily remove the raise in the code: the test fails with "DID NOT RAISE".
