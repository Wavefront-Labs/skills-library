---
id: computing-software.messaging-and-integration.prosody.sql-storage-config
name: sql-storage-config
category: computing-software
field: messaging-and-integration
product: prosody
tags: [prosody, xmpp, sql, postgresql, sqlite, mysql, storage]
level: practitioner
status: docs-checked
description: "Configure Prosody SQL storage: the sql table with driver, database, host, port, username, password, supported drivers, and automatic table management."
sources:
  - https://prosody.im/doc/modules/mod_storage_sql
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQL storage config

```lua
storage = "sql"
sql = {
    driver = "PostgreSQL"; -- or "SQLite3" / "MySQL" (case sensitive)
    database = "prosody";
    host = "localhost"; -- delete this line for Postgres
    port = 3306;
    username = "prosody";
    password = "secretpassword";
}
```

- Default is `sql = { driver = "SQLite3", database = "prosody.sqlite" }`; for SQLite3, `database` is a filename relative to the data directory.
- SQLite3 and PostgreSQL are officially supported; MySQL/MariaDB "may work but is not recommended".
- With enough permission, Prosody creates tables and indexes in an empty database and upgrades the schema itself. Grant SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX.
- `sql_manage_tables = false` stops it managing tables (default `true`).

- The LuaDBI library must be available on the system.

## Checked

2026-11-04: confirmed against prosody.im/doc/modules/mod_storage_sql (config block, defaults, supported databases, permissions list, sql_manage_tables). Added the LuaDBI requirement and removed a generic verify line.
Method: documentation only; no commands were run.
