---
id: computing-software.data-engineering.etl-pipeline-design.pipeline-timeouts-and-resource-limits
name: pipeline-timeouts-and-resource-limits
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, pipeline-timeouts, resource-limits, execution-timeout, query-timeouts]
level: practitioner
status: docs-checked
description: "Bound pipeline runtime and resource use: task execution timeouts, warehouse query timeouts, HTTP and DB client timeouts, memory limits, and safe behaviour on timeout."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/tasks.html#timeouts
  - https://docs.snowflake.com/en/sql-reference/parameters#statement-timeout-in-seconds
  - https://requests.readthedocs.io/en/latest/user/advanced/#timeouts
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Timeouts and resource limits

**Goal:** a hung step fails fast and visibly instead of blocking a pipeline for hours or burning credits.

## Layered timeouts (inner shorter than outer)
| Layer | Setting |
|---|---|
| HTTP calls | `requests.get(url, timeout=(5, 60))` (connect, read); never default (infinite) |
| DB client | connect/query timeouts in the driver (look up the driver's setting; for example Postgres has a `statement_timeout` setting) |
| Warehouse | Snowflake `STATEMENT_TIMEOUT_IN_SECONDS` (default 172800, i.e. 2 days; 0 enforces the maximum of 604800, 7 days) and `STATEMENT_QUEUED_TIMEOUT_IN_SECONDS` (default 0, no timeout); both can be set on the account, user, session or an individual warehouse |
| Task | Airflow `execution_timeout` set to a `datetime.timedelta` (for example `timedelta(hours=1)`); breach raises `AirflowTaskTimeout`; applies to all tasks including sensors |
| Run/DAG | a job-level or run-level timeout in your orchestrator (check its docs) |
Airflow sensors in reschedule mode also have a separate `timeout`, which raises `AirflowSensorTimeout` and fails the sensor without retrying. Set the task timeout from history (a margin over p99 runtime), not a round guess.

Snowflake: when a parameter is set both in the session hierarchy and on the warehouse, the lowest non-zero value applies. The statement timeout covers the whole statement, including queue time, locked time, compilation and execution.

```sql
ALTER WAREHOUSE etl_wh SET STATEMENT_TIMEOUT_IN_SECONDS = 3600 STATEMENT_QUEUED_TIMEOUT_IN_SECONDS = 900;
```

## Resource limits
- Container memory/CPU limits for tasks (Kubernetes pod resources) so one task cannot starve others; size requests from observed usage.
- Warehouse resource monitors / budgets to cap spend.
- Concurrency limits (pools, max active runs) on fragile sources.

## On timeout
- Make tasks idempotent so a retry after timeout is safe; partial writes must be rolled back or overwritten.
- Kill the remote work too: a task timeout that leaves a warehouse query running still costs. Use operators that cancel remote queries when the task is killed, or rely on the warehouse statement timeout.
- Alert distinctly on timeouts (often a sign of data growth or locking).

## Verify
Simulate a hanging step (sleep / lock): the task fails at its timeout, the remote query is cancelled (query history shows it), and the retry succeeds.

## Checked
Date: 2026-11-09. Confirmed from the Airflow Tasks page (execution_timeout, AirflowTaskTimeout, sensor timeout and AirflowSensorTimeout), the Snowflake parameters reference (both statement timeout parameters: defaults, 604800 maximum, lowest non-zero rule, scope levels, whole-statement time) and the Requests advanced usage page (connect and read timeouts as a tuple, no timeout by default). The SQL ALTER WAREHOUSE example is a usage illustration of the documented parameters. Removed: BigQuery jobTimeoutMs, Databricks SQL and job timeout names, dbt threads, Airflow dagrun_timeout, the Postgres connection-string example and the on_kill reference (none on the read pages). Not read: Postgres or BigQuery docs.
Method: documentation only; no commands were run.
