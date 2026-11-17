---
id: computing-software.ai-ml-engineering.kubeflow.kubeflow-katib-env-variables
name: kubeflow-katib-env-variables
category: computing-software
field: ai-ml-engineering
product: kubeflow
tags: [env-variables, katib-core-namespace, db-manager, katib-mysql, postgres]
level: advanced
status: docs-checked
description: "Katib component environment variables: controller, UI and DB Manager settings, MySQL and PostgreSQL pairing rules, and how the DB Manager address is built."
sources: ["https://github.com/kubeflow/website/blob/master/content/en/docs/components/katib/user-guides/env-variables.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Katib env variables

Katib Controller and UI:
- `KATIB_CORE_NAMESPACE` (mandatory): base namespace for Katib components.
- `KATIB_DB_MANAGER_SERVICE_NAMESPACE` (defaults to the core namespace), `KATIB_DB_MANAGER_SERVICE_IP` (`katib-db-manager`), `KATIB_DB_MANAGER_SERVICE_PORT` (6789).
- Controller only: `KATIB_SUGGESTION_COMPOSER` (default `general`; you can supply your own).

Address expression: `IP.NAMESPACE:PORT`. If the namespace variable is the empty string, the address is `IP:PORT`. Change these three to use your own DB Manager.

Katib DB Manager:
- `DB_NAME` (mandatory): `mysql` or `postgres`, the only supported databases (custom backends implement the Katib DB interface).
- `DB_PASSWORD` (mandatory; defaults test for MySQL, katib for Postgres), `DB_USER` (root or katib).
- MySQL: `KATIB_MYSQL_DB_HOST` (`katib-mysql`), `KATIB_MYSQL_DB_PORT` (3306), `KATIB_MYSQL_DB_DATABASE` (katib).
- Postgres: `KATIB_POSTGRESQL_DB_HOST` (`katib-postgres`), port 5432, database katib, `KATIB_POSTGRESQL_SSL_MODE` (disable).
- `SKIP_DB_INITIALIZATION` (false).

The database containers must match the DB Manager:
- MySQL: `MYSQL_ROOT_PASSWORD` equals `DB_PASSWORD`, `MYSQL_DATABASE` equals `KATIB_MYSQL_DB_DATABASE`, plus `MYSQL_ALLOW_EMPTY_PASSWORD=true`.
- Postgres: `POSTGRES_USER` equals `DB_USER`, `POSTGRES_PASSWORD` equals `DB_PASSWORD`, `POSTGRES_DB` equals `KATIB_POSTGRESQL_DB_DATABASE`.

The `katib-mysql-secrets` value for `MYSQL_ROOT_PASSWORD` is "test" and the `katib-postgres-secrets` values are "katib"; the page says you can change `DB_PASSWORD` to your own.

## Checked

2026-11-08. Confirmed against the Katib environment variables page: every variable, default and mandatory flag for controller, UI, DB Manager and DB containers, the address expressions and the MySQL and Postgres pairing rules. Reworded the secrets sentence to match the page.
Method: docs-only read of cited pages, 2026-11-08
