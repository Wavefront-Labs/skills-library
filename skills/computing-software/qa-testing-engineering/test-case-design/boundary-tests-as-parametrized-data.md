---
id: computing-software.qa-testing-engineering.test-case-design.boundary-tests-as-parametrized-data
name: boundary-tests-as-parametrized-data
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [boundary-parametrized-tests, boundary-value-analysis, parametrized-tests, pytest-parametrize, data-driven-testing]
level: practitioner
status: gated
description: "Implement boundary value tests as parametrized data in pytest, Jest and JUnit 5, with readable IDs, derived values and expected results per boundary."
sources:
  - https://docs.pytest.org/en/stable/how-to/parametrize.html
  - https://jestjs.io/docs/api#testeachtablename-fn-timeout
  - https://junit.org/junit5/docs/current/user-guide/#writing-tests-parameterized-tests
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Implementing boundary tests as parametrized data

**Goal:** each boundary value becomes one named, independently reported test case without copy-paste.

## pytest
```python
import pytest
from shop.pricing import shipping_fee

LIMIT = 50_00  # cents, free shipping at >= 50.00

@pytest.mark.parametrize(
    "basket_cents, expected",
    [
        pytest.param(LIMIT - 1, 499, id="just-below-free-limit"),
        pytest.param(LIMIT,     0,   id="at-free-limit"),
        pytest.param(LIMIT + 1, 0,   id="just-above-free-limit"),
        pytest.param(0,         499, id="empty-basket"),
        pytest.param(-1, ValueError, id="invalid-negative"),
    ],
)
def test_shipping_fee_boundaries(basket_cents, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            shipping_fee(basket_cents)
    else:
        assert shipping_fee(basket_cents) == expected
```
Better: split invalid cases into their own test to avoid the `if`.

## Jest
```js
test.each([
  { qty: 0,  ok: false },
  { qty: 1,  ok: true  },
  { qty: 20, ok: true  },
  { qty: 21, ok: false },
])("quantity $qty valid=$ok", ({ qty, ok }) => {
  expect(isValidQuantity(qty)).toBe(ok);
});
```

## JUnit 5
The Java block below is not run here (no JDK 11+): (gated: unconfirmed, source is paywalled or blocked). The pytest block (5 cases, stub implementation) and the Jest `test.each` block (4 cases) were run and passed.
```java
@ParameterizedTest(name = "age {0} -> adult={1}")
@CsvSource({ "17,false", "18,true", "19,true", "120,true", "121,false" })
void adultBoundary(int age, boolean adult) {
    assertEquals(adult, Person.isAdult(age));
}
```

## Practices
- Derive values from named constants (`LIMIT - 1`) so a changed limit updates tests and the intent is visible.
- But keep expected results literal; computing them with the same formula as production repeats its bug.
- IDs state the boundary role (`at-max`, `max-plus-one`) so the report reads as a BVA table.
- Keep valid and invalid boundaries in separate parametrized tests.

## Gotchas
- Floating boundaries: use exact decimal/cents, not 49.99 floats.
- A shared mutable fixture across params leaks state; parametrize data only.

## Verify
The test report lists one line per boundary value with a meaningful ID, and changing the limit constant by one makes the at-limit cases fail.
