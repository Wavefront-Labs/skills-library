---
id: computing-software.data-engineering.apache-airflow.managing-connections-from-the-cli
name: managing-connections-from-the-cli
category: computing-software
field: data-engineering
product: apache-airflow
tags: [apache-airflow, airflow-connections-cli, connections, conn-uri, test-connection]
level: practitioner
status: docs-checked
description: "Create, export, import and test Airflow connections from the CLI and env vars: URI vs JSON formats, encoding gotchas, and enabling the test-connection feature."
sources:
  - https://airflow.apache.org/docs/apache-airflow/stable/howto/connection.html
  - https://airflow.apache.org/docs/apache-airflow/stable/cli-and-env-variables-ref.html#connections
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managing and testing connections from the CLI

**Goal:** script connection setup reproducibly (CI, local dev, migrations) instead of clicking in the UI.

## Add
```bash
airflow connections add warehouse_pg \
  --conn-type postgres --conn-host db.internal --conn-port 5432 \
  --conn-login etl --conn-password "$PG_PASS" --conn-schema analytics \
  --conn-extra '{"sslmode": "require"}'

airflow connections add s3_raw --conn-json '{"conn_type": "aws", "extra": {"region_name": "eu-west-1", "role_arn": "arn:aws:iam::123456789012:role/etl"}}'
```
`--conn-uri 'postgres://etl:p%40ss@db.internal:5432/analytics?sslmode=require'` also works; special characters in user/password must be **URL-encoded** (`@` -> `%40`, `/` -> `%2F`).

## Env vars (no DB row)
```bash
export AIRFLOW_CONN_WAREHOUSE_PG='postgres://etl:...@db.internal:5432/analytics'
export AIRFLOW_CONN_S3_RAW='{"conn_type": "aws", "extra": {"region_name": "eu-west-1"}}'   # JSON form
```
For lookup order and secrets backends, see the connections how-to in sources.

## Inspect, export, import
```bash
airflow connections get warehouse_pg -o json
airflow connections list -o table
airflow connections export conns.json            # format is inferred from the file extension
airflow connections import conns.json --overwrite
airflow connections delete old_conn
```
Treat export files as secrets; never commit them.

## Test
Testing is disabled by default since 2.7. Enable deliberately: `[core] test_connection = Enabled` (or `Hidden`/`Disabled`). Then `airflow connections test warehouse_pg`, or the Test button in the UI.

## Gotchas
- `conn_type` must match an installed provider (`airflow providers list`), otherwise hooks fail with unknown type.
- `extra` must be valid JSON; a stray quote silently becomes a string and options are ignored.
- The env var form is `AIRFLOW_CONN_<CONN_ID>`, for example `AIRFLOW_CONN_WAREHOUSE_PG` for the connection id `warehouse_pg`.

## Verify
`airflow connections get <id>` shows the expected host/extra from inside the worker image, and a one-task DAG using the hook succeeds.

## Checked

2026-10-28. Confirmed in the Airflow CLI reference and connections how-to: `airflow connections add/get/list/export/import/delete/test` and their flags (`--conn-json`, `--overwrite`, `-o` formats, export format from the file extension); `[core] test_connection` values Enabled/Hidden/Disabled, default Disabled, added in 2.7. Removed: unconfirmed lookup-order, password-in-export, hook-support and case-sensitivity claims, and the 2.3+ version note.
Method: documentation only; no commands were run.
