---
id: computing-software.database-administration.pgbouncer.console-access-control
name: console-access-control
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, admin-users, stats-users, console, access]
level: practitioner
status: docs-checked
description: "Who may log in to the pgbouncer admin console: admin_users, stats_users, auth_type any and the passwordless pgbouncer user."
sources:
  - https://www.pgbouncer.org/usage.html
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: restrict access to the admin console.

The console is a virtual database named `pgbouncer`:

```
psql -p 6432 pgbouncer
```

- `admin_users` (default empty): comma-separated database users allowed to connect and run all console commands. Ignored when auth_type is any, in which case any user name gets in as admin (per the config docs).
- `stats_users` (default empty): users allowed to run read-only queries on the console, meaning all SHOW commands.

The usage docs add: with `auth_type=any`, any user is allowed in as a stats_user.

Additionally, the user name `pgbouncer` may log in without a password if the login comes via the Unix socket and the client has the same Unix user UID as the running process.

The console supports only the simple query protocol. Drivers that use the extended query protocol for all commands will not work against it.

A `SET` run on the pgbouncer database changes PgBouncer settings, while a SET on any other database is passed through to PostgreSQL like any other SQL.

```
[pgbouncer]
admin_users = dbadmin
stats_users = metrics_reader, stat_collector
```

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
