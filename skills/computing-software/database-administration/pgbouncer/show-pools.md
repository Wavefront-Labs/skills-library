---
id: computing-software.database-administration.pgbouncer.show-pools
name: show-pools
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, show-pools, monitoring, maxwait, pool-state]
level: practitioner
status: docs-checked
description: "SHOW POOLS columns (cl_active, cl_waiting, sv_idle, sv_used, maxwait, pool_mode) and how to read them."
sources:
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: read pool state from the admin console.

`SHOW POOLS;` returns one row per (database, user) pair. Columns:

- `database`, `user`.
- `cl_active`: clients linked to a server connection, or idle with nothing waiting.
- `cl_waiting`: clients that sent queries but have no server connection yet.
- `cl_active_cancel_req`: clients that forwarded a cancel to the server and await its response.
- `cl_waiting_cancel_req`: clients whose cancel has not been forwarded yet.
- `sv_active`: server connections linked to a client.
- `sv_active_cancel`: server connections forwarding a cancel request.
- `sv_being_canceled`: servers that would become idle but wait until all in-flight cancel requests against them complete.
- `sv_idle`: unused and immediately usable.
- `sv_used`: idle longer than server_check_delay, so server_check_query must run first.
- `sv_tested`: currently running server_reset_query or server_check_query.
- `sv_login`: currently logging in.
- `maxwait` and `maxwait_us`: how long the oldest queued client has waited (seconds and microsecond part). If it keeps increasing, the pool of servers is not handling requests fast enough: either an overloaded server or too small a pool_size.
- `pool_mode`: mode in use.
- `load_balance_hosts`: set when the host is a comma-separated list.

```
psql -p 6432 pgbouncer -c 'SHOW POOLS;'
```

Requires admin_users or stats_users membership.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. Removed: an unconfirmed saturation rule of thumb.

Method: documentation only; no commands were run.
