---
id: computing-software.database-administration.pgbouncer.multi-host-load-balancing
name: multi-host-load-balancing
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, load-balance-hosts, host-list, round-robin, server-round-robin]
level: advanced
status: docs-checked
description: "Comma-separated host lists, load_balance_hosts (round-robin, disable) and server_round_robin, plus FAQ guidance on external load balancing."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: spread new connections across several backends.

A `host` may be a comma-separated list, for example `host=192.168.0.1,192.168.0.2,192.168.0.3`. New connections are made round-robin. All hosts must be available at all times: there is no mechanism to skip unreachable hosts, which differs from libpq host lists. If a listed name resolves to several addresses via DNS, the two round-robin systems run independently.

`load_balance_hosts` (per database, default `round-robin`):

- `round-robin`: each new connection attempt chooses the next host entry.
- `disable`: new connections keep using the same entry until a connection fails, after which the next entry is chosen.

It currently covers only multi-host lists, not a single host whose DNS record has several IPs. The docs recommend a lower server_login_retry for fast retries with multiple hosts. SHOW POOLS and SHOW DATABASES show load_balance_hosts when the host is a list.

`server_round_robin` (default 0): by default idle server connections are reused LIFO, so a few connections take most load, best for a single server. If a round-robin system sits behind a database address (TCP, DNS or host list), turn this on for uniform load. It governs assignment of clients to already established connections, while host lists govern where new connections go.

The FAQ states PgBouncer has no internal multi-host load-balancing config; options are DNS round-robin (more than 8 IPs needs EDNS0 support in the DNS backend) or a TCP load balancer such as LVS or HAProxy, ideally with a smaller server_lifetime and server_round_robin on.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
