---
id: computing-software.database-administration.pgbouncer.reserve-pool-behaviour
name: reserve-pool-behaviour
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, reserve-pool, reserve-pool-size, reserve-pool-timeout, queueing]
level: advanced
status: docs-checked
description: "How the reserve pool absorbs bursts: reserve_pool_size, reserve_pool_timeout and per-database or per-user overrides."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: allow temporary extra server connections for clients stuck waiting.

`reserve_pool_size` (default 0, disabled) is how many additional connections a pool may use once clients have waited too long. `reserve_pool_timeout` (default 5.0 seconds, 0 disables) defines "too long": if a client has not been serviced in this time, connections from the reserve pool may be used.

Resolution order for reserve_pool_size: [users] value, else [databases] value (alias `reserve_pool`), else the global value.

```
[pgbouncer]
default_pool_size = 20
reserve_pool_size = 5
reserve_pool_timeout = 3

[databases]
app = host=db1 reserve_pool_size=10
```

With these settings a pool for app may open up to 20 normal connections plus extra ones from its reserve when a client waits more than 3 seconds.

Diagnose via SHOW POOLS: `cl_waiting` and `maxwait` show queued clients; sustained use of reserve connections means pool_size is too small or the server is slow. Clients that wait longer than query_wait_timeout (default 120 s) are disconnected.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. Removed: a padded SHOW DATABASES comparison line.

Method: documentation only; no commands were run.
