---
id: computing-software.data-engineering.apache-airflow.dynamic-task-mapping-and-dag-factories
name: dynamic-task-mapping-and-dag-factories
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, dynamic-task-mapping, expand, expand-kwargs, taskflow-api, dag-factory, multiple-outputs, map-reduce, max-active-tis-per-dag, parsing-performance, zombie-tasks, dynamic-dag-generation]
level: practitioner
status: docs-checked
description: "Generate many near-identical tasks/DAGs from data instead of copy-pasted code: dynamic task mapping, DAG factories, and their scaling limits."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/authoring-and-scheduling/dynamic-task-mapping.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/howto/dynamic-dag-generation.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/src/airflow/config_templates/config.yml
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/core-concepts/xcoms.rst
  - https://github.com/apache/airflow/blob/main/task-sdk/src/airflow/sdk/bases/operator.py
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Generating tasks and DAGs from data, not copy-paste

**Goal:** when "one task per table/client/file" means a variable, data-driven number of tasks, generate them instead of hand-writing or looping at parse time.

## 1. Dynamic task mapping (`expand`) — fan-out at runtime
```python
@task
def list_tables():
    return ["orders", "customers", "payments"]

@task
def load_table(table: str):
    run_sql(f"...{table}...")

load_table.expand(table=list_tables())
```
This creates one mapped task instance per element, decided at **runtime** from the upstream task's return value — unlike a Python `for` loop in the DAG file, which decides task count at **parse time** from static data. Passing several arguments to `expand` creates a cross product; use `expand_kwargs` (a sequence of mappings) when each call needs its own combination of arguments.
- **Gotcha:** the mapped-over value comes from an upstream XCom; map over keys or paths and load the bulk data inside the task rather than mapping over a huge list.
- **Gotcha:** `[core] max_map_length` (default 1024) is the longest list or dict an XCom can push to trigger mapping; a longer one fails the task that pushed it. A silently growing source list can hit it, so alert on the count.
- Limit concurrency of a mapped task with `max_active_tis_per_dag` (or `max_active_tis_per_dagrun`) passed to the task or to `partial()`, or with a pool, so hundreds of instances do not all hit a source DB at once.

## 2. DAG factories — generate whole DAGs from config
For "same shape, different source" DAGs (e.g. one DAG per client extracting to the same schema), write a Python function that takes a config dict and returns a `DAG` object, then call it in a loop over a YAML/JSON config file kept in the DAG folder. DAGs created by calling a `@dag`-decorated function (or used in a `with DAG(...)` block) are registered automatically; set `auto_register=False` to opt out:
```python
for cfg in load_configs("configs/*.yaml"):
    make_client_dag(cfg)      # a @dag-decorated function taking the config
```
This is parse-time generation — the DAG list is fixed once the file is read, unlike dynamic task mapping which is runtime. Use a DAG factory when each client needs its own schedule, SLA, or owner in the Airflow UI; use dynamic task mapping when they share one DAG and schedule.
- **Gotcha — parsing cost:** the DAG file is re-parsed every `[dag_processor] min_file_process_interval` seconds (default 30), and the whole file is loaded to process all its DAGs. A slow config loader (network call, large file) slows parsing of every DAG it generates. Keep the config in a file next to the DAGs instead of fetching it at parse time, and prefer mapped tasks within fewer DAGs when the per-client difference is only data.

## 3. Choosing between them
- Same schedule, same owner, varying data → dynamic task mapping, one DAG.
- Different schedule/owner/alerting per entity → DAG factory, many DAGs.

## Verify
- [ ] `list_tables()`'s return value stays small: the default XCom backend stores values in the Airflow database, and an object storage XCom backend is recommended for larger values.
- [ ] Mapped task count has an alert before it approaches `max_map_length`.
- [ ] DAG-file parse time stays low as the config list grows.
- [ ] A new entity added to config appears in the Airflow UI without a code deploy (factory) or next DAG run (mapping).

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: the runtime-versus-parse-time distinction, `expand` cross product versus `expand_kwargs`, `max_map_length` meaning and default 1024 (config.yml), `max_active_tis_per_dag` and `max_active_tis_per_dagrun` (operator source), automatic DAG registration and `auto_register=False`, `min_file_process_interval` default 30 under `[dag_processor]`, and the default database XCom backend with object storage recommended for large values. Removed the pickling claim, the `globals()` registration pattern, the `dag-factory` package remark, the 1s parse target and the UI scaling claim, which the docs do not support.

Method: documentation only; no commands were run.
