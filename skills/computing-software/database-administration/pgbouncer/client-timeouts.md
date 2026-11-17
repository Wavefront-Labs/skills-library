---
id: computing-software.database-administration.pgbouncer.client-timeouts
name: client-timeouts
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, client-login-timeout, query-wait-timeout, client-idle-timeout, timeouts]
level: advanced
status: docs-checked
description: "client_login_timeout, query_wait_timeout, query_wait_notify, cancel_wait_timeout, client_idle_timeout and related client-side timeouts."
sources:
  - https://www.pgbouncer.org/config.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: bound how long clients may wait, idle or run.

- `client_login_timeout` (default 60.0 s): a client that connects but cannot log in in this time is disconnected.
- `query_wait_timeout` (default 120.0 s): maximum time queries may wait for a server. If none is assigned in time, the client is disconnected. 0 disables, and then clients queue indefinitely. It guards against unresponsive servers grabbing connections and helps when the server is down or rejecting connections. Overridable per database and per user (-1 means not set).
- `query_wait_notify` (default 5 s): time a client is queued before PgBouncer sends a notification that it is queued. 0 disables.
- `cancel_wait_timeout` (default 10.0 s): maximum time cancel requests wait for execution; if not assigned, the client is disconnected. 0 disables (cancel requests queue indefinitely). Prevents a client locking up when a cancel cannot be forwarded because the server is down.
- `client_idle_timeout` (default 0.0, disabled): closes client connections idle longer than this. Should be larger than client-side connection lifetime settings and used only for network problems. Also per user, and flagged potentially dangerous.
- `login_notify_message` (default empty): welcome message sent after login, so clients know they reached PgBouncer.

The docs group query_timeout, query_wait_timeout, cancel_wait_timeout, client_idle_timeout, idle_transaction_timeout and transaction_timeout under "Dangerous timeouts": setting them can cause unexpected errors.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
