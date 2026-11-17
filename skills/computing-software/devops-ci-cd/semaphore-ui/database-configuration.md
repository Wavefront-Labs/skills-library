---
id: computing-software.devops-ci-cd.semaphore-ui.database-configuration
name: database-configuration
category: computing-software
field: devops-ci-cd
product: semaphore-ui
tags: [database, mysql, postgres, sqlite, dialect, semaphore-ui]
level: practitioner
status: docs-checked
description: "Choose and configure the Semaphore database dialect and connection options, including Postgres sslmode."
sources:
  - https://semaphoreui.com/docs/reference/configuration
  - https://semaphoreui.com/docs/admin-guide/ha
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Configure the Semaphore database

Goal: point Semaphore at MySQL, Postgres or SQLite.

Semaphore creates and migrates its own tables on start. Choose the dialect before the first run; changing it later means migrating data yourself. `dialect` is one of `mysql`, `postgres`, `sqlite` (the reference lists `sqlite` as the default).

| Config key | Variable | Default |
|---|---|---|
| `<dialect>.host` | `SEMAPHORE_DB_HOST` | `0.0.0.0` (for SQLite, the file path) |
| `<dialect>.user` | `SEMAPHORE_DB_USER` | none (unused for SQLite) |
| `<dialect>.pass` | `SEMAPHORE_DB_PASS` | none |
| `<dialect>.name` | `SEMAPHORE_DB` | `semaphore` |
| `<dialect>.options` | `SEMAPHORE_DB_OPTIONS` | object of driver options |
| `dialect` | `SEMAPHORE_DB_DIALECT` | `sqlite` |

Postgres with explicit options:

```json
{
  "dialect": "postgres",
  "postgres": {
    "host": "localhost",
    "user": "postgres",
    "pass": "pwd",
    "name": "semaphore",
    "options": { "sslmode": "disable" }
  }
}
```

If startup panics with `pq: SSL is not enabled on the server`, your Postgres does not serve SSL; add `sslmode: disable` under `options` as above.

Gotchas:
- SQLite and BoltDB are not supported for HA; use PostgreSQL or MySQL.
- Back up the encryption keys (`access_key_encryption` or the key registry) separately from the database, which is unreadable without them.

Verify: the server starts and migrations complete with no database error in the log.

## Checked

2026-11-04: checked against the config file, environment variable, security and high availability pages. Removed the unconfirmed SSL aside and the unconfirmed backup-before-upgrade advice; kept the documented key backup point.

Method: documentation only; no commands were run.
