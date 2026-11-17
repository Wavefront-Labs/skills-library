---
id: computing-software.database-administration.pgbouncer.admin-console-set-command
name: admin-console-set-command
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, set, runtime-config, show-config, console]
level: practitioner
status: docs-checked
description: "Change PgBouncer settings at runtime with SET on the admin console and check which variables are changeable."
sources:
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: tune PgBouncer without a restart.

On the admin console (the virtual `pgbouncer` database), `SET key = arg;` changes a configuration setting. Examples from the docs:

```
SET log_connections = 1;
SET server_check_query = 'select 2';
```

Which settings can change? Run `SHOW CONFIG;`. Its columns are key, value, default and changeable. `changeable = yes` means the variable can be changed while running; `no` means boot time only (edit the file and restart).

Important distinction: SET on the pgbouncer console sets PgBouncer settings. A SET issued on any other database is passed to the PostgreSQL backend like any other SQL command.

The console supports only the simple query protocol, so drivers that use the extended protocol for every statement cannot issue these commands. Use psql:

```
psql -p 6432 pgbouncer -c "SET log_stats = 0;"
```

Requires a user in admin_users (stats_users are read-only: SHOW commands only).

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. Removed: an unstated claim about SET versus the ini file and RELOAD.

Method: documentation only; no commands were run.
