---
id: computing-software.cybersecurity-defensive.dex.dex-storage-postgres
name: dex-storage-postgres
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [postgres, storage, sql, ssl]
level: practitioner
status: docs-checked
description: "Configure Dex Postgres storage with a dedicated database and user, and the ssl.mode setting which defaults to verify-full."
sources:
  - https://dexidp.io/docs/configuration/storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Give Dex its own Postgres database. It needs privileged access because it performs migrations, and its table names are not configurable, so sharing a database can cause name clashes.

```sql
CREATE DATABASE dex_db;
CREATE USER dex WITH PASSWORD 'change-me';
GRANT ALL PRIVILEGES ON DATABASE dex_db TO dex;
```

Dex config:

```yaml
storage:
  type: postgres
  config:
    host: localhost
    port: 5432
    database: dex_db
    user: dex
    password: change-me
    ssl:
      mode: verify-ca
      caFile: /etc/dex/postgres.ca
```

The SSL `mode` corresponds to the connection options of the `github.com/lib/pq` package. If unspecified, Dex defaults to the strictest mode, `verify-full`.

Gotchas:

- The example uses `verify-ca` with a `caFile`; leaving `ssl.mode` unset gives the strictest mode.
- Migrations run automatically on the first connection to the SQL server and cannot be rolled back, so Dex needs privileges to add and alter tables.
- Dex saves signing keys and bcrypt'd passwords in its storage, so use both transport security and database ACLs.

## Checked

2026-11-08. Read in full: the Dex Storage documentation page (SQL and Postgres sections). Confirmed: dedicated database reasons, the SQL example, the ssl.mode mapping to lib/pq with default verify-full, automatic non-reversible migrations, sensitive data warning. Removed: the advice to take a backup before upgrading, the environment-variable expansion tip and the closing check step (not on the page).

Method: documentation only; no commands were run.
