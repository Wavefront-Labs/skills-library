---
id: computing-software.data-engineering.snowflake.data-retention-and-storage-cost
name: data-retention-and-storage-cost
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, data-retention-time, time-travel-storage, fail-safe-bytes, transient-tables, table-storage-metrics, storage-cost, max-data-extension-time, cost-control]
level: practitioner
status: docs-checked
description: "Set Snowflake time-travel retention per object, understand time-travel and fail-safe storage cost, use transient tables for rebuildable data, find storage hogs."
sources:
  - https://docs.snowflake.com/en/user-guide/data-time-travel#specifying-the-data-retention-period-for-an-object
  - https://docs.snowflake.com/en/user-guide/tables-storage-considerations
  - https://docs.snowflake.com/en/sql-reference/info-schema/table_storage_metrics
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data retention and storage cost

**Goal:** enough history to recover from mistakes on important tables, without paying for weeks of churn on tables you rebuild daily.

## Set retention at the right level
```sql
alter account set data_retention_time_in_days = 1;                 -- the default maximum is 1 day
alter database analytics set data_retention_time_in_days = 7;
alter schema raw.critical set data_retention_time_in_days = 30;    -- Enterprise Edition or higher: up to 90
alter table analytics.fct_orders set data_retention_time_in_days = 14;
```
Objects created in a database or schema inherit its retention unless set explicitly; changing the account or schema value changes every child without an explicit value. `MIN_DATA_RETENTION_TIME_IN_DAYS` (set by ACCOUNTADMIN at account level) enforces a floor: the effective period is the larger of it and `DATA_RETENTION_TIME_IN_DAYS`. A value of 0 turns Time Travel off for that object.

## Where storage goes
Storage is charged whether data is Active, in Time Travel or in Fail-safe. Changed or deleted micro-partitions stay in Time Travel for the retention period, then move to Fail-safe (7 days for permanent tables; transient and temporary tables have none). A table fully rebuilt daily (`create or replace` / `insert overwrite`) with a long retention therefore keeps a copy of every rebuild for that whole period. Loading with INSERT, COPY or Snowpipe also adds some Time Travel and Fail-safe bytes through micro-partition defragmentation.
```sql
select table_catalog, table_schema, table_name,
       active_bytes/1e9 as active_gb, time_travel_bytes/1e9 as tt_gb,
       failsafe_bytes/1e9 as fs_gb, retained_for_clone_bytes/1e9 as clone_gb
from snowflake.account_usage.table_storage_metrics
order by time_travel_bytes + failsafe_bytes desc limit 20;
```

## Transient tables for rebuildable data
```sql
create transient table staging.stg_events (...);       -- Time Travel 0 or 1 day, no Fail-safe
create transient schema scratch;                         -- all tables inside transient
```
Good for staging layers, models fully rebuilt from sources, temp ETL tables. Not for anything you can't regenerate. The Snowflake docs advise keeping high-churn dimension tables permanent and relying on Time Travel and Fail-safe, since storage is inexpensive and such tables usually hold a modest share of total storage; find them with the `failsafe_bytes / active_bytes` ratio.

## Clones and retained bytes
Zero-copy clones share micro-partitions; storage a table owns that is retained only because clones still reference it shows in `retained_for_clone_bytes` and is billed to that table. Drop stale dev/CI clones.

## Verify
- [ ] Top-20 storage tables reviewed: high TT/FS bytes on rebuildable tables -> made transient or retention lowered.
- [ ] Critical raw tables have retention >= incident detection time.

## Checked
2026-11-09. Confirmed against the Snowflake docs "Understanding and viewing Fail-safe / Time Travel" (retention levels, inheritance, 0 to 90 days, Enterprise Edition, MIN_DATA_RETENTION_TIME_IN_DAYS, 7 days Fail-safe), "Storage considerations for tables" (transient and temporary tables, high-churn guidance, defragmentation bytes, clones), the TABLE_STORAGE_METRICS information-schema page (byte columns) and the Account Usage overview (the view exists there). Removed: the MAX_DATA_EXTENSION_TIME_IN_DAYS default of 14, the dbt-snowflake transient default, the `deleted = false` filter (the DELETED column is a timestamp), and the "~30 copies" figure.
Method: documentation only; no commands were run.
