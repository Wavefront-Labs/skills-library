---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.connection-pooling
name: connection-pooling
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, database-selection, connection-pooling, pgbouncer, rds-proxy, connection-limits, serverless-database-connections, database-proxy]
level: practitioner
status: docs-checked
description: "Size and implement database connection pooling: app pools, PgBouncer pooling modes, RDS Proxy, Azure built-in PgBouncer, and prepared-statement and session-state limits."
sources: ["https://www.pgbouncer.org/features.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html", "https://learn.microsoft.com/azure/postgresql/flexible-server/concepts-pgbouncer", "https://github.com/brettwooldridge/HikariCP/wiki/About-Pool-Sizing"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connection pooling and database proxies

## Why
Postgres uses a process-based connection model, so many idle connections are expensive and the
server runs into resource constraints beyond a few thousand connections (Azure PostgreSQL docs).
Surges of new connections also hurt (RDS Proxy docs: oversubscription or a fast rate of new connections).

## Layers
1. **Application pool** (HikariCP guidance): keep it small and saturated; most application threads
   should wait on the pool. Starting point from PostgreSQL: `connections = (core_count * 2) +
   effective_spindle_count` (cores without hyperthreads; spindles near zero when data is cached);
   load test around it. Pools of 100 are often overkill. Mixed long and short transactions: use
   separate pools. If a thread holds several connections at once, deadlock-free minimum is
   `Tn x (Cm - 1) + 1`.
2. **PgBouncer pool modes**:
   - Session: server connection held for the whole client connection; all PostgreSQL features.
   - Transaction: server connection held only during a transaction; breaks session features.
     Not supported: SET/RESET, LISTEN, WITH HOLD cursors, SQL PREPARE/DEALLOCATE, PRESERVE/DELETE
     ROWS temp tables, LOAD, session-level advisory locks. Protocol-level prepared statements work
     only when `max_prepared_statements` is non-zero.
   - Statement: transaction pooling with multi-statement transactions disallowed (autocommit).
3. **RDS Proxy**: pools and shares connections, queues or throttles when the pool is busy, and
   rejects connections beyond configured limits (load shedding). It reconnects to a standby on
   failover while preserving application connections; clients can be required to use IAM, and the
   proxy uses IAM or Secrets Manager credentials. Listens on port 3306 (MySQL, MariaDB) and 5432
   (PostgreSQL). Must be in the same VPC as the database and not publicly accessible; associates
   with the writer instance only; a statement over 16 KB pins the session to a connection. See
   "Avoiding pinning an RDS Proxy" for other causes.
4. **Azure Database for PostgreSQL flexible server built-in PgBouncer**: enable with
   `pgbouncer.enabled`; connect on port 6432 using the server host name. Defaults on the page:
   `pgbouncer.pool_mode` transaction, `pgbouncer.default_pool_size` 50, `pgbouncer.max_client_conn`
   5000, `pgbouncer.max_prepared_statements` 0. Not supported on the Burstable tier; restarts
   with the server on failover; it is a potential single point of failure and is single-threaded.

## Steps
1. Total possible connections = instances x pool size; keep below the database limit with headroom.
2. Add a proxy when instance count is elastic or large.
3. Monitor active, idle and waiting connections (Azure PgBouncer metrics: active and waiting client
   connections, active and idle server connections).
4. Test the application against transaction pooling in QA before switching production.

## Gotchas
- Features listed above that break in transaction mode.
- A pooler is itself a point of failure; plan for it.

## Verify
- [ ] Scale-out test to max instances keeps database connections below the limit.

## Checked
Confirmed against the four cited pages. Removed as not stated there: "several MB per process",
the PgBouncer 1.21 version gate, RDS Proxy "reduces failover time" figures, Cloud SQL managed
pooling, `idle_in_transaction_session_timeout`, and the serverless/HTTP data API advice.
Method: docs-only read of cited pages, 2026-11-08
