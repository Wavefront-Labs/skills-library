---
id: computing-software.qa-testing-engineering.jest-pytest.pytest-factory-as-fixture
name: pytest-factory-as-fixture
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [fixture-factory, pytest-fixtures, factory-as-fixture, test-data, pytest]
level: practitioner
status: verified
description: "Use the factory-as-fixture pattern in pytest: fixtures that return a function to create many configured objects per test, with tracked cleanup in teardown."
sources:
  - https://docs.pytest.org/en/stable/how-to/fixtures.html#factories-as-fixtures
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Factory-as-fixture pattern (pytest)

**Goal:** a test needs several objects with different attributes from the same fixture, plus automatic cleanup.

## Pattern
```python
import pytest

@pytest.fixture
def make_customer(db):
    created = []

    def _make_customer(name="Alice", tier="standard", **overrides):
        customer = db.customers.insert(name=name, tier=tier, **overrides)
        created.append(customer)
        return customer

    yield _make_customer

    for customer in created:            # teardown runs after the test, even on failure
        db.customers.delete(customer.id)


def test_gold_discount_only_for_gold(make_customer, pricing):
    gold = make_customer(tier="gold")
    standard = make_customer(name="Bob")
    assert pricing.discount(gold) == 10
    assert pricing.discount(standard) == 0
```

## Variations
- Factory fixtures can depend on other fixtures (db session, API client, tmp_path) so tests don't have to.
- Compose: `make_order` uses `make_customer` when no customer is passed.
- Scope: keep the factory function-scoped so cleanup is per test; the underlying client can be session-scoped.
- Combine with factory_boy: the fixture wraps `CustomerFactory.create` and records ids for cleanup.

## Versus parametrize
Parametrize runs the test several times with one value each; a factory gives one test several objects.

## Gotchas
- Forgetting to record created objects leaks data between tests.
- Cleanup order matters with foreign keys; delete in reverse (`reversed(created)`).
- If the DB is rolled back per test, cleanup is unnecessary; keep the factory simple.

## Verify
Tests create exactly the objects they need, and a row count check after the suite shows nothing left behind.
