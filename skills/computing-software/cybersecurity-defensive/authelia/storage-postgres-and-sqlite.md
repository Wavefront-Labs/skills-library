---
id: computing-software.cybersecurity-defensive.authelia.storage-postgres-and-sqlite
name: storage-postgres-and-sqlite
category: computing-software
field: cybersecurity-defensive
product: authelia
tags: [authelia, storage, postgresql, sqlite, encryption-key, high-availability, database]
level: practitioner
status: docs-checked
description: "Choose Authelia's storage backend, configure PostgreSQL with fallback servers or local SQLite, and set the required storage encryption key."
sources:
  - https://www.authelia.com/configuration/storage/introduction/
  - https://www.authelia.com/configuration/storage/postgres/
  - https://www.authelia.com/configuration/storage/sqlite/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Authelia stores user preferences, 2FA device handles and secrets, authentication logs and similar state in SQL. Providers are `postgres`, `mysql` and `local` (SQLite). All need `storage.encryption_key`, which encrypts sensitive columns at the application level. The minimum is 20 characters; use a random alphanumeric string of 64 or more.

SQLite:

```yaml
storage:
  encryption_key: '<STORAGE_ENCRYPTION_KEY>'
  local:
    path: '/config/db.sqlite3'
```

It is created if absent. The file is local, so you cannot run several Authelia instances against it, and the documentation recommends an external database for high availability and production.

PostgreSQL:

```yaml
storage:
  encryption_key: '<STORAGE_ENCRYPTION_KEY>'
  postgres:
    address: 'tcp://127.0.0.1:5432'
    database: 'authelia'
    schema: 'public'
    username: 'authelia'
    password: '<DB_PASSWORD>'
```

`address` is required and may use a `tcp` scheme or the `unix` scheme (for example `unix:///var/run/postgres.sock`); IPv6 goes in brackets. `database` and `username` are required, `schema` defaults to `public`, `timeout` to 5 seconds, and a `tls` block enables TLS (system trust store, extendable with `certificates_directory`). The password can be a secret and a random 64+ character string is recommended. The `servers` list adds fallback instances, each with its own `address` and `tls`. Every other setting, including database, schema, username and password, must match the primary, and the servers must be fully replicated.

The key performs application-level, column-specific encryption of sensitive values, so keeping a separate backup of it is sensible (this follows from that design; the pages do not state it).

Check: run `authelia storage schema-info` against the configuration and confirm it connects and shows the storage schema information (the CLI reference describes it as diagnostic storage information; it is not on the cited configuration pages).

## Checked

2026-11-08. Read in full: storage introduction, postgres, sqlite. Corrected the description of what storage holds, added PostgreSQL option defaults; schema-info wording verified against its CLI page.

Method: documentation only; no commands were run.
