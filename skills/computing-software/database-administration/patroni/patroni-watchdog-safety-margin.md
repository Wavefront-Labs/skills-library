---
id: computing-software.database-administration.patroni.patroni-watchdog-safety-margin
name: patroni-watchdog-safety-margin
category: computing-software
field: database-administration
product: patroni
tags: [patroni, watchdog, safety-margin, ttl, timing]
level: sme
status: docs-checked
description: "Reason about watchdog expiry versus ttl, and when to use safety_margin -1."
sources:
  - https://patroni.readthedocs.io/en/latest/watchdog.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: size the watchdog window so it fires before the leader key expires.

By default Patroni sets the watchdog to expire 5 seconds before the TTL expires. With `loop_wait=10` and `ttl=30` the HA loop has at least 15 seconds (`ttl - safety_margin - loop_wait`) to complete before the system is forcefully reset. DCS access times out after 10 seconds by default, so when the DCS is unavailable Patroni and PostgreSQL have at least 5 seconds (`ttl - safety_margin - loop_wait - retry_timeout`) to terminate all client connections.

Safety margin is the time reserved between the leader key update and the watchdog keepalive. Patroni sends a keepalive right after confirmation of the leader key update. If the Patroni process is suspended at exactly the wrong moment, the keepalive can be delayed beyond the margin without triggering the watchdog, leaving a window where the watchdog does not fire before the leader key expires.

To be certain the watchdog triggers under all circumstances, set `safety_margin: -1`, which sets the watchdog timeout to `ttl // 2`. If you need that guarantee you should probably increase `ttl` and/or reduce `loop_wait` and `retry_timeout`.

The `watchdog.device` default is `/dev/watchdog`. Release 4.1.4 fixed Patroni disabling the watchdog before client backends had fully stopped when `primary_stop_timeout` was shorter than the minimum watchdog timeout.

## Checked

2026-11-03. Confirmed against the Watchdog page (5 second default margin, the `ttl - safety_margin - loop_wait` arithmetic, `safety_margin` of -1 giving `ttl // 2`) and YAML Configuration Settings (`watchdog.device` defaults to /dev/watchdog); release 4.1.4 note against the release notes.

Method: documentation only; no commands were run.
