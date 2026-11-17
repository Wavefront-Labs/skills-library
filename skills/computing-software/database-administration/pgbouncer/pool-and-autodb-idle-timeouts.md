---
id: computing-software.database-administration.pgbouncer.pool-and-autodb-idle-timeouts
name: pool-and-autodb-idle-timeouts
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, autodb-idle-timeout, pool-idle-timeout, stats, wildcard-database]
level: advanced
status: docs-checked
description: "autodb_idle_timeout and pool_idle_timeout: freeing idle pools and why statistics are forgotten."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control when unused pools and auto-created databases are freed.

- `autodb_idle_timeout` (default 3600.0 s): automatically created databases, from the `*` fallback entry, whose pools have been unused this long are freed. The downside: their statistics are forgotten.
- `pool_idle_timeout` (default 0, disabled): a pool (one database/user pair) with no client connections and no server connections for this many seconds is freed. Similar to autodb_idle_timeout but frees individual pools rather than whole auto-created databases. Unlike server_idle_timeout, which closes idle server connections but keeps the pool, this frees the whole pool and only once it is completely empty.

Because the per-database totals in SHOW STATS are the sum over currently existing pools, freeing a pool makes those totals decrease, which monitoring systems may misread as a counter reset. That is why pool_idle_timeout is disabled by default.

The `*` fallback database in [databases]:

```
[databases]
* = host=foo
```

A connection asking for database `bar` then behaves as if `bar = host=foo dbname=bar` existed. These auto-created entries are cleaned up after autodb_idle_timeout of idleness.

Check what exists with SHOW DATABASES and SHOW POOLS, and counts of pools in SHOW LISTS.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
