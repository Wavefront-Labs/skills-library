---
id: computing-software.devops-ci-cd.deployment-strategies.keep-alive-and-idle-timeout-alignment
name: keep-alive-and-idle-timeout-alignment
category: computing-software
field: devops-ci-cd
product: deployment-strategies
tags: [deployment-strategies, keep-alive-timeout, idle-timeout, 502-bad-gateway, connection-reset, zero-downtime, graceful-shutdown]
level: practitioner
status: draft
description: "Prevent intermittent 502s and resets during deploys by aligning keep-alive and idle timeouts across load balancers, proxies and app servers, plus graceful connection draining."
sources:
  - https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#connection-idle-timeout
  - https://nodejs.org/api/http.html#serverkeepalivetimeout
  - https://nginx.org/en/docs/http/ngx_http_upstream_module.html#keepalive_timeout
  - https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Keep-alive and idle timeout alignment

## The rule
**Each downstream (server) side must keep idle connections open longer than the upstream (client) side that reuses them.** Otherwise the server closes an idle connection at the same moment the proxy sends a new request on it, and the proxy returns 502/504 or the client sees `ECONNRESET`.

Chain example: client -> ALB (idle 60 s) -> nginx (keepalive_timeout) -> app (Node keepAliveTimeout).
- ALB idle timeout 60 s => nginx `keepalive_timeout` > 60 s (e.g. 75 s).
- nginx upstream `keepalive_timeout` (to the app, default 60 s) => app keep-alive > that (e.g. 65 s+).

## Defaults that cause trouble
| Component | Default idle/keep-alive |
|---|---|
| AWS ALB idle timeout | 60 s |
| GCP HTTP(S) LB backend keep-alive | 600 s (so backends must exceed 600 s, Google recommends 620 s) |
| Azure Application Gateway | ~ 120 s+ (check SKU) |
| Node.js `server.keepAliveTimeout` | 5 s (way too low behind any LB) |
| Go `http.Server.IdleTimeout` | falls back to ReadTimeout, or no limit |
| Gunicorn `--keep-alive` | 2 s |
| nginx `keepalive_timeout` (client side) | 75 s |

## Fixes per runtime
```js
// Node.js behind ALB
server.keepAliveTimeout = 65_000;
server.headersTimeout = 66_000;   // must exceed keepAliveTimeout
```
```bash
gunicorn app:app --keep-alive 75          # behind an LB with 60 s idle
```
```go
srv := &http.Server{IdleTimeout: 75 * time.Second, ReadHeaderTimeout: 10 * time.Second}
```

## During deploys (graceful shutdown)
Even with correct timeouts, terminating pods/instances drop in-flight and idle connections:
1. Stop receiving new traffic first: deregister from the LB (ALB deregistration delay, readiness probe failing) **before** the process exits.
2. Kubernetes: endpoints removal and SIGTERM happen concurrently, so add `preStop: { sleep: { seconds: 10 } }` (1.30+ native sleep, or `exec: sleep 10`) and set `terminationGracePeriodSeconds` > preStop + drain time.
3. On SIGTERM, the app stops accepting, sends `Connection: close` on responses, finishes in-flight requests, closes idle keep-alive connections (`server.close()` + `closeIdleConnections()` in Node 18.2+), then exits.
4. Long-lived connections (WebSockets, gRPC streams) need explicit drain logic (GOAWAY for HTTP/2, reconnect signals).

## Diagnose
- ALB access logs: `elb_status_code=502` with `target_status_code=-` and short `target_processing_time` = target closed connection.
- nginx error log: `upstream prematurely closed connection while reading response header`.
- Spikes exactly at deploy times = shutdown ordering; random low-rate 502s = timeout mismatch.

## Verify
- [ ] Load test at steady low rate for 30 minutes shows zero 502s; same test across a rolling deploy shows zero errors.
- [ ] Timeouts documented per hop with the server side always longer.
