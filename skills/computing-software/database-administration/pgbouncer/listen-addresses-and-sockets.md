---
id: computing-software.database-administration.pgbouncer.listen-addresses-and-sockets
name: listen-addresses-and-sockets
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, listen-addr, listen-port, unix-socket, networking]
level: intro
status: docs-checked
description: "listen_addr, listen_port and the unix_socket_dir, unix_socket_mode and unix_socket_group settings, with defaults."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control where PgBouncer accepts connections.

- `listen_addr`: comma-separated list of addresses for TCP; `*` means all addresses. Addresses may be IPv4/IPv6 numerics or names. Default: not set, in which case only Unix socket connections are accepted.
- `listen_port` (default 6432): applies to both TCP and Unix sockets.
- `unix_socket_dir` (default /tmp, empty on Windows): location of the Unix sockets; applies to both the listening socket and server connections. An empty string disables Unix sockets. A value starting with `@` creates a socket in the abstract namespace (Linux and Windows).
- `unix_socket_mode` (default 0777): file mode of the socket. Ignored for abstract sockets; not supported on Windows.
- `unix_socket_group` (default not set): group name for the socket. Ignored for abstract sockets; not supported on Windows.

```
[pgbouncer]
listen_addr = 127.0.0.1,10.0.0.5
listen_port = 6432
unix_socket_dir = /path/to/sockets
unix_socket_mode = 0770
unix_socket_group = pgusers
```

Extra TCP tuning: `listen_backlog` (default 128) sets the listen(2) backlog; when the queue is full further new connection attempts are dropped.

For the admin console, the user name pgbouncer may log in without a password over the Unix socket when the client has the same Unix UID as the running process.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
