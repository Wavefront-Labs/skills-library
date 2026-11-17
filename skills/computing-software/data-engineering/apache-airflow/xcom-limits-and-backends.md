---
id: computing-software.data-engineering.apache-airflow.xcom-limits-and-backends
name: xcom-limits-and-backends
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, xcom, xcom-backend, xcomobjectstoragebackend, xcom-size-limit, taskflow-api, multiple-outputs]
level: practitioner
status: docs-checked
description: "Use Airflow XComs safely: pass references not data, size limits per database, TaskFlow return values, and the object storage XCom backend for larger payloads."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/core-concepts/xcoms.rst
  - https://github.com/apache/airflow/blob/main/providers/common/io/docs/xcom_backend.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/templates-ref.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XCom limits and custom backends

**Goal:** tasks share small metadata (paths, ids, counts) reliably, without bloating the metadata database.

## Rule: pass references, not data
XComs are designed for small amounts of data; the docs say not to pass large values such as dataframes. The default backend stores them in the Airflow database. Return `"s3://lake/tmp/run_123/part.parquet"`, a row count, or a job id, never a DataFrame or a list of a million ids.

## TaskFlow usage
```python
@task
def extract(run_id=None) -> dict:
    return {"path": f"s3://lake/tmp/{run_id}/", "rows": 120345}
@task(multiple_outputs=True)            # each dict key is pushed as its own XCom
def stats(): return {"min_ts": "...", "max_ts": "..."}

@task
def load(meta: dict): ...
load(extract())
```
Classic operators: `ti.xcom_pull(task_ids="extract", key="return_value")` (`return_value` is the default key); in templates use `{{ ti.xcom_pull(task_ids='extract')['path'] }}`. Always pass `task_ids` explicitly: without it `xcom_pull` pulls only from the current task. Values can be any serializable value, including `@dataclass` and `@attr.define` objects.

## Object storage backend (larger payloads)
With the common-io provider:
```ini
[core]
xcom_backend = airflow.providers.common.io.xcom.backend.XComObjectStorageBackend
[common.io]
xcom_objectstorage_path = s3://conn_id@mybucket/key     # the connection id is the user part of the URL
xcom_objectstorage_threshold = 1048576     # bytes; smaller values stay in the DB, larger go to object storage
xcom_objectstorage_compression = gzip
```
The DB then stores only a reference for big values; `threshold` must be larger than -1. Compression needs support installed (zip, gzip and bz2 work out of the box; `snappy` needs `python-snappy`). Rows removed through the REST API, the UI or `airflow db clean` leave the stored object behind, so manage cleanup of the bucket prefix yourself.
A custom backend: subclass `BaseXCom` and override `store_value` and `load_value` (and `purge` to delete stored data); a backend that only overrides `serialize_value` and `deserialize_value` cannot be used with Dags that use task loops.

## Gotchas
- When a task is retried its XComs are cleared, so XComs cannot persist state across retries or sensor pokes.
- Mapped tasks: pulling all values returns a lazy sequence; iterate, do not materialise thousands into memory.
- XCom operations go through the task context; directly updating the XCom database model is not possible.

## Verify
- [ ] Large-output tasks write to storage and return a path.

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: XComs designed for small values with the database as the default backend, `xcom_pull` default key and `task_ids` behaviour, serializable value types, `multiple_outputs`, the object storage backend settings (`xcom_backend`, `xcom_objectstorage_path`, `xcom_objectstorage_threshold` larger than -1, `xcom_objectstorage_compression`) and the compression note, custom backend methods (`store_value`, `load_value`, `purge`) with db clean leaving stored data behind, and XCom clearing on retry. Removed the per-database size limits, the 2.9 gate, the pickling statement and the SQL check, which are not documented. The returned path now uses the `run_id` context variable instead of a template string that a task body would not render.

Method: documentation only; no commands were run.
