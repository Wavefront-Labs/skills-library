---
id: computing-software.cloud-infrastructure-engineering.aws.rds-proxy-monitoring-and-connection-troubleshooting
name: rds-proxy-monitoring-and-connection-troubleshooting
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, rds-proxy, proxy-troubleshooting, proxy-metrics, databaseconnectionscurrentlysessionpinned, enhanced-logging, connection-errors]
level: advanced
status: docs-checked
description: "Monitor RDS Proxy with its CloudWatch metrics and fix connection failures: target health, Secrets Manager/IAM auth errors, TLS, pinning, borrow timeouts and SG paths."
sources: ["https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.troubleshooting.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.monitoring.html", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy-pinning.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RDS Proxy monitoring and troubleshooting

## 1. Target health first
```bash
aws rds describe-db-proxy-targets --db-proxy-name orders-proxy \
  --query 'Targets[].{ep:Endpoint,role:Role,state:TargetHealth.State,reason:TargetHealth.Reason,desc:TargetHealth.Description}'
```
`TargetHealth.State` is `REGISTERING`, `AVAILABLE`, `UNAVAILABLE` or `UNUSED`; `Reason` is one of `UNREACHABLE`,
`CONNECTION_FAILED`, `AUTH_FAILURE`, `PENDING_PROXY_CAPACITY`, `INVALID_REPLICATION_STATE`, `PROMOTED`.
- `AVAILABLE`: the proxy can connect to the DB. `REGISTERING` is brief.
- `PENDING_PROXY_CAPACITY`: retry after the proxy finishes scaling.
- `UNREACHABLE`, `CONNECTION_FAILED`, `AUTH_FAILURE`: read the `Description` field for the diagnosis.
- Description "Proxy does not have any registered credentials": check that credentials are registered for the user and
  the IAM role that reads the Secrets Manager secret is valid. The secret's `SecretString` must be JSON with
  `username` and `password`.
- The proxy role needs `secretsmanager:GetSecretValue` on each secret and `kms:Decrypt` on its key.
- Test reachability from a host in the same VPC (`nc` to the proxy endpoint and port): you cannot log in to the proxy from outside its VPC.

## 2. Client-side errors (documented text)
| Error | Cause and fix |
|---|---|
| `This RDS Proxy requires TLS connections` (MySQL 3159, PostgreSQL 28000) | `Require Transport Layer Security` is on but the client used `ssl-mode=DISABLED` / `sslmode=disable`; connect with TLS or turn the setting off |
| `IAM authentication is allowed only with SSL connections` (PostgreSQL 28000) | IAM auth with `sslmode=disable`; use `sslmode=require` or stronger |
| `IAM authentication failed for user` / `... for the role` (PostgreSQL 28P01) | check the token, the proxy's authentication scheme, and the IAM policy on the proxy role granting `rds-db:connect` for the database user; for IAM connections the resource uses the proxy resource ID (`prx-...`) |
| `This RDS proxy has no credentials for the role` (PostgreSQL 28000) | no Secrets Manager secret registered for that role; add one |
| `Timed-out waiting to acquire database connection` (MySQL 9501, PostgreSQL 08000) | maximum connections reached, or database unavailable; see pinning and `MaxConnectionsPercent` |
| `ERROR 1045 Access denied` (MySQL) | the proxy's secret does not match an existing DB user and password |
| `ERROR 1040 ... rate limit exceeded` (MySQL), PostgreSQL 53300 | connection or IAM authentication request rate limit exceeded; event `RDS-EVENT-0275` records throttling |

## 3. Metrics that matter (CloudWatch console: Metrics, RDS, Per-Proxy Metrics)
Dimension sets: `ProxyName`; `ProxyName`+`EndpointName`; `ProxyName`+`TargetGroup`+`Target`; `ProxyName`+`TargetGroup`+`TargetRole`.
- `ClientConnections`, `ClientConnectionsReceived`, `ClientConnectionsSetupFailedAuth`,
  `ClientConnectionsSetupSucceeded`, `ClientConnectionsNoTLS`, `ClientConnectionsTLS`.
- `DatabaseConnections`, `DatabaseConnectionsCurrentlyBorrowed`,
  `DatabaseConnectionsCurrentlyInTransaction`, `DatabaseConnectionsCurrentlySessionPinned`,
  `DatabaseConnectionsBorrowLatency` (time to get a DB connection from the pool), `DatabaseConnectionsWithTLS`.
- `MaxDatabaseConnectionsAllowed` vs `DatabaseConnections`: pool ceiling.
- `QueryRequests`, `QueryRequestsTLS`, `QueryRequestsNoTLS`, `QueryDatabaseResponseLatency`.
Metrics are published per underlying proxy instance, so aggregate with CloudWatch statistics. Some metrics do not
appear until the first successful connection.
Alarms: auth failures > 0, borrow latency high, pinned connections near `DatabaseConnections` (multiplexing lost).

## 4. Pinning (multiplexing lost)
Pinning ties a client to one DB connection until it disconnects. Triggers differ by engine (the pinning page lists
them): for example statements over 16 KB (all engines), temporary tables, prepared statements, and `SET` of session
variables (PostgreSQL always pins on `SET`).
Enable **enhanced logging** temporarily (`modify-db-proxy --debug-logging`) to debug SQL behaviour and proxy
performance; the setting is automatically disabled after 24 hours. Then:
- move identical initialisation `SET`s into the proxy's **initialization query** (`InitQuery` in the target group
  connection pool config) or set variables consistently across connections;
- for MySQL-family proxies, set `SessionPinningFilters=EXCLUDE_VARIABLE_SETS` when variable sets are safe to share;
- avoid client-side prepared statements where they pin.

## 5. Pool sizing knobs
`MaxConnectionsPercent` (of the DB's `max_connections`), `MaxIdleConnectionsPercent`,
`ConnectionBorrowTimeout`. Leave headroom for admin connections and other clients that
bypass the proxy. If the proxy subnets run low on free IPs it cannot scale (`RDS-EVENT-0243`).

## Verify
- [ ] All targets `AVAILABLE`.
- [ ] Clients connect via the proxy endpoint with TLS; `ClientConnectionsSetupFailedAuth` is zero.
- [ ] `DatabaseConnectionsCurrentlySessionPinned` low relative to borrowed connections under load.

## Checked
Date: 2026-10-27. Sources: RDS User Guide rds-proxy.troubleshooting (target health, documented error text),
rds-proxy.monitoring (metric names and dimension sets), rds-proxy-pinning, rds-proxy-creating (enhanced logging, 24 h
auto-disable); botocore `rds` model (`TargetHealth` state and reason enums). Corrected `DatabaseConnectionRequestsWithTLS`
(the metric is `DatabaseConnectionsWithTLS`), replaced guessed reason meanings and error strings with documented ones,
removed the `AWS/RDS` namespace and `/aws/rds/proxy/<name>` log group claims (not confirmed).
Method: documentation only; no commands were run.
