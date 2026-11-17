---
id: computing-software.database-administration.pgbouncer.show-clients-and-servers
name: show-clients-and-servers
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, show-clients, show-servers, connections, troubleshooting]
level: practitioner
status: docs-checked
description: "SHOW CLIENTS and SHOW SERVERS columns and states, and mapping a client to its server connection using ptr and link."
sources:
  - https://www.pgbouncer.org/usage.html
  - https://www.pgbouncer.org/faq.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: identify connections on both sides of the pooler.

`SHOW CLIENTS;` columns: type (C), user, database, replication (none, logical or physical), state, addr, port, local_addr, local_port, connect_time, request_time, wait and wait_us (current waiting time), close_needed (unused for clients), ptr, link, remote_pid (only over Unix socket where the OS supports it), tls, application_name, prepared_statements, id.

Client states: `active` (linked to a server connection), `idle` (no queries waiting), `waiting`, `active_cancel_req`, `waiting_cancel_req`.

`SHOW SERVERS;` has the same shape with type S, plus `close_needed` (1 if the connection will close ASAP because a config reload, DNS update or RECONNECT changed connection info) and `remote_pid` (backend PID; over a Unix socket it is the OS PID where supported; otherwise taken from the server's cancel packet, which is a random number if the server is another PgBouncer). `wait` and `wait_us` are unused for servers. `prepared_statements` is the number prepared on the server, limited by max_prepared_statements.

Server states: `active`, `idle`, `used`, `tested`, `new`, `active_cancel`, `being_canceled`.

FAQ recipe for which client is on which server: use `ptr` and `link` to match a client to its server connection; use the client's `addr` and `port` for the client-side TCP connection; use `local_addr` and `local_port` for the TCP connection to the server.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
