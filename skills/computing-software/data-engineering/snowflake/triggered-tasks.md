---
id: computing-software.data-engineering.snowflake.triggered-tasks
name: triggered-tasks
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, triggered-tasks, tasks, streams, event-driven]
level: practitioner
status: docs-checked
description: "Run Snowflake tasks only when a stream has new data using triggered tasks (WHEN SYSTEM$STREAM_HAS_DATA without SCHEDULE), with serverless options and limits."
sources:
  - https://docs.snowflake.com/en/user-guide/tasks-triggered
  - https://docs.snowflake.com/en/sql-reference/sql/create-task
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Triggered tasks

**Goal:** process new rows within seconds of arrival without polling on a schedule and paying for empty runs.

## Define
```sql
CREATE OR REPLACE TASK load_orders
  WAREHOUSE = etl_wh              -- or omit for serverless: USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE
  WHEN SYSTEM$STREAM_HAS_DATA('raw.orders_stream')
AS
  MERGE INTO core.orders t USING raw.orders_stream s ON t.order_id = s.order_id
  WHEN MATCHED AND s.metadata$action = 'DELETE' AND NOT s.metadata$isupdate THEN DELETE
  WHEN MATCHED AND s.metadata$action = 'INSERT' THEN UPDATE SET t.status = s.status
  WHEN NOT MATCHED AND s.metadata$action = 'INSERT' THEN INSERT (order_id, status) VALUES (s.order_id, s.status);

ALTER TASK load_orders RESUME;
```
No `SCHEDULE`: the task runs when the stream has data.

## Behaviour
- Minimum interval between runs: `USER_TASK_MINIMUM_TRIGGER_INTERVAL_IN_SECONDS` (default 30 s).
- Streams can be created on tables, external tables, dynamic tables, Iceberg tables, directory tables and views; check the triggered-task docs for the sources that can trigger a task.

## vs scheduled + WHEN
A scheduled task with `WHEN SYSTEM$STREAM_HAS_DATA(...)` also skips runs when the stream is empty (a SKIPPED run does not resume the warehouse) but only checks on its schedule; a triggered task has no schedule.

## Gotchas
- The DML must consume the stream (read it in a committed statement) or the task keeps firing.
- Resume the task after creating it (`ALTER TASK ... RESUME`).

## Verify
`TASK_HISTORY(task_name => 'LOAD_ORDERS')` shows runs only after inserts, about 30 s apart under constant load.

## Checked
2026-10-28. Confirmed against the triggered tasks page and CREATE TASK (no SCHEDULE with WHEN SYSTEM$STREAM_HAS_DATA, USER_TASK_MINIMUM_TRIGGER_INTERVAL_IN_SECONDS with a 30 second default and 10 second minimum, USER_TASK_MANAGED_INITIAL_WAREHOUSE_SIZE, SKIPPED runs do not resume the warehouse) and the streams introduction (supported source objects). Removed: OR across several streams, task-graph root claim, serverless cost claim and the created-suspended claim.
Method: documentation only; no commands were run.
