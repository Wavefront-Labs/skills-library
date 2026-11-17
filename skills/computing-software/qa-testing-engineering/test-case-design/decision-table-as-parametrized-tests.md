---
id: computing-software.qa-testing-engineering.test-case-design.decision-table-as-parametrized-tests
name: decision-table-as-parametrized-tests
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [decision-table-parametrized-tests, decision-tables, data-driven-testing, parametrize, table-driven-tests]
level: practitioner
status: gated
description: "Implement decision tables as data-driven tests: one row per rule in pytest parametrize, JUnit CsvSource or Jest test.each, with readable ids and expected actions."
sources:
  - https://docs.pytest.org/en/stable/how-to/parametrize.html
  - https://junit.org/junit5/docs/current/user-guide/#writing-tests-parameterized-tests
  - https://jestjs.io/docs/api#testeachtablename-fn-timeout
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Decision tables as parametrised tests

**Goal:** the test code mirrors the decision table, so reviewers can check rules row by row.

## pytest
```python
import pytest
RULES = [
    # id,                     tier,     total,   region,          shipping
    ("R1 bronze small",       "bronze", "49.99", "domestic",      "4.99"),
    ("R2 silver at 50",       "silver", "50.00", "domestic",      "0.00"),
    ("R3 gold under 100",     "gold",   "99.99", "domestic",      "2.99"),
    ("R4 gold at 100",        "gold",   "100.00","domestic",      "0.00"),
    ("R5 any international",  "gold",   "500.00","international", "19.99"),
]
@pytest.mark.parametrize("tier,total,region,expected", [r[1:] for r in RULES], ids=[r[0] for r in RULES])
def test_shipping_rules(tier, total, region, expected):
    assert shipping_cost(tier, Decimal(total), region) == Decimal(expected)
```

## JUnit 5
The Java block below is not run here (no JDK 11+): (gated: unconfirmed, source is paywalled or blocked). The pytest block and the Jest tagged-template `test.each` block were run against stub implementations and passed.
```java
@ParameterizedTest(name = "{0}")
@CsvSource(textBlock = """
    R1 bronze small,    bronze, 49.99,  domestic,      4.99
    R2 silver at 50,    silver, 50.00,  domestic,      0.00
    R5 international,   gold,   500.00, international, 19.99
    """)
void shippingRules(String id, String tier, BigDecimal total, String region, BigDecimal expected) {
    assertEquals(0, expected.compareTo(shipping.cost(tier, total, region)));
}
```
Large tables: `@CsvFileSource(resources = "/shipping-rules.csv", numLinesToSkip = 1)`.

## Jest
```js
test.each`
  id                | tier        | total     | expected
  ${'R1'}           | ${'bronze'} | ${49.99}  | ${4.99}
  ${'R4'}           | ${'gold'}   | ${100}    | ${0}
`('$id: $tier $total -> $expected', ({ tier, total, expected }) => {
  expect(shippingCost(tier, total, 'domestic')).toBe(expected)
})
```

## Practices
- Rule ids in test names match the table, so a failure names the broken rule.
- Keep the table as a CSV shared with the business if they maintain rules.
- Test at the lowest level that evaluates the rule (unit/API), not via UI.

## Gotchas
- Money as floats in parameters creates comparison noise; use strings -> Decimal/BigDecimal.

## Verify
Each decision table column maps to one parameter row; deleting a rule's implementation fails exactly that row.
