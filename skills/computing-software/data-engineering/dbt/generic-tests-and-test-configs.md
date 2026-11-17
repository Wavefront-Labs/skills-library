---
id: computing-software.data-engineering.dbt.generic-tests-and-test-configs
name: generic-tests-and-test-configs
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-tests, generic-tests, store-failures, severity, warn-if, error-if, where-config, limit, relationships, accepted-values, data-tests]
level: practitioner
status: verified
description: "Apply dbt's built-in generic tests well: unique/not_null/accepted_values/relationships, severity with warn_if/error_if thresholds, where filters, store_failures for triage."
sources:
  - https://docs.getdbt.com/docs/build/data-tests
  - https://docs.getdbt.com/reference/data-test-configs
  - https://docs.getdbt.com/reference/resource-configs/store_failures
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Generic tests and test configs

**Goal:** catch broken keys, invalid values and orphans on every build, with thresholds that separate "page someone" from "look tomorrow".

## The four built-ins
```yaml
models:
  - name: fct_orders
    columns:
      - name: order_id
        data_tests: [unique, not_null]                 # `tests:` is the older key
      - name: status
        data_tests:
          - accepted_values:
              arguments: {values: ['placed', 'shipped', 'delivered', 'returned']}   # arguments block: dbt 1.10.5+; older: values directly
      - name: customer_id
        data_tests:
          - relationships:
              arguments: {to: ref('dim_customers'), field: customer_id}
```
Every model's primary key gets `unique` + `not_null` (or `dbt_utils.unique_combination_of_columns` for composite keys). Minimum bar.

## Configs
```yaml
          - relationships:
              arguments: {to: ref('dim_customers'), field: customer_id}
              config:
                severity: error
                error_if: ">100"        # fail only above 100 orphans
                warn_if: ">0"
                where: "order_date >= current_date - 3"   # limit scan / ignore known legacy rows
                store_failures: true      # write failing rows to <schema>_dbt_test__audit
                limit: 1000
                tags: ["critical"]
```
- `severity: warn` makes the test never fail the run; prefer thresholds with `error_if` so a blow-up still fails.
- `where` keeps tests cheap on huge tables (test recent partitions) and excludes accepted legacy issues.
- `store_failures: true` (or `store_failures_as: view|table`) leaves the failing rows queryable: link them in alerts. The default schema is `<target schema>_dbt_test__audit` (`main_dbt_test__audit` here, checked), and each run replaces that test's previous failures.

## Running
```bash
dbt test -s fct_orders
dbt build -s +fct_orders              # tests run after each model; downstream skipped if a test errors
dbt test --select "tag:critical"
dbt test -s test_type:generic
```
In `dbt build`, a failing test with severity error **skips downstream models**, preventing bad data propagation.

## Gotchas
- `accepted_values` on a free-text column becomes noise; use it for real enums.
- `relationships` tests on huge tables are expensive full anti-joins: add `where`.
- Tests on views query the full upstream logic: cost adds up.
- Test names are generated from the args, e.g. `relationships_fct_orders_segment__segment__ref_stg_customers_`.

## Verify
- [ ] Every model has a primary key test (`dbt ls -s "test_type:generic,test_name:unique"` coverage check or `dbt-project-evaluator`).
- [ ] Introducing a duplicate key in dev fails `dbt build` and shows rows in the audit schema.
