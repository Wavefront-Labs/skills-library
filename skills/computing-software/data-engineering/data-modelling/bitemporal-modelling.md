---
id: computing-software.data-engineering.data-modelling.bitemporal-modelling
name: bitemporal-modelling
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, bitemporal-modelling, valid-time, transaction-time, system-versioning, as-of-queries, restatements, audit]
level: advanced
status: gated
description: "Model data with both valid time (when true in the world) and transaction time (when recorded): table design, corrections without loss, and as-of / as-known-at queries."
sources:
  - https://en.wikipedia.org/wiki/Bitemporal_modeling
  - https://learn.microsoft.com/en-us/sql/relational-databases/tables/temporal-tables
  - https://www.kimballgroup.com/2013/02/design-tip-152-slowly-changing-dimension-types-0-4-5-6-7/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bitemporal modelling

**Goal:** answer both "what was the customer's credit limit on 1 March" and "what did we *believe* on 5 March that the limit was on 1 March", which audits, finance restatements and regulatory reports require.

## Two time axes
- **Valid time** (business/effective time): when the fact is true in reality. `valid_from`, `valid_to`.
- **Transaction time** (system/recorded time): when the row was stored in the database and when it was superseded. `recorded_from`, `recorded_to`.
SCD2 covers only one axis (usually something between the two). Bitemporal keeps both.

## Table design
```sql
create table credit_limit_bt (
  customer_id    varchar not null,
  credit_limit   numeric(18,2) not null,
  valid_from     date not null,
  valid_to       date not null default '9999-12-31',
  recorded_from  timestamp not null default current_timestamp,
  recorded_to    timestamp not null default '9999-12-31 00:00:00',
  primary key (customer_id, valid_from, recorded_from)
);
```
Rules: rows are never updated except to close `recorded_to`; corrections insert new rows.

## Operations
- **New fact:** insert with `valid_from` = effective date, open intervals.
- **Correction of the past** (limit on 1 March was actually 6,000 not 5,000, discovered 10 March):
  1. Close the wrong row's transaction time: `update ... set recorded_to = '2026-03-10 09:00' where <row> and recorded_to = '9999-12-31'`.
  2. Insert the corrected row(s) with the same valid interval and `recorded_from = '2026-03-10 09:00'`.
  If the correction splits a valid interval, insert multiple rows covering the pieces.

## Queries
(Ran on DuckDB 1.5: after the 10 March correction the current-belief query returns 6000 and the as-known-at 5 March query returns 5000.)
```sql
-- current belief about valid time X
select * from credit_limit_bt
where customer_id = 'C1' and date '2026-03-01' >= valid_from and date '2026-03-01' < valid_to
  and recorded_to = '9999-12-31';

-- as known at T about valid time X (what a report produced on 5 March would have shown)
select * from credit_limit_bt
where customer_id = 'C1'
  and date '2026-03-01' >= valid_from and date '2026-03-01' < valid_to
  and timestamp '2026-03-05 00:00' >= recorded_from and timestamp '2026-03-05 00:00' < recorded_to;
```

## Platform support
- SQL Server / Azure SQL / MariaDB system-versioned temporal tables provide transaction time automatically (`FOR SYSTEM_TIME AS OF`); you add valid-time columns yourself (gated: unconfirmed, source is paywalled or blocked).
- Delta/Iceberg/Snowflake Time Travel (not run here (gated: unconfirmed, source is paywalled or blocked)) give transaction-time snapshots for limited retention: not a substitute for long-term bitemporal history.
- In dbt: snapshots approximate transaction time (`dbt_valid_from` = load time with check strategy); add source valid-time columns for the other axis.

## Gotchas
- Interval convention: use half-open `[from, to)` on both axes and enforce no overlaps per key within the same transaction-time slice.
- Fact tables referencing bitemporal dimensions must decide which axis they join on (usually valid time with current belief, or as-known-at the report date for reproducibility).
- Storage grows with corrections; that is the point (audit), but index/cluster on `(customer_id, valid_from)`.

## Verify
- [ ] Reproduce an old report exactly using as-known-at queries.
- [ ] Constraint test: no overlapping valid intervals per key among current-belief rows.
