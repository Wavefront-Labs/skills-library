---
id: computing-software.data-engineering.apache-airflow.naming-mapped-task-instances
name: naming-mapped-task-instances
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, map-index-template, dynamic-task-mapping, mapped-tasks, rendered-map-index, observability]
level: practitioner
status: docs-checked
description: "Give Airflow mapped task instances readable names with map_index_template (2.9+) so operators see table or file names instead of indexes 0..N in the UI."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/authoring-and-scheduling/dynamic-task-mapping.rst
  - https://github.com/apache/airflow/blob/main/task-sdk/src/airflow/sdk/bases/operator.py
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Naming mapped task instances (map_index_template)

**Goal:** when task `load[37]` fails, the on-call sees `load[customers_eu]` and can act without opening logs.

## Classic operators
```python
SQLExecuteQueryOperator.partial(
    task_id="refresh",
    conn_id="warehouse",
    map_index_template="{{ task.parameters['table'] }}",
).expand(parameters=[{"table": "orders"}, {"table": "customers"}])
```
The template is rendered with the task context after each expanded task executes, so it can read the task's own (expanded) attributes via `task`, for example `{{ task.parameters['table'] }}` for `.expand(parameters=...)`.

## TaskFlow
```python
from airflow.sdk import get_current_context

@task(map_index_template="{{ table_label }}")
def load(table: str, region: str):
    ctx = get_current_context()
    ctx["table_label"] = f"{table}_{region}"     # set a context var the template reads
    ...

load.expand_kwargs([{"table": "orders", "region": "eu"}, {"table": "orders", "region": "us"}])
```

## Behaviour
- The names show up in the Airflow UI instead of the integer indexes.
- Because the template is rendered after the main execution block, a TaskFlow function can inject a variable into the context (`get_current_context()["my_variable"] = ...`) for the template to use.

## Good labels
- Short and unique per run: table name, partition, file stem, customer id.
- Avoid secrets or PII in labels.

## Related tips
- Combine with `max_active_tis_per_dagrun` to control concurrency of mapped instances.

## Verify
- [ ] The UI shows labelled map indexes for a test run.

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: `map_index_template` on `partial()` for classic operators and on `@task`, rendering after execution with the task context, `get_current_context()` injection and the UI naming (dynamic-task-mapping.rst, Named mapping), and `max_active_tis_per_dagrun`. Removed the 2.9 gate, the `rendered_map_index` REST and callback claims, the CLI and clearing claims and the fallback behaviour, which are not stated in the docs.

Method: documentation only; no commands were run.
