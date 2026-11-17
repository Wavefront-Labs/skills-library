---
id: computing-software.data-engineering.dbt.singular-tests
name: singular-tests
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-tests, singular-tests, data-tests, business-rule-tests, reconciliation-test, tests-folder, test-severity]
level: practitioner
status: verified
description: "Write dbt singular tests for one-off business rules: a SELECT returning failing rows in tests/, configs in the file, reconciliation checks between models, and naming for triage."
sources:
  - https://docs.getdbt.com/docs/build/data-tests#singular-data-tests
  - https://docs.getdbt.com/reference/data-test-configs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Singular tests

**Goal:** encode a specific business rule or reconciliation as a test that fails when the rule is broken.

## Shape
A singular test is a `.sql` file under `tests/` (the `test-paths` folder) containing a SELECT that returns **failing rows**. Zero rows = pass.
```sql
-- tests/assert_order_totals_match_line_items.sql
{{ config(severity='error', error_if='>0', tags=['finance', 'critical'], store_failures=true) }}
with orders as (
    select order_id, total_amount from {{ ref('fct_orders') }}
    where order_date >= current_date - 7
),
lines as (
    select order_id, sum(quantity * unit_price) as line_total
    from {{ ref('fct_order_lines') }} group by 1
)
select o.order_id, o.total_amount, l.line_total
from orders o left join lines l using (order_id)
where abs(coalesce(l.line_total, 0) - o.total_amount) > 0.01
```
The `ref`s make the test depend on both models; `dbt build` runs it after them.

## Good singular tests
- Cross-model reconciliation (revenue in mart = revenue in source within tolerance).
- Rules involving several columns (`shipped_at >= ordered_at`).
- Aggregate sanity (daily row count not lower than 50% of the 7-day average).
- Known incident regressions: when a bug is fixed, add a test that would have caught it.

## When to make it generic instead
If you would copy the same SQL for a second model, turn it into a custom generic test (parameterised macro).

## Tips
- Name files `assert_<rule>.sql` so failures read like a sentence in CI output.
- Return the columns someone needs to investigate (keys, both values), not `count(*)`.
- Limit to recent partitions where full scans are expensive.
- Document them: a properties file under `tests/` with a top-level `data_tests:` entry per test name and a `description` (the description reached manifest.json on dbt 1.12.6); at minimum, a SQL comment at the top explaining the rule and its owner.

## Verify
- [ ] Deliberately break the rule in dev data: the test fails and stored failures show the offending rows.
- [ ] `dbt ls -s test_type:singular` lists the test.
