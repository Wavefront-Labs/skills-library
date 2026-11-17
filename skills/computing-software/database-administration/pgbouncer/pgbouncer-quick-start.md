---
id: computing-software.database-administration.pgbouncer.pgbouncer-quick-start
name: pgbouncer-quick-start
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, quick-start, pgbouncer-ini, userlist, setup]
level: intro
status: docs-checked
description: "Minimal PgBouncer setup: pgbouncer.ini, userlist.txt, launching with -d, connecting with psql and reaching the admin console."
sources:
  - https://www.pgbouncer.org/usage.html
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: get a working PgBouncer in front of one PostgreSQL database and confirm you can reach the admin console.

Create a pgbouncer.ini:

```
[databases]
template1 = host=localhost port=5432 dbname=template1

[pgbouncer]
listen_port = 6432
listen_addr = localhost
auth_type = md5
auth_file = userlist.txt
logfile = pgbouncer.log
pidfile = pgbouncer.pid
admin_users = someuser
```

Create userlist.txt with the users allowed in, one per line, in the form `"someuser" "same_password_as_in_server"`.

Launch it in the background:

```
pgbouncer -d pgbouncer.ini
```

Daemon mode (-d) requires pidfile and either logfile or syslog; no log messages go to stderr after it backgrounds.

Point the application, or psql, at the PgBouncer port instead of PostgreSQL:

```
psql -p 6432 -U someuser template1
```

Manage PgBouncer by connecting to the special virtual database named pgbouncer and running SHOW HELP;:

```
psql -p 6432 -U someuser pgbouncer
```

After editing pgbouncer.ini, apply the change with RELOAD; on the console. The defaults are listen_port 6432 and pool_mode session. The pgbouncer database name is reserved for the console and cannot be used as a key in [databases].

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
