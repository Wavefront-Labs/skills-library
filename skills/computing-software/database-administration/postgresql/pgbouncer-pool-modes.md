---
id: computing-software.database-administration.postgresql.pgbouncer-pool-modes
name: pgbouncer-pool-modes
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, pg-connection-pooling, pgbouncer, pgbouncer-pool-mode, transaction-pooling, session-pooling, statement-pooling, session-state, advisory-locks]
level: practitioner
status: docs-checked
description: "Choose PgBouncer session, transaction or statement pooling and know exactly which PostgreSQL features break in transaction mode."
sources:
  - https://www.pgbouncer.org/config.html#pool_mode
  - https://www.pgbouncer.org/features.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PgBouncer pool modes

**Goal:** pick the mode that maximises connection reuse without breaking the application.

## The three modes
| Mode | Server connection returned to pool | Use |
|---|---|---|
| `session` | When the client disconnects | Legacy apps relying on session state; little multiplexing gain |
| `transaction` | At COMMIT/ROLLBACK | Default choice for web apps; huge client:server ratios |
| `statement` | After each statement; multi-statement transactions refused | Autocommit-only workloads (e.g. PL/Proxy) |

```ini
[pgbouncer]
pool_mode = transaction
[databases]
app = host=10.0.0.5 dbname=app
reporting = host=10.0.0.5 dbname=app pool_mode=session   ; per-database override
```
Per-user override: `[users] etl = pool_mode=session`.

## What breaks in transaction mode
Session state lives on a server connection the next transaction may not get:
| Feature | Workaround |
|---|---|
| `SET` / `RESET` (search_path, timezone) | `SET LOCAL` inside the transaction, or role/database defaults (`ALTER ROLE ... SET`) |
| Session-level advisory locks | Transaction-level advisory locks |
| `LISTEN` | Direct connection (bypass the pooler) |
| Temp tables surviving across transactions | Create and drop within one transaction (`ON COMMIT DROP`) |
| `WITH HOLD` cursors | Avoid or use session pool |
| Protocol-level prepared statements | `max_prepared_statements` (enabled by default, 200, since PgBouncer 1.24.0; see prepared statements skill) |
| `LOAD` of libraries | Session pool |

PgBouncer tracks some session parameters (`track_extra_parameters`). The changelog says its latest release tracks all parameters PostgreSQL reports by default (search_path on PostgreSQL 18 and above, default_transaction_read_only on 14 and above); check your version before relying on `SET` in transaction mode.

## Checking what you have
```bash
psql -p 6432 -U pgbouncer pgbouncer -c 'SHOW POOLS;'   # cl_active, cl_waiting, sv_active, sv_idle, pool_mode
```
`cl_waiting > 0` steadily means the pool is too small or transactions are held open.

## Gotchas
- An app holding a transaction open while calling external APIs pins a server connection in any mode; fix the app.
- `server_reset_query = DISCARD ALL` is used only in session mode; in transaction mode it is skipped (unless `server_reset_query_always`).

## Verify
Run the app's integration tests through the pooler in transaction mode; grep the code for `SET `, `LISTEN`, session advisory lock calls, `TEMP TABLE`.

## Checked

2026-10-28. Confirmed against the PgBouncer config page (pool_mode, max_prepared_statements default 200, track_extra_parameters, so_reuseport) and changelog (max_prepared_statements default 200 from 1.24.0; all PostgreSQL-reported parameters tracked by default in the latest release). Corrected: prepared statement default version (1.24.0, not 1.21+/1.22) and the stale parameter-tracking statement. Removed: advisory lock function names and the fixed list of tracked parameters (not in the fetched pages).

Method: documentation only; no commands were run.
