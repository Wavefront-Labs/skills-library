---
id: computing-software.data-engineering.apache-airflow.mapping-with-map-and-zip
name: mapping-with-map-and-zip
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, dynamic-task-mapping, xcom-map-zip, xcomarg-map, xcomarg-zip, expand, cross-product]
level: advanced
status: docs-checked
description: "Reshape inputs to Airflow dynamic task mapping with XComArg .map(), .zip() and .concat(), and expand over cross products without extra transform tasks."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/authoring-and-scheduling/dynamic-task-mapping.rst
  - https://github.com/apache/airflow/blob/main/task-sdk/src/airflow/sdk/definitions/xcom_arg.py
  - https://github.com/apache/airflow/blob/main/airflow-core/src/airflow/config_templates/config.yml
  - https://github.com/apache/airflow/blob/main/task-sdk/src/airflow/sdk/bases/operator.py
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/core-concepts/xcoms.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mapping inputs with .map() and .zip()

**Goal:** feed mapped tasks exactly the arguments they need from upstream XComs, without writing a separate "reshape" task that adds latency and a worker slot.

## .map(): transform each element lazily
```python
@task
def list_files() -> list[str]:
    return ["s3://landing/a.csv", "s3://landing/b.csv"]

def to_copy_kwargs(path: str) -> dict:
    return {"source_bucket_key": path, "dest_bucket_key": path.replace("landing", "staged")}

copy = S3CopyObjectOperator.partial(task_id="copy", aws_conn_id="aws").expand_kwargs(
    list_files().map(to_copy_kwargs)
)
```
- The function runs lazily when each mapped instance resolves its argument, not as its own task.
- It must be a plain Python function taking exactly one positional argument, not a task; it runs as pre-processing of the downstream task.
- Raising `AirflowSkipException` inside the map function marks that element's mapped instance as skipped.

## .zip(): pair lists element-wise
```python
@task
def tables() -> list[str]: return ["orders", "customers"]
@task
def watermarks() -> list[str]: return ["2026-10-17", "2026-10-16"]

@task
def load(pair):
    table, since = pair
    ...

load.expand(pair=tables().zip(watermarks()))
# by default the shortest input wins; pass fillvalue=... to pad to the longest
```
The signature in the SDK source is `zip(*others, fillvalue=...)`; the prose docs call the same option `default`, so check which name your installed version accepts.

## .concat(): append lists
```python
process.expand(path=list_new_files().concat(list_retry_files()))
```

## Cross product vs zip
`expand(a=[1,2], b=["x","y"])` maps over the **cartesian product** (4 instances). Use `.zip()` or `expand_kwargs` with pre-built dicts when you want pairs (2 instances).

## Limits
- `[core] max_map_length` (default 1024) is the longest list or dict that can trigger mapping; a longer one fails the pushing task.
- `max_active_tis_per_dagrun` on the mapped task limits concurrent instances per DAG run (`max_active_tis_per_dag` limits them across runs).

## Gotchas
- The upstream XCom must be a list or dict. Return keys or paths, not bulk data: the default XCom backend stores values in the Airflow database.

## Verify
- [ ] Graph shows the expected number of map indexes and no extra reshape task.
- [ ] `map_index_template` (or task logs) shows each instance received the right pair.

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: `.map()` contract (plain function, one positional argument, runs in the downstream task, `AirflowSkipException` marks the element skipped), `.zip()` shortest-wins default and the `fillvalue` parameter in the SDK source (docs prose says `default`), `.concat()`, the `expand` cross product, `max_map_length`, per-run concurrency limit and the database XCom default. Removed the 2.10 gate, the lambda serialization, generator and UI-visibility claims, and the scheduler-load remark, which are not in the docs.

Method: documentation only; no commands were run.
