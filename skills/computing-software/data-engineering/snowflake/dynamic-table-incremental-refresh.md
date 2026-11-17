---
id: computing-software.data-engineering.snowflake.dynamic-table-incremental-refresh
name: dynamic-table-incremental-refresh
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, incremental-refresh-mode, dynamic-tables, target-lag, refresh-mode]
level: advanced
status: docs-checked
description: "Get Snowflake dynamic tables to refresh incrementally: REFRESH_MODE, constructs that force full refresh, diagnosing refresh_mode_reason, and lag/cost tuning."
sources:
  - https://docs.snowflake.com/en/user-guide/dynamic-tables-refresh
  - https://docs.snowflake.com/en/user-guide/dynamic-tables-supported-queries
  - https://docs.snowflake.com/en/sql-reference/functions/dynamic_table_refresh_history
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic table incremental refresh

**Goal:** dynamic tables that process only changed data, not full recomputes every lag interval.

## Refresh mode
```sql
CREATE OR REPLACE DYNAMIC TABLE core.daily_sales
  TARGET_LAG = '15 minutes' WAREHOUSE = transform_wh
  REFRESH_MODE = INCREMENTAL          -- AUTO | INCREMENTAL | FULL | ADAPTIVE
  INITIALIZE = ON_CREATE
AS SELECT order_date, store_id, sum(amount) amount FROM raw.orders GROUP BY 1, 2;
```
- Check the resolved mode with `SHOW DYNAMIC TABLES` (`refresh_mode`, `refresh_mode_reason`).

## Diagnose
```sql
SHOW DYNAMIC TABLES LIKE 'DAILY_SALES';   -- refresh_mode, refresh_mode_reason
SELECT name, refresh_action, refresh_trigger, data_timestamp
FROM TABLE(information_schema.dynamic_table_refresh_history(name => 'CORE.DAILY_SALES'))
ORDER BY data_timestamp DESC LIMIT 20;
```
`refresh_action` values include NO_DATA, INCREMENTAL, CUSTOM_INCREMENTAL, FULL and REINITIALIZE (see the function reference).

## Things that block or hurt incremental
- Query constructs that are not incrementalizable (see the supported-queries page and `refresh_mode_reason`).

## Tuning
- Split complex queries into a chain of simpler dynamic tables; each piece can be incremental.
- Intermediate DTs use `TARGET_LAG = DOWNSTREAM` so they refresh only when consumers need them.

## Verify## Verify
Refresh history shows `INCREMENTAL` actions rather than `FULL` or `REINITIALIZE`.

## Checked
2026-10-28. Confirmed against the dynamic table refresh mode page and the DYNAMIC_TABLE_REFRESH_HISTORY reference (REFRESH_MODE values incl. ADAPTIVE, INITIALIZE = ON_CREATE default, SHOW DYNAMIC TABLES refresh_mode and refresh_mode_reason, REFRESH_ACTION and REFRESH_TRIGGER values, downstream target lag). Removed: statistics fields, claims about AUTO resolution and INCREMENTAL creation failure, the list of blockers, re-initialisation and time-window gotchas.
Method: documentation only; no commands were run.
