---
id: computing-software.collaboration-platform-administration.vikunja.config-database-options
name: config-database-options
category: computing-software
field: collaboration-platform-administration
product: vikunja
tags: [vikunja, database-section, postgres-ssl, connection-pool, pg-schema]
level: practitioner
status: docs-checked
description: "Reference for Vikunja's database.* options: type, credentials, SQLite path resolution, connection pool limits, PostgreSQL SSL and schema, MySQL TLS."
sources:
  - https://raw.githubusercontent.com/go-vikunja/vikunja/main/config-raw.json
  - https://raw.githubusercontent.com/go-vikunja/website/main/src/content/docs/setup/install.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`database.type`: `mysql`, `postgres` or `sqlite` (default). Defaults: `user` vikunja, `host` localhost, `database` vikunja, `password` empty.

SQLite: `database.path` default `./vikunja.db`. Relative paths resolve against the pinned config's directory (when the config was pinned with `--config` and the value is not set explicitly), else an explicit `service.rootpath`, else a per-user data directory (Linux `$XDG_DATA_HOME/vikunja` or `~/.local/share/vikunja`). Use an absolute path in production, especially as a Windows service.

Pool: `maxopenconnections` 100 (mysql and postgres only), `maxidleconnections` 50, `maxconnectionlifetime` 1800000 (milliseconds).

PostgreSQL only: `sslmode` (default `disable`), `sslcert`, `sslkey`, `sslrootcert`, and `schema` (default `public`). If tables were created in another schema, set `schema` to match; Vikunja pins the connection `search_path` to it.

MySQL: `tls` accepts false (default), true, skip-verify, preferred.

Versions: the config reference says MySQL 8.0+, MariaDB 10.2+, PostgreSQL 12+; the install page lists the oldest versions that should work as MySQL 8.0 (5.7 is not supported), MariaDB 10.2, PostgreSQL 9.5, and says only the CI versions are tested: MySQL 8, MariaDB 12, PostgreSQL 18 and bundled SQLite.

## Checked

2026-11-04: all options and defaults checked against config-raw.json (database section) and the install page (versions). The two pages disagree on the PostgreSQL minimum, so both are stated.

Method: documentation only; no commands were run.
