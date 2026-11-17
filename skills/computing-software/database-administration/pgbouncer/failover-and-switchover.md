---
id: computing-software.database-administration.pgbouncer.failover-and-switchover
name: failover-and-switchover
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, failover, switchover, dns, reconnect]
level: advanced
status: docs-checked
description: "How PgBouncer follows a new primary: DNS changes, editing host and RELOAD, or RECONNECT; PgBouncer has no built-in failover detection."
sources:
  - https://www.pgbouncer.org/faq.html
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: redirect PgBouncer to a new server.

The FAQ states PgBouncer has no internal failover-host configuration or failure detection; use external tools with one of three mechanisms:

1. DNS reconfiguration. When the IP behind a DNS name changes, PgBouncer reconnects to the new server. Tune with `dns_max_ttl` (lifetime of one host name, default 15 s) and `dns_zone_check_period` (how often a zone SOA is queried; if the SOA changed, all names under the zone are re-queried; default disabled; c-ares only).
2. Edit the host in pgbouncer.ini and reload with SIGHUP or `RELOAD;`. PgBouncer detects the changed host and reconnects to the new server.
3. Run `RECONNECT;`, meant for cases where neither of the above applies, for example when HAProxy routes connections downstream of PgBouncer. It reopens all server connections, so run it after the other component changed its routing.

Supporting commands: `WAIT_CLOSE` to wait until the change is fully applied, `PAUSE` and `RESUME` to switch all connections at the same instant, and `KILL` to drop connections without waiting in an emergency failover.

```
RELOAD;
WAIT_CLOSE;
```

Existing server connections to the old destination are closed when next released, according to the pooling mode; new ones use the new parameters immediately. With server_login_retry (default 15 s), a briefly failing server delays reconnection by at least that long.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
