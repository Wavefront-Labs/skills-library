---
id: computing-software.qa-testing-engineering.test-automation.database-seeding-and-reset-between-tests
name: database-seeding-and-reset-between-tests
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [database-seeding, database-reset, test-isolation, test-data-management, transaction-rollback, truncate, transactional-tests]
level: practitioner
status: docs-checked
description: "Keep database tests isolated: transaction per test, template-database copies, yield-fixture teardown, and random-order runs to expose leaked state."
sources:
  - https://docs.djangoproject.com/en/stable/topics/testing/overview/
  - https://www.postgresql.org/docs/current/manage-ag-templatedbs.html
  - https://docs.pytest.org/en/stable/how-to/fixtures.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Database seeding and reset between tests

**Goal:** every test starts from a known state, fast, including under parallel runs.

## Strategies (fastest first)
1. **Transaction per test**: open a transaction in setup and roll it back in teardown. Django's `django.test.TestCase` runs each test inside a transaction to provide isolation. In pytest, put teardown after the `yield` of a fixture; pytest runs that code in reverse fixture order once the test finishes.
```python
@pytest.fixture
def db_session(engine):
    conn = engine.connect(); tx = conn.begin()
    session = Session(bind=conn)
    yield session
    session.close(); tx.rollback(); conn.close()
```
Expect this to fail when the code under test commits on its own connection, uses several connections, or the test drives a separate server process (E2E).

2. **Truncate or flush**: empty the tables after each test or spec (Django's alternative to the transaction is flushing the database). Generate the table list from the schema and exclude migration and reference tables.

3. **Template database (PostgreSQL)**: build and seed one database once, then copy it with `CREATE DATABASE new_name TEMPLATE source_db;` (or `createdb -T source_db new_name`). Limits from the manual: no other sessions may be connected to the source database while it is copied, and `CREATE DATABASE` fails if any other connection exists when it starts. The manual says this is not intended as a general-purpose "COPY DATABASE" facility. A database can be marked as a template with `datistemplate`; if unset, only superusers and the owner can clone it.

4. **Snapshot/restore**: container image or volume snapshot with seeded data for large datasets.

## Seeding
- Keep seed scripts idempotent and versioned with migrations.
- Separate reference data (always present) from scenario data (per test via factories or API).
- Be aware of Django: data loaded in migrations is available in `TestCase` tests but not in `TransactionTestCase` tests; `serialized_rollback = True` reloads it per test but slows the suite by approximately 3x.
- E2E: seed through an API or global setup, not the UI.

## Parallel runs
- Django states that properly isolated tests can run in parallel with `test --parallel` for a speed-up on multi-core hardware.
- Use one database per worker or unique data per test so tests never collide.

## Gotchas
- A test run that passes only in a specific order has leaked state. Django's runner can randomise or reverse order inside groups with `--shuffle` and `--reverse` to expose dependencies.
- Plain `unittest.TestCase` avoids the transaction cost but, if it touches the database, results vary with execution order (Django docs).
- Django destroys test databases after the run unless `--keepdb` is used.

## Verify
Running the suite twice in a row and in shuffled order gives identical results.

## Checked
2026-11-09: checked against the Django testing overview (TestCase transaction, TransactionTestCase, serialized_rollback and the 3x figure, --shuffle, --reverse, --parallel, --keepdb, unittest.TestCase order dependence), the PostgreSQL template databases chapter in full (TEMPLATE copy, no-other-connections rule, datistemplate, createdb -T) and the pytest fixtures page (yield teardown and reverse order). Removed as not stated by the sources: the SQLAlchemy `join_transaction_mode` argument, `TRUNCATE ... RESTART IDENTITY CASCADE`, `INSERT ... ON CONFLICT`, the `PYTEST_XDIST_WORKER` naming, the claim that sequences are not rolled back, and `cy.task`. Code sample is illustrative.

Method: documentation only; no commands were run.
