---
id: computing-software.ai-ml-engineering.mlflow.tracking-server-backend-and-artifact-stores
name: tracking-server-backend-and-artifact-stores
category: computing-software
field: ai-ml-engineering
product: mlflow
tags: [mlflow, experiment-tracking, mlflow-tracking-server, artifact-store, backend-store, proxied-artifacts, mlflow-db-upgrade]
level: practitioner
status: docs-checked
description: "Deploy a shared MLflow tracking server: SQL backend store, S3/GCS/Azure artifact store, proxied vs direct artifact access, auth, upgrades with mlflow db upgrade and scaling."
sources:
  - https://mlflow.org/docs/latest/self-hosting/architecture/tracking-server/
  - https://mlflow.org/docs/latest/self-hosting/architecture/artifact-store/
  - https://mlflow.org/docs/latest/self-hosting/architecture/backend-store/
  - https://mlflow.org/docs/latest/self-hosting/security/basic-http-auth/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MLflow tracking server with backend and artifact stores

## Architecture
- **Backend store** (runs, params, metrics, tags, registry): a relational database through SQLAlchemy (`sqlite`, `postgresql`, `mysql`, `mssql`); SQLite (`sqlite:///mlflow.db`) is the default when none is given. The file-based `./mlruns` store is in maintenance mode, and since 3.13.0 pointing the tracking or registry store at a local file path raises an error unless `MLFLOW_ALLOW_FILE_STORE=true`.
- **Artifact store** (models, plots, files): Amazon S3 and compatible storage, Azure Blob Storage, Google Cloud Storage, Backblaze B2, an SFTP server or NFS.
- **Server**: `mlflow server` (uvicorn-based; `--uvicorn-opts` passes options, and `--gunicorn-opts` remains for gunicorn users) behind TLS and auth.

## Start the server (proxied artifacts)
```bash
pip install mlflow psycopg2-binary boto3
mlflow server \
  --backend-store-uri postgresql://mlflow:${PW}@db:5432/mlflow \
  --artifacts-destination s3://ml-artifacts/mlflow \
  --host 0.0.0.0 --port 5000 --workers 4
```
With proxied access (default `--serve-artifacts`), clients upload/download artifacts **through the server** using `mlflow-artifacts:/` URIs; only the server needs cloud credentials. Direct access (`--no-serve-artifacts --default-artifact-root s3://...`) makes clients talk to S3 themselves, so every client needs bucket credentials. `--artifacts-only` runs a dedicated artifact proxy.

Clients: `export MLFLOW_TRACKING_URI=https://mlflow.internal` (or `mlflow.set_tracking_uri`).

## Gotchas
- `--default-artifact-root` applies to new experiments only; changing server flags later does not affect already-created experiments (each experiment records its own `artifact_location`).
- Do not rely on the default backend (SQLite in the current docs); always pass `--backend-store-uri` explicitly for a shared server.
- Upgrading MLflow may require schema migrations: `mlflow server` fails against a database with an out-of-date schema, so back up the DB and run `mlflow db upgrade postgresql://...` before starting the new version (schema migrations can cause downtime).
- Large artifact uploads through the proxy can hit timeouts; the docs describe multipart upload for proxied access (`MLFLOW_ENABLE_PROXY_MULTIPART_UPLOAD=true`, with `MLFLOW_MULTIPART_UPLOAD_MINIMUM_FILE_SIZE` and `MLFLOW_MULTIPART_UPLOAD_CHUNK_SIZE`) and `--uvicorn-opts "--timeout-keep-alive=120"` for keep-alive timeouts.
- Auth: built-in basic auth (`mlflow server --app-name basic-auth`, with roles and permissions) or SSO through a plugin or reverse proxy; see the authentication skill.

## Verify
- [ ] From a laptop with no cloud credentials, `mlflow.log_artifact` and `mlflow.artifacts.download_artifacts` work (proxy path).
- [ ] DB backup and restore tested; `mlflow db upgrade` rehearsed on a copy.
- [ ] Server availability monitored (for example an HTTP check against the server's URL).

## Checked

- Date: 2026-10-25. Release: MLflow 3.17.2 (released 2026-10-20); documentation and source read from the master branch of mlflow/mlflow (docs/docs, mlflow/, CHANGELOG.md) on 2026-10-25.
- SQLAlchemy dialects, SQLite default, file store maintenance mode, `mlflow db upgrade` before starting, schema-migration downtime: docs/self-hosting/architecture/backend-store.mdx. File-store error and `MLFLOW_ALLOW_FILE_STORE=true` in 3.13.0: CHANGELOG.md.
- Supported artifact stores, `--artifacts-destination`, proxied serving by default, multipart upload env vars, default artifact location warning: docs/self-hosting/architecture/artifact-store.mdx and tracking-server.mdx; `--serve-artifacts/--no-serve-artifacts` (default on), `--artifacts-only`, `--default-artifact-root` (new experiments only), `--workers` default 4: mlflow/cli/__init__.py and mlflow/utils/cli_args.py.
- `--uvicorn-opts` timeout example and gunicorn note: tracking-server.mdx.
- Removed as unconfirmed: HDFS as a store, the registry/concurrency criticism of the file store, the speed claim for direct access, client/server version-compatibility claims, nginx body-limit advice, managed-service options and the `/health` path. The three dead `tracking/*.html` links were replaced with the self-hosting pages.

Method: documentation only; no commands were run.
