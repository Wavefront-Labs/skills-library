---
id: computing-software.data-engineering.apache-airflow.config-via-environment-variables
name: config-via-environment-variables
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow, airflow-config-env, airflow-cfg, environment-variables, config-precedence, cmd-secret-suffix, airflow-config-list]
level: practitioner
status: docs-checked
description: "Configure Airflow through AIRFLOW__SECTION__KEY environment variables, _CMD and _SECRET suffixes, config precedence, and inspect effective values with airflow config."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/howto/set-config.html
  - https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Airflow config via environment variables

**Goal:** manage Airflow settings in containers/Helm without editing `airflow.cfg`, and know which value is effective.

## Naming
`AIRFLOW__{SECTION}__{KEY}` (double underscores, uppercase):
```bash
AIRFLOW__CORE__PARALLELISM=64
AIRFLOW__DAG_PROCESSOR__MIN_FILE_PROCESS_INTERVAL=60
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://...
AIRFLOW__LOGGING__REMOTE_LOGGING=True
AIRFLOW__CELERY__WORKER_CONCURRENCY=16
```
Connections and variables have their own env forms (not config): `AIRFLOW_CONN_<CONN_ID>` (URI or JSON) and `AIRFLOW_VAR_<KEY>`.

## Secret values without plaintext env
Supported for sensitive keys (e.g. `sql_alchemy_conn`, `fernet_key`, `broker_url`, `result_backend`, `secret_key`):
```bash
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN_CMD='cat /run/secrets/db_uri'
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN_SECRET='airflow/db-uri'     # read from configured secrets backend
```

## Precedence (highest first)
1. `AIRFLOW__SECTION__KEY` env var
2. `AIRFLOW__SECTION__KEY_CMD` env var
3. `AIRFLOW__SECTION__KEY_SECRET` env var
4. Value in `airflow.cfg`
5. `_cmd` in airflow.cfg
6. `_secret` in airflow.cfg
7. Airflow's built-in default

## Inspect effective config
```bash
airflow config get-value core parallelism
airflow config list --section scheduler
airflow config list --include-sources       # shows where each value came from (env var, airflow.cfg, default)
airflow config lint                         # Airflow 3 migration: flags removed/renamed options
```
The UI config view is controlled by `[api] expose_config`; keep it `False`, or `True` (sensitive values are masked).

## Gotchas
- Every component needs the same core settings; setting an env var only on the scheduler pod is a classic split-brain (e.g. different `fernet_key`, different `dags_folder`).
- Sections move between versions (for example the DAG parsing keys now live in `[dag_processor]`); run `airflow config lint` when migrating from Airflow 2.x to 3.0.

## Verify
- [ ] `airflow config list --include-sources` on each component shows identical values for shared keys.
- [ ] No secrets appear as plaintext env in pod specs (use _CMD/_SECRET or k8s secretKeyRef).

## Checked

2026-10-28. Confirmed in the Airflow set-config how-to, configuration reference and CLI reference: `AIRFLOW__{SECTION}__{KEY}` plus `_CMD` and `_SECRET` forms and the documented precedence order, `sql_alchemy_conn`/`fernet_key`/`broker_url` as supported keys, `airflow config get-value/list/lint`, `--include-sources`, `[api] expose_config` values, `AIRFLOW_CONN_<CONN_ID>` and `AIRFLOW_VAR_<KEY>`. Removed: the `[webserver] expose_config` mention and default claim, the Helm values example, the boolean-string gotcha, and the Airflow 3 section-move generalisation.
Method: documentation only; no commands were run.
