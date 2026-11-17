---
id: computing-software.database-administration.memcached.key-health-stats
name: key-health-stats
category: computing-software
field: database-administration
product: memcached
tags: [health-stats, curr-connections, cmd-flush, limit-maxbytes, monitoring]
level: practitioner
status: docs-checked
description: "Which memcached stats to watch for server health: connections, listen_disabled_num, limit_maxbytes, cmd_flush, swap and network."
sources:
  - https://docs.memcached.org/serverguide/maintenance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

From the `stats` command (Maintenance page):
- `curr_connections`: clients presently connected; make sure it does not come too close to your max connection setting (-c).
- `listen_disabled_num`: times memcached hit its connection limit and disabled its listener (new connections wait in a queue); keep it at or close to zero.
- `accepting_conns`: 1 or 0, whether the server has hit max connections.
- `limit_maxbytes`: verifies the -m argument took; init scripts can be misconfigured so memcached starts with default values.
- `cmd_flush`: incremented every time someone issues `flush_all`; watch it in production and sound the alarms if it moves unless intended, since debug code or misinformed people can leave scripts invalidating the entire cache.

Active probing: monitoring scripts should ideally issue test sets/gets/deletes occasionally and time each. Slow to connect suggests a connection or network problem; slow to respond suggests the server might be swapping or in ill health.

OS: watch swap usage (severe performance degradation) and the network stack (dropped packets, underruns, CRC errors, switch per-port counters). Degraded performance can trace to bad wiring, a bad switchport, a dying NIC or a driver in need of tuning.

Upgrading: most minor releases fix bugs and add instrumentation; it is often better to upgrade early so you have the extra instrumentation when you need it. Follow the release notes.

## Checked

2026-11-04. Confirmed against the Maintenance page (Watching Server Health, OS Health, Upgrading). Removed: nothing; wording tightened.

Method: documentation only; no commands were run.
