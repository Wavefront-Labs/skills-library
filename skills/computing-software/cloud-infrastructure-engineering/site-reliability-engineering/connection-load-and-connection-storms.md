---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.connection-load-and-connection-storms
name: connection-load-and-connection-storms
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [connection-load, connection-storms, handling-overload, tls-handshake, connection-pooling, health-checks, reconnect-backoff]
level: advanced
status: docs-checked
description: "Account for connection load (pools, idle health checks, bursts of new connections) and prevent connection storms with batch proxies, tuned health checks and backoff."
sources: ["https://sre.google/sre-book/handling-overload/", "https://sre.google/sre-book/load-balancing-datacenter/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Connection load and connection storms

SRE Book "Handling Overload", "Load from Connections": load at a backend is not only the requests it
receives. The CPU and memory cost of maintaining a large pool of connections, and of a fast rate of
connection churn, is negligible in small systems but quickly becomes a problem in very large-scale RPC systems.

## Sources of connection load
- Large pools of connections: every client connecting to every backend (fix: subsetting, see
  `deterministic-subsetting-implementation`).
- Health checking of idle connections: in Google's RPC protocol an idle client drops its TCP connection and
  health checks over UDP. With very many clients issuing a very low request rate, health checking can
  take more resources than serving the requests.
- Bursts of new connections: very large batch jobs that create many worker tasks at once; negotiating and
  maintaining that many new connections simultaneously can overload a group of backends.

## Connection storm scenario (illustrative)
Backend restarts or failover -> all clients reconnect at once -> connection setup saturates the new
backends -> health checks fail -> clients move to other backends -> they saturate -> cascade.

## Prevention
| Control | How |
|---|---|
| Tune connection parameters | the book: significantly lower the health-check frequency, or create and destroy connections dynamically |
| Batch proxies | the book: mandate that batch client jobs go through a separate set of proxy tasks that only forward requests ("batch client -> batch proxy -> backend"); only the proxy job suffers at job start, like a fuse, and it reduces connections to the backend |
| Load-aware cross-datacenter balancing | the book: base balancing on cluster utilization, not just request count, so load shifts to datacenters with spare capacity |
| Subsetting | limit the pool of backends each client connects to |
| Jittered reconnect backoff | standard practice; check the exact defaults of your RPC library in its documentation |
| Server-side connection limits | look up your proxy's or server's connection-limit settings (for example circuit-breaker limits) in its docs |

## Monitoring
Connections open per backend, new connections per second, health-check traffic versus request traffic, and
file-descriptor usage per process.

## Gotchas
- Health checks that do real work multiply load; keep them cheap and separate from deep checks.
- Clients with no backoff after a DNS failover can hammer the new target; test failover under load.

## Verify
- [ ] Restart a backend tier under load: new-connection rate stays bounded, no cascade.
- [ ] Alerts on connection counts and fd usage.

## Checked
2026-11-01. Confirmed against the SRE Book "Handling Overload" chapter (connection load, idle health checks,
bursts from batch jobs, batch proxy, load-aware balancing). Removed: the health-check arithmetic, gRPC
backoff defaults, Envoy `max_connections` YAML, PgBouncer, TLS resumption, MaxConnectionAge and `nstat`
counters (no fetched page states them; the Envoy circuit-breaking page text did not show those fields).
Method: documentation only; no commands were run.
