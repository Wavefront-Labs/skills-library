---
id: computing-software.database-administration.pgbouncer.reconnect-kill-and-wait-close
name: reconnect-kill-and-wait-close
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, reconnect, kill, kill-client, wait-close]
level: advanced
status: docs-checked
description: "RECONNECT, KILL, KILL_CLIENT and WAIT_CLOSE: switching servers gradually or abruptly and waiting for close_needed to clear."
sources:
  - https://www.pgbouncer.org/usage.html
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: move traffic to a new destination or drop connections.

- `RECONNECT [db];`: close each open server connection for the database (or all) after it is released per the pooling mode, even if its lifetime is not up. New connections can open immediately. Use it when the server connection setup changed, for gradual switchover. Not needed after a pgbouncer.ini change plus reload, or after DNS changes, because the equivalent runs automatically; it is needed only when something downstream of PgBouncer routes connections (for example HAProxy). Afterwards some connections may go to the old destination and some to the new one, sensible mainly for read-only replicas or multimaster nodes. For an all-at-once switch use PAUSE instead.
- `KILL [db];`: immediately drop all client and server connections for the database, or all databases, excluding the admin database. New client connections to a killed database wait until RESUME. Use it in emergency failover instead of waiting.
- `KILL_CLIENT id;`: immediately kill one client and its server connections, where id comes from SHOW CLIENTS (for example `KILL_CLIENT 1234`).
- `WAIT_CLOSE [db];`: wait until all server connections for the database (or all) clear the `close_needed` state shown in SHOW SERVERS. Call it after RECONNECT or RELOAD to be sure a change is fully active, for example in switchover scripts.

```
RECONNECT app;
WAIT_CLOSE app;
```

`server_fast_close` makes session-pooled idle servers in close_needed close sooner, at the cost of interrupting idle client sessions.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
