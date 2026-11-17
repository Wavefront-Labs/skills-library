---
id: computing-software.data-engineering.apache-airflow.mapped-task-groups
name: mapped-task-groups
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, mapped-task-groups, dynamic-task-mapping, task-group-expand, map-index, max-active-tis-per-dagrun, partial, task-groups]
level: advanced
status: docs-checked
description: "Fan out whole sub-pipelines in Airflow with mapped task groups: @task_group.expand, per-instance dependencies, map_index in the UI, concurrency limits, and failure isolation."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/authoring-and-scheduling/dynamic-task-mapping.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/src/airflow/config_templates/config.yml
  - https://github.com/apache/airflow/blob/main/task-sdk/src/airflow/sdk/bases/operator.py
  - https://github.com/apache/airflow/blob/main/task-sdk/src/airflow/sdk/definitions/decorators/task_group.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mapped task groups

**Goal:** run an extract -> validate -> load chain once per item discovered at runtime (tables, files, tenants), where each item's chain proceeds independently.

## Pattern
```python
from airflow.sdk import dag, task, task_group

@dag(schedule="@daily", catchup=False, max_active_tasks=16)
def per_table_sync():
    @task
    def list_tables() -> list[str]:
        return discover_changed_tables()                 # runtime list

    @task_group
    def sync(table: str):
        @task(max_active_tis_per_dagrun=4)
        def extract(t): return export_to_s3(t)
        @task
        def validate(path): check_rows(path); return path
        @task
        def load(path): copy_into_warehouse(path)
        load(validate(extract(table)))

    sync.expand(table=list_tables())
per_table_sync()
```
Each table gets its own instance of every task, with `map_index` 0..n-1. Within one instance, `validate[3]` depends only on `extract[3]`, so a slow table does not hold back the others.

## Behaviour notes
- `.partial(...)` on the group fixes constant arguments; `.expand_kwargs([...])` passes per-instance dicts.
- An empty input creates no instances and the mapped task is marked `skipped`; downstream joins need a trigger rule that allows skipped upstreams.
- Upper bound: `[core] max_map_length` (default 1024), the longest list or dict that can trigger mapping.
- Limit concurrency with `max_active_tis_per_dagrun` or `max_active_tis_per_dag` on a task, or with pools; otherwise 500 tables can mean 500 simultaneous extracts.
- Custom labels so the UI shows table names instead of numbers: `@task(map_index_template="{{ table_label }}")` and inside the task `get_current_context()["table_label"] = t`.

## Gotchas
- Code in a task group function cannot resolve the values passed into it (a group has no worker); do any logic on them inside a task.
- Task mapping nested inside a mapped task group is not permitted.
- Depending on a mapped task group's output aggregates the group's results into a list; return the value you want to collect from the group function.
- You cannot branch on the results of a mapped task, but you can branch on the input of a task group.

## Verify
- [ ] Grid view shows n mapped instances per task with readable labels.
- [ ] One failing table leaves other tables' loads successful.
- [ ] Peak concurrent extracts never exceed the configured limit.

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: group `expand` and `expand_kwargs`, per-expansion dependency (each task depends only on its own group instance), empty-input skip, `max_map_length`, `max_active_tis_per_dagrun`, `map_index_template` with `get_current_context()`, no nested mapping inside a mapped group, aggregation of group outputs and branching limits (dynamic-task-mapping.rst, task-group decorator source). Removed the 2.6 and 2.9 version gates and the per-instance retry and clearing claims, which the docs do not state.

Method: documentation only; no commands were run.
