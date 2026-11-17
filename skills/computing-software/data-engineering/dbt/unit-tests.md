---
id: computing-software.data-engineering.dbt.unit-tests
name: unit-tests
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-unit-tests, unit-testing, given-expect, mock-inputs, is-incremental-override, transformation-logic, ci-only-tests, unit-test-fixtures]
level: advanced
status: verified
description: "Test dbt model SQL logic with unit tests (1.8+): given/expect fixtures, mocking refs and sources, overriding is_incremental and macros, and running them in CI only."
sources:
  - https://docs.getdbt.com/docs/build/unit-tests
  - https://docs.getdbt.com/reference/resource-properties/unit-tests
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# dbt unit tests

**Goal:** prove a model's transformation logic (CASE rules, date math, window logic, incremental filters) on tiny hand-written inputs before it runs on real data.

Data tests check data after building; unit tests check **logic** with static inputs. Available from dbt 1.8 (docs); the examples below were run on dbt 1.12.6 with dbt-duckdb.

## Define
```yaml
# models/marts/_marts__unit_tests.yml
unit_tests:
  - name: test_order_status_mapping
    model: fct_orders
    given:
      - input: ref('stg_orders')
        rows:
          - {order_id: 1, raw_status: 'SHIPPED_PARTIAL', amount: 10}
          - {order_id: 2, raw_status: null, amount: 5}
      - input: ref('stg_customers')
        rows:
          - {customer_id: 9, segment: 'smb'}
    expect:
      rows:
        - {order_id: 1, status: 'shipped'}
        - {order_id: 2, status: 'unknown'}
```
- Only the columns you list are required in `given`; others are null.
- `expect` compares only listed columns.
- `format: dict` (default), `csv` or `sql` with `rows:` as CSV text/SQL for larger fixtures (inline CSV and SQL ran); `fixture: name` loads a csv/sql file from `tests/fixtures/` (a csv fixture ran). An ephemeral input must use `format: sql`.

## Incremental logic
```yaml
  - name: test_incremental_filter
    model: fct_events
    overrides:
      macros:
        is_incremental: true
    given:
      - input: this                          # the existing target table
        rows: [{event_id: 1, event_ts: '2026-10-14 10:00:00'}]
      - input: ref('stg_events')
        rows:
          - {event_id: 1, event_ts: '2026-10-14 10:00:00'}
          - {event_id: 2, event_ts: '2026-10-15 09:00:00'}
    expect:
      rows: [{event_id: 2}]
```
`overrides` can also set `vars` and `env_vars`.

## Run
```bash
dbt test --select "test_type:unit"
dbt build -s fct_orders          # unit tests run before the model is built
```
Inputs are mocked, but dbt still introspects the relations for column types, so they must exist in the target schema; for an incremental model the model's own relation must exist too (without them: "Not able to get columns for unit test ... because the relation doesn't exist"). In a fresh CI schema, create them cheaply first: `dbt run -s +fct_orders --empty` (builds zero-row relations; it fixed the error here). dbt does not test that the merge/insert was applied to the existing table.

## Practice
- Run unit tests in dev/CI only; exclude in prod jobs (`--exclude-resource-type unit_test`, checked) since logic does not change at runtime.
- Write them for complex logic and bug fixes, not for trivial renames.

## Verify
- [ ] Changing a CASE branch in the model makes the unit test fail with a row diff.
- [ ] CI runs `dbt test -s test_type:unit` on modified models.
