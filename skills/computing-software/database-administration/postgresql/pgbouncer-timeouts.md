---
id: computing-software.database-administration.postgresql.pgbouncer-timeouts
name: pgbouncer-timeouts
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pgbouncer-timeouts, query-wait-timeout, server-lifetime, server-idle-timeout, idle-transaction-timeout, pgbouncer]
level: practitioner
status: docs-checked
description: "Set PgBouncer timeouts (query_wait_timeout, server_lifetime, server_idle_timeout, idle_transaction_timeout, client_idle_timeout) and diagnose which one fired."
sources:
  - https://www.pgbouncer.org/config.html
  - https://www.pgbouncer.org/usage.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PgBouncer timeouts

## The ones that matter
| Setting | Default | What it does | Starting point (judgement) |
|---|---|---|---|
| `query_wait_timeout` | 120 s | max time a query waits for a server connection; then the client is disconnected; 0 disables (clients queue indefinitely) | 15-30 s for web apps: fail fast instead of piling up |
| `server_lifetime` | 3600 s | close an unused server connection that has been connected longer than this; 0 = use once, then close | 1800-3600 s; recycles backend memory, rebalances after failover |
| `server_idle_timeout` | 600 s | close server connections idle this long | 300-600 s |
| `idle_transaction_timeout` | 0 (off) | disconnect a client idle **inside a transaction** this long | 60-300 s: protects the pool from leaked transactions |
| `client_idle_timeout` | 0 (off) | disconnect idle clients | usually off; docs: only for network problems, keep it larger than client-side lifetimes |
| `server_connect_timeout` | 15 s | TCP/auth to PostgreSQL | 5 s |
| `server_login_retry` | 15 s | wait before retrying after a failed server login | 5 s |
| `query_timeout` | 0 (off) | cancel queries running this long | docs: use only with a slightly smaller server-side `statement_timeout`, for network problems |
| `client_login_timeout` | 60 s | client must finish login in this time | default |

## Diagnose from the app error
- Clients dropped by `query_wait_timeout` (exact message text varies by version; check the PgBouncer log): pool exhausted; check `SHOW POOLS` (`cl_waiting`, `maxwait`). Root cause is usually slow queries or long transactions holding servers, or pool too small.
- Client dropped by `idle_transaction_timeout`: app opened a transaction and did not send anything; find the code path (BEGIN then a remote API call).
- Server connections lost around a fixed age: compare `tcp_keepalive` and its related settings in config.html with any firewall idle timer; `server_lifetime` only closes unused connections.

## Watching
```
SHOW POOLS;    -- cl_active, cl_waiting, sv_active, sv_idle, maxwait, maxwait_us
SHOW STATS;    -- avg_wait_time
SHOW CONFIG;   -- effective timeout values
```
Alert on `maxwait` > a few seconds.

## Apply
Edit pgbouncer.ini then `RELOAD;` in the admin console.

## Gotchas
- `query_wait_timeout = 0` means clients wait forever: an incident turns into thousands of hung app threads.
- `server_reset_query` (`DISCARD ALL`) runs only in session pooling by default; transaction pooling relies on apps not leaving session state.
- PostgreSQL `idle_in_transaction_session_timeout` is the server-side backstop; set both.

## Checked
2026-10-31. Confirmed on pgbouncer.org config.html: defaults and meaning of query_wait_timeout (120, 0 disables), server_lifetime (3600), server_idle_timeout (600), server_connect_timeout (15), server_login_retry (15), client_login_timeout (60), query_timeout (0), client_idle_timeout (0), idle_transaction_timeout (0), server_reset_query behaviour in transaction pooling; on usage.html: SHOW POOLS columns maxwait and maxwait_us, SHOW STATS avg_wait_time, RELOAD. Removed: exact client error message strings (not in the docs) and the claim that timeouts apply without dropping connections. The starting-point column is judgement.
Method: documentation only; no commands were run.
