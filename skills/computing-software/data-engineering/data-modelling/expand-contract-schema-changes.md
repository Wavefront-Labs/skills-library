---
id: computing-software.data-engineering.data-modelling.expand-contract-schema-changes
name: expand-contract-schema-changes
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, schema-migration, expand-contract, parallel-change, breaking-changes, column-rename, zero-downtime-migration, dual-write, deprecation]
level: advanced
status: docs-checked
description: "Make breaking schema changes safely with expand-contract: renames, type changes and splits, dual-writing and backfill, tracking consumers, then contracting."
sources:
  - https://martinfowler.com/bliki/ParallelChange.html
  - https://docs.getdbt.com/docs/collaborate/govern/model-versions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Expand-contract for breaking schema changes

**Goal:** rename a column, change a type, split a table, or change grain while every reader and writer keeps working throughout.

## The three phases
1. **Expand:** add the new structure alongside the old. Nothing is removed.
2. **Migrate:** write both (or derive one from the other), backfill history, move consumers one by one to the new structure.
3. **Contract:** when no consumer uses the old structure, remove it.

## Example: rename `cust_no` -> `customer_id` and change type to BIGINT
```sql
-- Expand
alter table orders add column customer_id bigint;
-- Migrate: writers populate both (app change), or a trigger/derivation during transition
update orders set customer_id = cast(cust_no as bigint) where customer_id is null;   -- backfill in batches
-- views for readers that can't change yet keep the old name working
create or replace view orders_v1 as select *, cust_no as customer_no_legacy from orders;
-- Contract (weeks later, after verification)
alter table orders drop column cust_no;
```

## In analytics layers
- dbt model versions: publish `fct_orders` v2 with the new column; keep v1 with a `deprecation_date`; consumers pin `ref('fct_orders', v=1)` until they migrate.
- Views as compatibility shims over the new tables.
- Streaming: new topic version (`orders.v2`) produced in parallel, consumers switch, old topic retired.

## Tracking consumers
- The warehouse's query or access history shows who still reads the old column.
- Exposures/lineage in dbt and catalogs list known downstream assets.
- Announce timelines; contract only when usage reaches zero (or an agreed cutoff with sign-off).

## Gotchas
- Backfill large tables in batches to avoid locks and long transactions.
- During migrate, the two columns can diverge if any writer updates only one: add a reconciliation check (`where customer_id <> cast(cust_no as bigint)`).
- Constraints (NOT NULL on the new column) are added only after backfill completes.

## Verify
- [ ] Reconciliation check returns zero rows throughout the migrate phase.
- [ ] Access history shows no reads of the old column for the agreed period before contract.

## Checked

2026-10-28. Confirmed: Fowler's Parallel Change page (expand, migrate, contract) and the dbt model versions page (`deprecation_date` introduced in dbt 1.6, `ref('model', v=1)`). Removed: named Snowflake and BigQuery history views (not in the cited pages).

Method: documentation only; no commands were run.
