---
id: computing-software.database-administration.replication-high-availability.connection-routing-and-health-checks
name: connection-routing-and-health-checks
category: computing-software
field: database-administration
product: replication-high-availability
tags: [database-administration, high-availability, failover, haproxy-health-check, haproxy, proxysql, patroni-rest-api, read-write-split, connection-routing, pgbouncer, virtual-ip]
level: advanced
status: draft
description: "Route clients to the current primary and healthy replicas after failover: HAProxy with role-aware health checks (Patroni REST), ProxySQL hostgroups, DNS and VIP trade-offs."
sources:
  - https://patroni.readthedocs.io/en/latest/rest_api.html
  - https://www.haproxy.com/documentation/haproxy-configuration-manual/latest/#5.2-check
  - https://proxysql.com/documentation/main-runtime/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Connection routing and health checks

**Goal:** within seconds of a failover, writes go to the new primary and reads to
healthy, non-lagging replicas, without app config changes.

## Options
| Method | Failover speed | Notes |
|---|---|---|
| DNS record update | TTL + client caching (often minutes) | Simple; JVM and pools cache DNS |
| Virtual IP (keepalived/VRRP, cloud secondary IP) | Seconds | Same L2/subnet; must be moved only after fencing |
| TCP proxy with role-aware checks (HAProxy) | Check interval × fall count | Works across subnets; proxy itself needs HA |
| SQL-aware proxy (ProxySQL, PgBouncer + logic, MySQL Router) | Seconds | Read/write split, query rules |
| Multi-host client connection strings | Driver-dependent | libpq `target_session_attrs=read-write`, JDBC `targetServerType=primary` |

## HAProxy in front of Patroni (PostgreSQL)
Patroni's REST API answers `200` on `/primary` only on the leader, `/replica`
(optionally `?lag=10MB`) only on healthy replicas.
```
listen pg_rw
  bind *:5000
  option httpchk GET /primary
  http-check expect status 200
  default-server inter 2s fall 3 rise 2 on-marked-down shutdown-sessions
  server pg1 10.0.0.11:5432 check port 8008
  server pg2 10.0.0.12:5432 check port 8008
listen pg_ro
  bind *:5001
  balance roundrobin
  option httpchk GET /replica?lag=50MB
  server pg1 10.0.0.11:5432 check port 8008
  server pg2 10.0.0.12:5432 check port 8008
```
`on-marked-down shutdown-sessions` kills connections to a demoted node so clients
reconnect to the new primary instead of writing into a read-only server.

## ProxySQL (MySQL)
Writer/reader hostgroups; ProxySQL moves servers between them by checking
`read_only` (`mysql_replication_hostgroups`) or Group Replication state
(`mysql_group_replication_hostgroups`), and shuns replicas over
`max_replication_lag`. Query rules route `SELECT` (not `SELECT ... FOR UPDATE`) to readers.

## Gotchas
- A plain TCP check (port open) routes writes to a demoted primary: always check role.
- The proxy layer is a new SPOF: run two with keepalived or as a sidecar per app host.
- Read-your-writes breaks with read routing to lagging replicas; route session-critical reads to the primary.

## Verify
During a failover drill, measure time until writes succeed via the proxy endpoint
and that no writes reached the old primary (`pg_stat_activity` / processlist on it).
