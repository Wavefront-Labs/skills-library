---
id: computing-software.data-engineering.prefect.server-database
name: server-database
category: computing-software
field: data-engineering
product: prefect
tags: [server, postgres, sqlite, migrations, version-compatibility]
level: practitioner
status: docs-checked
description: "Self-hosted Prefect server architecture: SQLite versus PostgreSQL requirements, what the database stores, migrations and client/server compatibility."
sources:
  - https://docs.prefect.io/v3/concepts/server
  - https://docs.prefect.io/v3/concepts/settings-and-profiles
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose and operate the server database.

A self-hosted server is backed by a database and includes a UI. It shares a capability set with Prefect Cloud; Cloud adds RBAC, audit logs and SSO.

Version compatibility: use the same `prefect` version on client and server. Older clients work with newer servers; newer clients may not work with older servers because new REST API fields are added, and the server typically returns HTTP 422.

Database:
- SQLite (default): lightweight, single-server, almost no setup.
- PostgreSQL: production, high availability, multi-server. Requires PostgreSQL 14.9 or higher and the `pg_trgm` extension installed and enabled.

Set it with the `server.database.connection_url` setting (SQLAlchemy format).

Persisted data: flow and task run state and history, logs, deployments, flow and task run concurrency limits, storage blocks for results, variables, artifacts, work pool status, events, automations.

Migrations use Alembic. The server runs needed migrations automatically at startup, and they can also be run manually from the CLI.

Scaling: run multiple server instances for high availability (see the scaling guide). The concept page does not give ports, URLs or service names.

## Checked

2026-11-08. Client and server version guidance, persisted data list, SQLite and PostgreSQL requirements, pg_trgm and Alembic migrations confirmed on the server page; server.database.connection_url confirmed on the settings and profiles page (added as a source).

Method: documentation only; no commands were run.
