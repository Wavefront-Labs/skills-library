---
id: computing-software.cloud-infrastructure-engineering.aws.rds-proxy-connection-pooling
name: rds-proxy-connection-pooling
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, rds-proxy, connection-pooling, connection-multiplexing, pinning, session-pinning, lambda-database, secrets-manager, iam-authentication, proxy-endpoint, read-only-endpoint, max-connections-percent, idle-client-timeout, failover, aurora, rds, postgresql, mysql, pgbouncer, proxysql, create-db-proxy, proxy-target-group]
level: practitioner
status: docs-checked
description: "Put RDS Proxy in front of RDS/Aurora: Secrets Manager and IAM auth, pool sizing, read-only endpoints, and fixing session pinning that defeats multiplexing."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy-setup.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy-managing.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy-pinning.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy-endpoints.html", "https://docs.aws.amazon.com/lambda/latest/dg/configuration-database.html"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# RDS Proxy — connection pooling that survives Lambda and failover

**Goal:** thousands of short-lived application connections (Lambda, autoscaled
containers) share a small pool of real database connections, failover is invisible to
clients, credentials never live in app config — and the proxy actually multiplexes
instead of silently pinning every session.

## 1. When you need it
- Lambda or any client fleet that opens connections per request and hits "too many connections" errors
  (a high `ConnectionAttempts` metric is the User Guide's signal).
- You want failover to be less disruptive: the proxy bypasses DNS caches and holds idle client
  connections open while it reconnects to the new writer.
- You want IAM auth / Secrets Manager rotation without touching app code.
Less useful for a single long-running app with its own well-sized pool; RDS Proxy has its own charges
(see the pricing page, not checked here).
Alternatives: PgBouncer/ProxySQL on your own instances (more to run); Aurora Data API for pure HTTP access.

## 2. Create
```bash
# secret with {"username":"app","password":"..."} — one per DB user the proxy will serve
aws rds create-db-proxy --db-proxy-name app-proxy --engine-family POSTGRESQL \
  --auth '[{"AuthScheme":"SECRETS","SecretArn":"arn:aws:secretsmanager:<REGION>:<ACCOUNT_ID>:secret:app-db","IAMAuth":"REQUIRED","ClientPasswordAuthType":"POSTGRES_SCRAM_SHA_256"}]' \
  --role-arn arn:aws:iam::<ACCOUNT_ID>:role/rds-proxy-secrets --vpc-subnet-ids subnet-a subnet-b --vpc-security-group-ids sg-proxy \
  --require-tls --idle-client-timeout 1800 --debug-logging
aws rds register-db-proxy-targets --db-proxy-name app-proxy --db-cluster-identifiers app    # or --db-instance-identifiers
aws rds modify-db-proxy-target-group --db-proxy-name app-proxy --target-group-name default \
  --connection-pool-config 'MaxConnectionsPercent=80,MaxIdleConnectionsPercent=40,ConnectionBorrowTimeout=120'
# MySQL-family proxies only: add SessionPinningFilters=[EXCLUDE_VARIABLE_SETS] (the only allowed value)
aws rds describe-db-proxy-targets --db-proxy-name app-proxy   # TargetHealth.State must be AVAILABLE
```
- The proxy role needs `secretsmanager:GetSecretValue` on the secrets and `kms:Decrypt`
  on their key. `IAMAuth: REQUIRED` means clients present an IAM token, the proxy
  presents the secret's password to the DB — the password never leaves AWS.
- Security groups: client SG → proxy SG (engine port); proxy SG → DB SG. The VPC needs a minimum of two
  subnets in different Availability Zones.
- Multiple DB users = multiple secrets in `--auth`. Engine families are `MYSQL`, `POSTGRESQL`, `SQLSERVER`.
- Target `UNAVAILABLE` with "Proxy does not have any registered credentials" = secret
  format wrong (must be the RDS-style JSON) or the role cannot read it.

## 3. Connect
```bash
# IAM token (valid 15 min); IAM authentication needs SSL/TLS on the connection
TOKEN=$(aws rds generate-db-auth-token --hostname app-proxy.proxy-xxxx.<REGION>.rds.amazonaws.com --port 5432 --username app --region <REGION>)
psql "host=app-proxy.proxy-xxxx.<REGION>.rds.amazonaws.com user=app password=$TOKEN sslmode=verify-full sslrootcert=amazon-roots.pem dbname=app"
```
RDS Proxy certificates come from ACM; for certificate verification use a `.pem` of the root CAs from Amazon Trust
Services, not the RDS CA bundle (see `rds-proxy-tls-enforcement`).
Client IAM policy: `rds-db:connect` on `arn:aws:rds-db:<REGION>:<ACCOUNT_ID>:dbuser:prx-<PROXY_RESOURCE_ID>/app`
(when connecting through a proxy, use the **proxy** resource ID such as `prx-...`, not the DB's). Lambda: set the
proxy endpoint as host and generate a fresh token when needed (tokens expire after 15 minutes).

## 4. Pool sizing
- `MaxConnectionsPercent` (1-100; default 100, or 10 for SQL Server) = share of the DB's `max_connections` the proxy
  may open per target; leave headroom (80) for admins and migrations. With two proxies on one DB,
  split the percentage.
- `MaxIdleConnectionsPercent` (0 up to `MaxConnectionsPercent`; default half of `MaxConnectionsPercent`, or 50 if that is
  unset, 5 for SQL Server) = how many idle DB connections stay open; lower it for bursty workloads sharing a DB.
  Specify the two settings together.
- `ConnectionBorrowTimeout` (0-300 s, default 120) = how long the proxy waits for a free pooled connection
  once it has opened its maximum and all are busy; set it below your request timeout so you fail fast.
- `IdleClientTimeout` (1-28,800 s, default 1800): drop idle client connections (the DB connection returns
  to the pool) — keep it above your app pool's idle time or the pool will constantly reconnect.
- Metrics: `ClientConnections`, `DatabaseConnections`, `DatabaseConnectionsCurrentlyBorrowed`,
  `QueryDatabaseResponseLatency`, `DatabaseConnectionsBorrowLatency` (rising = pool exhausted),
  `ClientConnectionsSetupFailedAuth`.

## 5. Pinning — the thing that makes the proxy useless if ignored
Multiplexing works only while a session is "clean". Some interactions **pin** the client connection to one DB
connection until the session ends, which reduces connection reuse. Triggers (RDS User Guide, "Avoiding pinning"):
- All engines: any statement with text larger than 16 KB.
- PostgreSQL: `SET` commands, `PREPARE`/`DISCARD`/`DEALLOCATE`/`EXECUTE`, temporary tables/sequences/views,
  declared cursors, `LISTEN`, loading a module such as `auto_explain`, `nextval`/`setval`, and session-level advisory
  locks (`pg_advisory_lock`; transaction-level `pg_advisory_xact_lock` does not pin).
- MySQL and MariaDB: `SET` of session variables (unless exempted by the filter below), temporary tables,
  prepared statements (SQL text or binary protocol), and sometimes `ROW_COUNT`/`FOUND_ROWS`.
- SQL Server: temporary tables, transactions, cursors, prepared statements and many `SET` statements.
- The `SessionPinningFilters` setting (`EXCLUDE_VARIABLE_SETS`) is supported for MySQL-family databases only; for
  PostgreSQL, setting a variable pins.
Watch `DatabaseConnectionsCurrentlySessionPinned`. Fixes from the User Guide: set variables consistently across
connections, remove `SET` statements from application code, or move identical initialisation `SET`s into the proxy's
initialization query (`InitQuery` in the connection pool configuration). Enhanced logging (`--debug-logging`) logs
detailed information to help debug proxy behaviour; enable it only while debugging. Also turn off driver-side
server-prepared statements where your driver allows it (see its documentation).

## 6. Read-only endpoints and failover
- `create-db-proxy-endpoint --target-role READ_ONLY` (values `READ_WRITE`, `READ_ONLY`) creates a read-only
  endpoint; the default endpoint cannot be modified and sends requests to the writer. A proxy has the default
  endpoint plus up to 20 you create (RDS User Guide, rds-proxy-endpoints).
- In-flight transactions and statements are cancelled on failover and must be retried; idle client connections
  are preserved (see `rds-proxy-failover-behaviour`). Pair with `failover-db-cluster` drills.
- Cross-VPC: a proxy endpoint can be associated with a different VPC than the proxy's own, to connect from another VPC.

## Gotchas
- Engine support is by engine family and version (`MYSQL`, `POSTGRESQL`, `SQLSERVER`); check the User Guide's
  supported engine versions before designing around it.
- Low free IP addresses in the proxy subnets prevent scaling and raise event `RDS-EVENT-0243`.
- Connection throttling raises `RDS-EVENT-0275`; MySQL clients see `ERROR 1040` rate limit messages.
- Not checked here: per-proxy connection ceilings and target limits (see the RDS quotas page).

## Verify
- [ ] 2,000 concurrent clients (`pgbench -c 2000` via the proxy) produce `DatabaseConnections` ≤ `MaxConnectionsPercent` × `max_connections`.
- [ ] `DatabaseConnectionsCurrentlySessionPinned` ≈ 0 under normal app traffic (after fixing the `SET`s).
- [ ] Writer failover: clients see ≤ 1 failed transaction each and no reconnect storm; `ClientConnections` steady.
- [ ] `ClientConnectionsSetupFailedAuth` is zero; connecting with a plain password while `IAMAuth: REQUIRED` is rejected.
- [ ] Secret rotation runs and the app keeps working (no `password authentication failed` in proxy logs).

## Checked
Date: 2026-10-27. Sources: RDS User Guide rds-proxy-planning, rds-proxy.howitworks, rds-proxy-pinning,
rds-proxy.monitoring (metric names), rds-proxy.troubleshooting (secret JSON format, `TargetHealth` messages, event IDs),
rds-proxy-network-prereqs, rds-proxy-endpoints, UsingWithRDS.IAMDBAuth.IAMPolicy and Connecting (proxy resource ID,
15-minute token); botocore `rds` model (ConnectionPoolConfiguration defaults and ranges, UserAuthConfig enums,
EngineFamily, TargetRole). Corrected: `SessionPinningFilters` is MySQL-family only, PostgreSQL `PREPARE` and `SET` pin,
IAM connections verify against Amazon Trust Services roots (not the RDS bundle). Removed unconfirmed timing, memory,
latency, cost, SNI, `rds.force_ssl` and rotation-Lambda claims and the invented proxy log group name.
Method: documentation only; no commands were run.
