---
id: computing-software.messaging-and-integration.celery.celery-database-result-backend
name: celery-database-result-backend
category: computing-software
field: messaging-and-integration
product: celery
tags: [celery-conf-database-backend, celery, sqlalchemy, result-backend, celery-taskmeta, engine-options, mysql, postgresql]
level: practitioner
status: docs-checked
description: "Configure the Celery SQLAlchemy database result backend: URL, engine options, table names and schemas, 5.7 migrations and retries."
sources:
  - https://docs.celeryq.dev/en/stable/userguide/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Database (SQLAlchemy) result backend

Goal: store results in a relational database and handle the 5.x/5.7 schema changes.

## URL
Prefix the SQLAlchemy connection string with `db+`:

```python
result_backend = 'db+sqlite:///results.sqlite'
result_backend = 'db+mysql://scott:tiger@localhost/foo'
result_backend = 'db+postgresql://scott:tiger@localhost/mydatabase'
result_backend = 'db+oracle://scott:tiger@127.0.0.1:1521/sidname'
```

## Settings
- `database_create_tables_at_setup` (5.5.0+, default `True`): create tables during setup; `False` creates them lazily on the first task (the behaviour before 5.5).
- `database_engine_options` (default `{'pool_pre_ping': True, 'pool_recycle': 3600}`; was `{}` before 5.7): avoids `(OperationalError) (2006, 'MySQL server has gone away')`. Disable with `{'pool_pre_ping': False, 'pool_recycle': None}`; `{'echo': True}` logs SQL.
- `database_short_lived_sessions` (default disabled): can drastically reduce performance; use on low-traffic workers whose cached connections go stale.
- `database_table_names`: `{'task': 'myapp_taskmeta', 'group': 'myapp_groupmeta'}`.
- `database_table_schemas`: `{'task': 'celery', 'group': 'celery'}`.
- `database_engine_callback` (5.7+, default `None`): callable or dotted path (`'myapp.db:register_do_connect'`) receiving the engine right after creation, e.g. to add a `do_connect` listener injecting an IAM or JWT password.

## 5.7 behaviour changes
- Retries use the unified backend mechanism with `result_backend_always_retry=True` and `result_backend_max_retries=3` by default; override e.g. `result_backend_always_retry = False` or `result_backend_max_retries = 10`.
- The backend honors `result_serializer`; before 5.7 the `result` column was always a pickle. Old rows still read correctly; no schema change.
- Task children are stored in a `children` column of `celery_taskmeta`. Celery tries to add it at startup; without DDL permissions run `ALTER TABLE celery_taskmeta ADD COLUMN children BLOB;` (`BYTEA` on PostgreSQL).
- `result_extended=True` needs a `stamps` column (see the backend retry skill).
- Upgrading from 5.6 or earlier: `date_done` has no index, and `celery.backend_cleanup` queries it. `create_all()` will not alter tables, so add indexes yourself: `CREATE INDEX ix_celery_taskmeta_date_done ON celery_taskmeta (date_done);` and `CREATE INDEX ix_celery_tasksetmeta_date_done ON celery_tasksetmeta (date_done);` (or Alembic `op.create_index`).
- `result_expires` cleanup needs `celery beat` running with this backend.

## Checked

2026-11-07. Confirmed against the Celery 5.7.0 stable docs (userguide/configuration.html): the settings, defaults, parameters, code and wording kept in this skill. These are the pages' own claims, not independent tests. Nothing needed removing.

Method: documentation only; no commands were run.
