---
id: computing-software.data-engineering.apache-airflow.task-sdk-and-api-server
name: task-sdk-and-api-server
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, airflow-3, task-sdk, airflow-api-server, direct-db-access-removed, task-execution-api, dag-processor, edge-executor, airflow-client]
level: advanced
status: docs-checked
description: "Airflow 3 architecture: tasks use the Task SDK and API server instead of the metadata DB, separate dag-processor, what breaks, and swapping DB access for REST API calls."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/installation/upgrading_to_airflow3.html
  - https://airflow.apache.org/docs/task-sdk/stable/index.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Airflow 3: Task SDK, API server, and no direct DB access

**Goal:** run and write tasks for Airflow 3's client-server architecture, and fix code that assumed workers could touch the metadata database.

## What changed (AIP-72)
- **Workers no longer connect to the metadata DB.** Task code runs via the **Task SDK**, which talks to the **Task Execution API** served by the API server. XComs, variables, connections and state updates flow over HTTP.
- `airflow api-server` is the API server component (see the CLI reference).
- `airflow dag-processor` is a separate component.
- Components: scheduler, dag-processor, api-server, triggerer, workers (Celery/K8s/Edge executor for remote workers).

## Code that breaks
```python
# Airflow 2 patterns that fail in tasks on 3.x
from airflow.settings import Session
from airflow.models import DagRun, TaskInstance
with Session() as s:
    s.query(DagRun).filter(...)          # not allowed in task code on 3.x
```
Also: any other use of Airflow database sessions or ORM models from task code.

## Replacements
| Need | Airflow 3 way |
|---|---|
| Read variables/connections | Task SDK (`airflow.sdk`), e.g. `Connection.get("my_conn")`, not ORM sessions |
| XCom | Return values and the Task SDK, not ORM queries |
| Info about other DAG runs, trigger runs, clear tasks | Public REST API (`apache-airflow-client` Python package) with an access token from `/auth/token` |
| Previous run state | Look up the available context keys in the Task SDK context reference |
| Pausing DAGs, admin chores | REST API or CLI outside tasks |
Install `apache-airflow-client`, fetch a token from `/auth/token`, and call the REST API with it; see the client's docs for the call signatures.

## Operating notes
- Workers need network access to the API server's execution API, not the DB. The `[core] execution_api_server_url` option is listed as deprecated in the configuration reference; look up its replacement there.
- Scale the API server for task traffic.
- Plugins that ran code in the scheduler/webserver with DB access must be reviewed against the 3.x plugin interface.

## Verify
- [ ] Workers' network policy blocks the metadata DB and tasks still succeed.
- [ ] `grep -rE "settings.Session|provide_session|DagRun.find" dags/ plugins/` returns nothing in task code.
- [ ] dag-processor and api-server deployed and monitored as separate components.

## Checked

2026-10-28. Confirmed against: the Airflow 3 upgrade guide, best-practices page, CLI reference and configuration reference. Removed (not confirmable in the fetched pages): prev_* context names, Variable import path, REST client call signature, UI/REST v2 description, RuntimeError text.

Method: documentation only; no commands were run.
