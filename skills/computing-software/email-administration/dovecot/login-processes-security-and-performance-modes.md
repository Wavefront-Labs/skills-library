---
id: computing-software.email-administration.dovecot.login-processes-security-and-performance-modes
name: login-processes-security-and-performance-modes
category: computing-software
field: email-administration
product: dovecot
tags: [login-processes, high-security-mode, high-performance-mode, service-client-limit, dovenull, login-unauthenticated-client-limit]
level: advanced
status: docs-checked
description: "Choose between one-process-per-connection high-security mode and shared high-performance login processes, with the limits that control each."
sources:
  - https://doc.dovecot.org/main/core/config/login_processes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Login processes handle IMAP, POP3, submission and ManageSieve connections before login. They need no other abilities, so by default they run as the unprivileged `dovenull` user chrooted into a non-writable directory holding only authentication sockets. They also keep proxying TLS after login, so all TLS code stays in the restricted environment and a library hole exposes only that chroot.

High-security mode uses a new imap-login or pop3-login process for each connection. A flaw in pre-authentication code then exposes only that one connection. Consequences:
- `service_process_limit` caps simultaneous logins (default `default_process_limit`), and TLS proxying processes count toward it. Make it higher than the maximum simultaneous users.
- With TLS the process stays alive to proxy between the client and the imap process.
- At the cap, the oldest process still logging in (not proxying) is destroyed.
- Set `service_process_min_avail` above zero to keep idle processes and avoid startup latency.
- `service_vsz_limit` is fine at default.

High-performance mode uses long-running login processes each handling many connections. It loses much of the isolation benefit, because an attacker in one process can see other connections.
- Set `service_process_min_avail` to at least the CPU count (`%{system:cpu_count}` expands automatically), otherwise new processes appear only when one hits `service_client_limit`.
- Default `service_client_limit` times `service_process_limit` is 1000 x 100 = 100k connections.
- Raise `service_vsz_limit` to avoid out-of-memory with TLS.
- `login_unauthenticated_client_limit` caps unauthenticated connections per process, destroying the oldest first to blunt idle-connection DoS.

`login_socket_path` sets the auth socket path globally, with per-service overrides.

## Checked

2026-11-03. Confirmed on the Login Processes page: dovenull and a non-writable chroot with only auth sockets, TLS proxying staying in the login process, high-security mode (one process per connection, service_process_limit defaulting to default_process_limit, oldest logging-in process destroyed at the cap, service_process_min_avail, service_vsz_limit), high-performance mode (service_process_min_avail at least the CPU count via %{system:cpu_count}, 1000 x 100 = 100k connections, raise service_vsz_limit, login_unauthenticated_client_limit) and login_socket_path. Nothing removed.

Method: documentation only; no commands were run.
