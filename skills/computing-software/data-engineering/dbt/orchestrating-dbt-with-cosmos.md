---
id: computing-software.data-engineering.dbt.orchestrating-dbt-with-cosmos
name: orchestrating-dbt-with-cosmos
category: computing-software
field: data-engineering
product: dbt
tags: [dbt, dbt-core, dbt-orchestration, astronomer-cosmos, airflow, dbttaskgroup, dbtdag, databricks-dbt-task, dagster-dbt, bash-operator-dbt]
level: advanced
status: docs-checked
description: "Orchestrate dbt Core: Astronomer Cosmos DbtTaskGroup/DbtDag (per-model tasks, render config, execution modes), a single dbt build task, Databricks dbt tasks, and Dagster assets."
sources:
  - https://astronomer.github.io/astronomer-cosmos/
  - https://docs.databricks.com/en/jobs/dbt.html
  - https://docs.dagster.io/integrations/libraries/dbt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Orchestrating dbt Core (Cosmos, Databricks, Dagster)

**Goal:** schedule dbt runs with retries, visibility per model, and dependencies on upstream ingestion, without hand-maintaining a task per model.

## Option A: one task running dbt build
```python
BashOperator(task_id="dbt_build", bash_command="cd /opt/dbt && dbt build", retries=0)
```
Simple (one dbt process). Downside: one failure = rerun the whole thing (use `dbt retry` in a follow-up task), and no per-model visibility in Airflow.

## Option B: Cosmos (per-model Airflow tasks)
Astronomer Cosmos turns a dbt project into Airflow tasks, so Airflow can schedule and monitor dbt (per its home page). The class names, load modes and execution modes are on the Cosmos docs site (`DbtTaskGroup` / `DbtDag` and the render and execution configuration pages); take the code from there for your Cosmos version.
- Per-model tasks give per-model retries and status in Airflow.
- Watch DAG parse cost and Airflow scheduling overhead for large projects; compare against Option A.

## Option C: platform-native
- **Databricks jobs** dbt task: runs the dbt commands you list (default `dbt deps`, `dbt seed`, `dbt run`) on a SQL warehouse; good when everything else is on Databricks.
- **Dagster** has a dbt integration (see its dbt docs page).
- **dbt Cloud** jobs, when you use Cloud.

## Verify
- [ ] Upstream ingestion completion gates the dbt run (asset or task dependency).
- [ ] A failing model can be retried without rebuilding successful ones.
- [ ] DAG parse time for the Cosmos DAG stays low.

## Checked

2026-10-28. Confirmed against: Cosmos home page, Databricks dbt task page (SQL warehouse, default commands dbt deps/seed/run), Dagster dbt page, snapshots/upgrade pages for dbt retry. Removed (not confirmable in the fetched pages): Cosmos code and constants (DbtTaskGroup args, LoadMode, TestBehavior, dbt_executable_path), --selector flag, @dbt_assets claim, DbtCloudRunJobOperator, 1000-model threshold, dbt build under Databricks.

Method: documentation only; no commands were run.
