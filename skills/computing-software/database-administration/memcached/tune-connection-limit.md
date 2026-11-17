---
id: computing-software.database-administration.memcached.tune-connection-limit
name: tune-connection-limit
category: computing-software
field: database-administration
product: memcached
tags: [connection-limit, c, listen-disabled-num, maxconns, curr-connections]
level: practitioner
status: docs-checked
description: "Size the -c connection limit and detect exhaustion with listen_disabled_num, curr_connections and accepting_conns."
sources:
  - https://docs.memcached.org/serverguide/configuring/
  - https://docs.memcached.org/serverguide/maintenance/
  - https://docs.memcached.org/serverguide/performance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Default max concurrent connections is 1024 (`-c`). Extra connections may hang waiting for slots. Per-connection overhead is low (lower when idle), so setting it high is fine.

Sizing example: 5 web servers x Apache MaxClients 12 = 60 connections. Leave spare slots for admin tasks, new web servers and cron scripts.

Detect exhaustion with `stats`:
- `curr_connections`: keep well below `-c`.
- `listen_disabled_num`: times the limit was hit (the listener is disabled and new connections queue). Keep at or near zero.
- `accepting_conns`: 1 or 0 right now.
- `maxconns` in `stats settings` shows the active limit.

Other limits: one thread accepts new connections, so rapid connect/disconnect churn can overwhelm it (use persistent connections), and churn needs OS tuning for local ports and TIME_WAIT.

## Checked

Confirmed 2026-11-09: default of 1024 concurrent connections, extra connections may hang, low per-connection overhead, the 5 x 12 sizing example and spare slots, `listen_disabled_num`, `curr_connections` and `-c`, `accepting_conns` being 1 or 0, `maxconns` in `stats settings`, one accept thread and the need for persistent connections and OS tuning (Configuring, Maintenance and Performance pages). Nothing removed.

Method: docs-checked 2026-11-09 against docs.memcached.org Configuring, Maintenance and Performance pages
