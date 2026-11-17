---
id: computing-software.database-administration.pgbouncer.show-databases-users-config
name: show-databases-users-config
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, show-databases, show-users, show-config, console]
level: practitioner
status: docs-checked
description: "SHOW DATABASES, SHOW USERS, SHOW CONFIG, SHOW LISTS, SHOW STATE and the other informational commands."
sources:
  - https://www.pgbouncer.org/usage.html
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: inspect configuration and internals from the console.

- `SHOW DATABASES`: name, host, port, database, force_user, pool_size, min_pool_size, reserve_pool_size, server_lifetime, pool_mode (NULL if default), load_balance_hosts, max_connections (from max_db_connections), current_connections, max_client_connections, current_client_connections, paused (1/0), disabled (1/0).
- `SHOW USERS`: name, pool_size, reserve_pool_size, pool_mode (NULL if not set), max_user_connections, current_connections, max_user_client_connections, current_client_connections.
- `SHOW CONFIG`: key, value, default, changeable. changeable is yes or no; no means boot time only.
- `SHOW LISTS` (columns, not rows): databases, users, pools, free_clients, used_clients, login_clients, free_servers, used_servers, dns_names, dns_zones, dns_queries, dns_pending (not used). Free clients/servers are disconnected objects whose memory is kept for reuse.
- `SHOW STATE`: active or paused.
- `SHOW VERSION`: version string.
- `SHOW MEM`: sizes of internal memory allocations; subject to change.
- `SHOW SOCKETS` and `SHOW ACTIVE_SOCKETS`: clients and servers info plus low-level socket details.
- `SHOW DNS_HOSTS` (hostname, ttl, addrs) and `SHOW DNS_ZONES` (zonename, serial, count).
- `SHOW PEERS` (peer_id, host, port, pool_size) and `SHOW PEER_POOLS`.
- `SHOW HELP` lists console usage.

All SHOW commands work for stats_users; other commands need admin_users. Only the simple query protocol is supported.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
