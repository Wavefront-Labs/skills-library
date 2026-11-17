---
id: computing-software.database-administration.pgbouncer.server-login-retry
name: server-login-retry
category: computing-software
field: database-administration
product: pgbouncer
tags: [pgbouncer, server-login-retry, failover, restart, pause]
level: advanced
status: docs-checked
description: "server_login_retry and server_connect_timeout: how PgBouncer backs off after a failed server login and why to use PAUSE for restarts."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: understand the retry delay after server login failures.

`server_login_retry` (default 15.0 seconds): if login to the server fails, from a connect failure or an authentication failure, the pooler waits this long before retrying. During the wait, new clients trying to connect to the failing server get an error immediately without another connection attempt.

The purpose is to stop clients queuing needlessly while the server is not working. The cost: if a server fails briefly, for example during a restart or because of an erroneous configuration, it takes at least this long until PgBouncer considers connecting again. The docs say planned events such as restarts should normally be managed with the PAUSE command to avoid this.

`server_connect_timeout` (default 15.0 seconds) closes a server connection whose connect and login do not finish in time.

For multi-host entries (`host=h1,h2,h3` with `load_balance_hosts`), the docs recommend setting server_login_retry lower than the default so retries across hosts are fast.

Planned restart procedure from the console:

```
PAUSE;
-- restart PostgreSQL
RESUME;
```

PAUSE waits for server connections to be released according to the pooling mode and does not return until all are disconnected. New client connections to a paused database wait until RESUME. SHOW DATABASES has a paused column, and SHOW STATE shows active or paused.

## Checked

2026-11-03. Settings, defaults, values, console commands and column names were checked against the official PgBouncer pages cited in `sources` (config, usage, faq, install; fetched this batch), reading the prose against the page text. No wrong claims were found; nothing was removed.

Method: documentation only; no commands were run.
