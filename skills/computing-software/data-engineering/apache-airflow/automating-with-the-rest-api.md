---
id: computing-software.data-engineering.apache-airflow.automating-with-the-rest-api
name: automating-with-the-rest-api
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow-rest-api, api-v2, jwt-token, clear-task-instances, dag-runs, automation, airflow-client]
level: practitioner
status: gated
description: "Automate Airflow via its REST API (v1 in 2.x, v2 in 3.x): auth tokens, triggering runs, clearing failed tasks, pausing DAGs, and polling run state from scripts and CI."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/stable-rest-api-ref.html
  - https://airflow.apache.org/docs/apache-airflow/stable/security/api.html
  - https://github.com/apache/airflow-client-python
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Automating Airflow with the REST API

**Goal:** script operations (trigger, rerun failures, pause/unpause, monitor) from CI, other systems or runbooks.

## Auth
- **Airflow 3 (`/api/v2`):** get a JWT from the API server, then send `Authorization: Bearer`. (gated: unconfirmed, source is paywalled or blocked)
```bash
TOKEN=$(curl -s -X POST "$AF/auth/token" -H 'Content-Type: application/json' \
  -d '{"username":"svc_ci","password":"'"$PW"'"}' | jq -r .access_token)
```
  (Exact token endpoint depends on the auth manager: SimpleAuthManager/FAB provide `/auth/token`.)
- **Airflow 2 (`/api/v1`):** basic auth or session per `[api] auth_backends` (`airflow.api.auth.backend.basic_auth`). Managed services wrap it: MWAA (`create-web-login-token`/`invoke-rest-api`), Composer (IAP/OAuth token).

Use a dedicated service account with only the needed role.

## Common calls (v2; v1 is similar with /api/v1)
```bash
H=(-H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json')
# trigger
curl -s -X POST "$AF/api/v2/dags/sales_load/dagRuns" "${H[@]}" -d '{"logical_date": null, "conf": {"full_refresh": false}}'
# run state
curl -s "$AF/api/v2/dags/sales_load/dagRuns/$RUN_ID" "${H[@]}" | jq -r .state
# list failed runs in a window
curl -s "$AF/api/v2/dags/~/dagRuns?state=failed&start_date_gte=2026-10-17T00:00:00Z" "${H[@]}"
# clear failed tasks of a run (dry run first)
curl -s -X POST "$AF/api/v2/dags/sales_load/clearTaskInstances" "${H[@]}" \
  -d '{"dag_run_id": "'"$RUN_ID"'", "only_failed": true, "dry_run": true}'
# pause / unpause
curl -s -X PATCH "$AF/api/v2/dags/sales_load?update_mask=is_paused" "${H[@]}" -d '{"is_paused": true}'
```
`~` is a wildcard for dag_id in list endpoints.

## Python client
```python
import airflow_client.client as af
cfg = af.Configuration(host=f"{AF}/api/v2", access_token=TOKEN)   # v1 client: username/password
with af.ApiClient(cfg) as c:
    runs = af.DagRunApi(c).get_dag_runs(dag_id="sales_load", state=["failed"], limit=50)
```
Use the client major version matching the Airflow major version.

## Poll pattern for CI
Trigger, then poll state every 30 s until `success`/`failed`, with an overall timeout; print task-level failures via `GET .../taskInstances?state=failed`.

## Gotchas
- v1 endpoints are removed in Airflow 3; `execution_date` fields became `logical_date`, and `logical_date` may be null for manual runs.
- Pagination: default `limit` 100 (max per `[api] maximum_page_limit`); loop with `offset`.
- Rate of polling many runs can load the API server; use list endpoints with filters instead of per-run calls.

## Verify
- [ ] Service account can perform only intended actions (403 on others).
- [ ] CI script exits non-zero on failed run and prints failing task ids.

## Checked

2026-11-02

- Confirmed: The Airflow API security page and the apache/airflow-client-python README were fetched.
- Removed or gated: The stable REST API reference page returned no text; endpoint paths, query parameters (start_date_gte, only_failed), the token endpoint and [api] settings are gated, confirm in the REST API reference for your version.

Method: documentation only; no commands were run.
