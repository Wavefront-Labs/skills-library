---
id: computing-software.data-engineering.apache-airflow.task-groups
name: task-groups
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, dag, task-groups, task-group-decorator, subdag-replacement, prefix-group-id, default-args, ui-grouping, reusable-pattern]
level: practitioner
status: docs-checked
description: "Organise Airflow DAGs with task groups: @task_group and TaskGroup, reusable group factories, prefixed task ids, group-level default_args, and replacing removed SubDAGs."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/core-concepts/dags.rst
  - https://github.com/apache/airflow/blob/main/task-sdk/src/airflow/sdk/definitions/taskgroup.py
  - https://github.com/apache/airflow/blob/main/task-sdk/src/airflow/sdk/definitions/decorators/task_group.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Task groups

**Goal:** group repeated or logically related tasks for readability and reuse, without the scheduling problems SubDAGs had .

## Decorator form
```python
from airflow.sdk import dag, task, task_group

@dag(schedule="@daily", catchup=False)
def ingest_sources():
    @task_group(group_id="orders", tooltip="extract, validate, load orders")
    def pipeline(table: str):
        @task
        def extract(t): return f"s3://landing/{t}/"
        @task
        def validate(path): ...
        @task
        def load(path): ...
        p = extract(table)
        validate(p) >> load(p)

    pipeline.override(group_id="orders")("orders")
    pipeline.override(group_id="customers")("customers")
ingest_sources()
```
Task ids become `orders.extract`, `customers.load`, etc. (child ids are prefixed with the parent group id by default; `prefix_group_id=False` disables that). Without an explicit `tooltip`, the decorated function's docstring is used.

## Context-manager form (classic operators)
```python
from airflow.sdk import TaskGroup
with TaskGroup("dq_checks", default_args={"retries": 0}) as dq:
    check_counts = SQLColumnCheckOperator(...)
    check_fresh = SQLTableCheckOperator(...)
load >> dq >> publish        # dependencies on the whole group
```
`default_args` on a group override the DAG's for tasks inside it.

## Patterns
- **Factory functions** returning a task group for each source system keep DAG files short.
- Combine with dynamic task mapping: a `@task_group` can be `.expand()`ed over a list (mapped task groups).

## Gotchas
- With `prefix_group_id=False` you must keep every task and group id unique yourself.

## Verify
- [ ] Graph view shows collapsed groups with the expected tasks.
- [ ] Any task-id references use the prefixed ids.

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: decorator and context-manager forms, `override(group_id=...)`, `.expand()` on a task group and docstring tooltip (task-sdk decorator source), default id prefixing and `prefix_group_id=False`, group `default_args` overriding DAG-level ones. Removed the SubDAG removal note, the 2.5 version gate and the claims about concurrency, renaming and nesting depth, which the docs do not state.

Method: documentation only; no commands were run.
