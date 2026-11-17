---
id: computing-software.data-engineering.apache-airflow.manual-triggers-with-run-conf
name: manual-triggers-with-run-conf
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, trigger-dag-conf, dag-params, manual-trigger, rest-api-trigger, param-validation, dag-run-conf]
level: practitioner
status: docs-checked
description: "Trigger Airflow DAG runs manually or via CLI/REST with run conf, validate inputs with Params, and read them safely in tasks and templates."
sources:
  - https://github.com/apache/airflow/blob/main/airflow-core/docs/core-concepts/params.rst
  - https://github.com/apache/airflow/blob/main/airflow-core/src/airflow/api_fastapi/core_api/openapi/v2-rest-api-generated.yaml
  - https://github.com/apache/airflow/blob/main/airflow-core/src/airflow/cli/cli_config.py
  - https://github.com/apache/airflow/blob/main/airflow-core/src/airflow/config_templates/config.yml
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Manual triggers with run conf

**Goal:** let operators re-run a pipeline for a specific scope (date range, customer, full refresh) with validated inputs instead of editing code.

## Declare Params
```python
from airflow.sdk import dag, task, Param

@dag(schedule="@daily", catchup=False, params={
    "start_date": Param(None, type=["null", "string"], format="date", description="Override start (YYYY-MM-DD)"),
    "customers": Param([], type="array", items={"type": "string"}),
    "full_refresh": Param(False, type="boolean"),
    "mode": Param("incremental", enum=["incremental", "backfill"]),
})
def sales_load():
    @task
    def plan(params=None, data_interval_start=None):
        start = params["start_date"] or data_interval_start.to_date_string()
        return {"start": start, "full": params["full_refresh"]}
    plan()
sales_load()
```
Params are validated with JSON Schema; scheduled runs use the defaults, and the trigger form in the UI is generated from them. If validation fails, Airflow shows a warning instead of creating the DAG run. Typed fields are required by default; allow the `null` type to make one optional.

## Trigger
```bash
# CLI
airflow dags trigger sales_load --conf '{"start_date": "2026-09-01", "full_refresh": true}'
# REST (/api/v2, token auth; logical_date is required but may be null)
curl -X POST "$AF/api/v2/dags/sales_load/dagRuns" -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' -d '{"logical_date": null, "conf": {"mode": "backfill"}}'
```

## Reading values
- In tasks: use `params` from the task context. Values passed when triggering override the DAG defaults, and task-level params take precedence over DAG-level ones. `dag.params` inside the DAG definition only ever holds the defaults, not the values supplied at trigger time.
- In templates: `{{ params.start_date }}`. Templates render params as strings by default.
- Scheduled runs use the param defaults; make defaults produce normal behaviour.

## Settings
- `[core] dag_run_conf_overrides_params` controls whether values supplied when triggering can update params; setting it to `False` turns the default params into constants.
- When the DAG has a `schedule`, params with defaults must be valid, which is checked at DAG parse time; with `schedule=None` the validation happens when you trigger the DAG.

## Gotchas
- Do not paste untrusted conf values into shell commands through templates; constrain them with JSON Schema keywords such as `enum` or `pattern`.
- Pass references (paths, ids) rather than large data in conf.

## Verify
- [ ] Trigger form shows typed fields; invalid input is rejected before the run is created.
- [ ] Scheduled run with no conf behaves identically to before Params were added.

## Checked

2026-10-25: Airflow documentation source on the apache/airflow main branch (airflow-core/docs, task-sdk and providers/standard), latest commit 2026-10-24. Confirmed: Param validation with JSON Schema and the generated trigger form, `format="date"`, `enum`, `type=["null", "string"]` for optional typed fields, parse-time validation for scheduled DAGs, `params` precedence and the `dag.params` caveat (params.rst), `dag_run_conf_overrides_params`, the `-c/--conf` option of `airflow dags trigger` (CLI source) and `POST /api/v2/dags/{dag_id}/dagRuns` with required nullable `logical_date` and optional `conf` (OpenAPI spec). Removed the Airflow 2 API example, the default-value claim for `dag_run_conf_overrides_params`, the logical-date uniqueness claim and the metadata size remark, which are not documented. The empty-string date default was replaced because a scheduled DAG must have valid param defaults.

Method: documentation only; no commands were run.
