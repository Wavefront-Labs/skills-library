---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-pipelines-database-config
name: kubeflow-pipelines-database-config
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [pipelines-database, mysql, postgresql-overlay, mlmd]
level: advanced
status: docs-checked
description: "KFP database configuration: MySQL as the supported default, PostgreSQL overlays for development only, and which PostgreSQL combinations are unavailable."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/pipelines/operator-guides/configure-database.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Pipelines database config

KFP stores pipeline definitions, run history and other metadata in a relational database accessed mainly by the API server.

**MySQL** is the default and fully supported backend, configured automatically by the standard kustomize manifests (`env/platform-agnostic` plus the cluster-scoped resources). The overlays for proxy-enabled, cache-disabled, pod-to-pod TLS and artifact proxy configurations assume MySQL.

**PostgreSQL** is for development and evaluation only and is not supported for production KFP 2.18, which still depends on ML Metadata (MLMD) whose PostgreSQL backend has limitations. Components use the `pgx` driver. Available overlays:
- `manifests/kustomize/env/platform-agnostic-postgresql` (standalone, single user)
- `manifests/kustomize/env/platform-agnostic-multi-user-postgresql` (multi-user)

Both are configured with execution cache enabled, proxy disabled and pod-to-pod TLS disabled.

No PostgreSQL overlay exists for:
- Standalone with pod-to-pod TLS, with execution cache disabled, or with proxy enabled.
- Multi-user with execution cache disabled, or with artifact proxy enabled.

The project CI deployment script rejects these combinations explicitly and does not test them. Pod-to-pod TLS is not available with PostgreSQL at all: the only TLS overlay (`platform-agnostic-standalone-tls`) is standalone and MySQL based, and no multi-user TLS overlay exists regardless of database.

sslmode: the API server needs `sslmode` set explicitly in the PostgreSQL connection parameters or it will not start; the base overlay leaves it unset. Patch both the API server (env `DBCONFIG_POSTGRESQLCONFIG_EXTRAPARAMS`) and the cache server (`--db_extra_params`), for example `{"sslmode":"disable"}` for local development and `verify-full` (or another PostgreSQL sslmode) with TLS certificates.

The page says KFP 2.18 release images do not include PostgreSQL configuration, so a development setup uses manifests and images built from master (a mutable tag); do not use that path for production.

## Checked

2026-11-08. Confirmed against the Database Configuration page: MySQL default, PostgreSQL development-only warning, the two overlays, the unavailable combinations table, the TLS notes, sslmode and the master-image caveat.
Method: docs-only read of cited pages, 2026-11-08
