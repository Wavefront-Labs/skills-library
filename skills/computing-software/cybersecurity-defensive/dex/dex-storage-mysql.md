---
id: computing-software.cybersecurity-defensive.dex.dex-storage-mysql
name: dex-storage-mysql
category: computing-software
field: cybersecurity-defensive
product: dex
tags: [mysql, storage, sql, ssl]
level: practitioner
status: docs-checked
description: "Configure Dex MySQL storage (5.7 or later) with a dedicated database and the ssl.mode setting that defaults to true."
sources:
  - https://dexidp.io/docs/configuration/storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dex requires MySQL 5.7 or later. As with Postgres, dedicate a database to Dex: it needs privileged access for migrations and its table names are not configurable, so sharing may cause name clashes.

```sql
CREATE DATABASE dex_db;
CREATE USER dex IDENTIFIED BY 'change-me';
GRANT ALL PRIVILEGES ON dex_db.* TO dex;
```

Dex config:

```yaml
storage:
  type: mysql
  config:
    database: dex_db
    user: dex
    password: change-me
    ssl:
      mode: custom
      caFile: /etc/dex/mysql.ca
```

The SSL `mode` corresponds to the connection options of the `github.com/go-sql-driver/mysql` package. If unspecified, Dex defaults to the strictest mode, `true`.

Notes:

- Migrations run automatically on the first connection and cannot be rolled back.
- Dex stores signing keys and bcrypt'd passwords in its storage, so use both transport security (TLS) and database ACLs.

Gotcha: Dex needs privileges to add and alter tables for its migrations, so grant privileges on the whole `dex_db` schema as shown.

## Checked

2026-11-08. Read in full: the Dex Storage documentation page (SQL and MySQL sections). Confirmed: MySQL 5.7 or later, dedicated database reasons, the example SQL and config, the ssl.mode mapping to go-sql-driver/mysql with default `true`, automatic non-reversible migrations, sensitive data warning. Removed: the backup advice and the statement about what caFile does in custom mode (the page shows only the example).

Method: documentation only; no commands were run.
