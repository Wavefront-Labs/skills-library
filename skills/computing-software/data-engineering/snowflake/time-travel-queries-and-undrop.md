---
id: computing-software.data-engineering.snowflake.time-travel-queries-and-undrop
name: time-travel-queries-and-undrop
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, snowflake-time-travel, at-before, undrop, data-recovery, offset, statement-id, clone-at, fail-safe, incident-recovery]
level: practitioner
status: docs-checked
description: "Recover from bad writes in Snowflake: query AT/BEFORE a timestamp, offset or statement, restore via CLONE or INSERT, UNDROP tables/schemas, and what Fail-safe can and cannot do."
sources:
  - https://docs.snowflake.com/en/user-guide/data-time-travel
  - https://docs.snowflake.com/en/sql-reference/constructs/at-before
  - https://docs.snowflake.com/en/sql-reference/sql/undrop-table
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time Travel queries and UNDROP

**Goal:** after an accidental DELETE/UPDATE/DROP or a bad pipeline run, see and restore the previous state quickly.

## Look back
```sql
select * from analytics.fct_orders at (timestamp => '2026-10-16 08:00:00'::timestamp_ltz);
select * from analytics.fct_orders at (offset => -60*30);                  -- 30 minutes ago
select * from analytics.fct_orders before (statement => '01b2c3d4-0000-...'); -- just before a specific query
```
Find the bad statement's query id in `query_history` (`query_text ilike 'delete from analytics.fct_orders%'`). `BEFORE(statement => ...)` is the most precise restore point.

## Restore options
```sql
-- 1. whole table back (clone as of the earlier point, then swap)
create or replace table analytics.fct_orders_restored clone analytics.fct_orders before (statement => '<query id>');
alter table analytics.fct_orders swap with analytics.fct_orders_restored;
-- 2. only the deleted rows back
insert into analytics.fct_orders
select * from analytics.fct_orders before (statement => '<query id>')
minus select * from analytics.fct_orders;
```

## UNDROP
```sql
show tables history like 'FCT_ORDERS' in schema analytics;   -- lists dropped tables too
undrop table analytics.fct_orders;
undrop schema analytics;      -- UNDROP also supports schemas and databases
```

## Limits
- Retention: `DATA_RETENTION_TIME_IN_DAYS` (default 1; up to 90 on Enterprise). Beyond it, data moves to **Fail-safe** (7 days for permanent tables) where only Snowflake can recover it.
- Transient databases, schemas and tables: retention of 0 or the default of 1 day.

## Verify
- [ ] Practice drill: delete rows in a dev table and restore via `BEFORE(statement => ...)`.
- [ ] Critical tables have retention longer than the time it would take to notice a bad write.

## Checked
2026-10-28. Confirmed against the Snowflake Time Travel page (AT(OFFSET => ...), BEFORE(STATEMENT => ...), DATA_RETENTION_TIME_IN_DAYS default of 1 day and up to 90 days on Enterprise and higher, Fail-safe 7 days where only Snowflake can recover, SHOW TABLES HISTORY, UNDROP TABLE, SCHEMA and DATABASE, transient retention 0 or 1 day) and the access history page (ALTER TABLE ... SWAP WITH). Removed: the COPY GRANTS paragraph, atomic and metadata-only remarks, best-effort Fail-safe wording, temporary-table and no-Fail-safe claims, same-name UNDROP advice and the recreated-table history claim.
Method: documentation only; no commands were run.
