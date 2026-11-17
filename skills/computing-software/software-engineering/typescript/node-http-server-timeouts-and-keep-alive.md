---
id: computing-software.software-engineering.typescript.node-http-server-timeouts-and-keep-alive
name: node-http-server-timeouts-and-keep-alive
category: computing-software
field: software-engineering
product: typescript
tags: [typescript, node-http-server, keepalivetimeout, requesttimeout, headerstimeout, load-balancer-502, nodejs]
level: advanced
status: gated
description: "Configure Node HTTP servers: requestTimeout, headersTimeout, keepAliveTimeout vs load balancer idle timeouts (the 502 trap), body size limits, and outbound agent keep-alive."
sources: ["https://nodejs.org/api/http.html#class-httpserver", "https://nodejs.org/api/http.html#serverkeepalivetimeout", "https://docs.aws.amazon.com/elasticloadbalancing/latest/application/application-load-balancers.html#connection-idle-timeout", "https://nodejs.org/api/http.html#class-httpagent"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node HTTP server timeouts and keep-alive

**Goal:** a Node service behind a load balancer with no intermittent 502s, no
slowloris exposure and efficient outbound connections.

## Server timeouts (Node 18+ defaults; read back unchanged on Node 20.20 and 24.22)
| Setting | Default | Meaning |
|---|---|---|
| `server.requestTimeout` | 300000 ms | max time to receive the entire request |
| `server.headersTimeout` | 60000 ms | max time to receive headers (slowloris defence) |
| `server.keepAliveTimeout` | 5000 ms | idle time before closing a keep-alive socket |
| `server.timeout` | 0 (none) | socket inactivity timeout |
```ts
import http from "node:http";
const server = http.createServer(app);
server.keepAliveTimeout = 65_000;     // > load balancer idle timeout (ALB default 60 s)
server.headersTimeout = 66_000;       // should exceed keepAliveTimeout (common guidance)
server.requestTimeout = 120_000;      // must be >= headersTimeout (see below)
server.listen(8080);
```
Tested on Node 24.22: `http.createServer({ requestTimeout: 30000, headersTimeout: 66000 })` throws `ERR_OUT_OF_RANGE` ("headersTimeout ... must be <= requestTimeout"), so keep `headersTimeout <= requestTimeout` when both are non-zero; the Node docs default `headersTimeout` to the lower of `requestTimeout` and 60000. The "headersTimeout should exceed keepAliveTimeout" rule is common operational guidance that the Node docs page does not state (gated: unconfirmed, source is paywalled or blocked).

Same properties exist on the server returned by Express's `app.listen()`; Fastify exposes
`keepAliveTimeout`/`connectionTimeout`/`requestTimeout` options.

## The intermittent 502 trap
The load balancer reuses idle upstream connections for up to its idle timeout (ALB 60 s default per the AWS docs, which also recommend an application idle timeout longer than the LB's to avoid 502s; GCP LB 600 s (gated: unconfirmed, source is paywalled or blocked), nginx `keepalive_timeout`). Node closes idle sockets after 5 s. If Node closes a
socket at the same moment the LB sends a request on it, the LB gets a reset -> 502. Fix:
upstream keep-alive timeout **longer** than the LB's idle timeout.

## Body limits
Node itself does not limit body size; frameworks do (`express.json({ limit: "1mb" })`,
Fastify `bodyLimit`). Set them explicitly; also `server.maxHeadersCount` and
`--max-http-header-size` (16 KB default; tested `http.maxHeaderSize` is 16384) if large cookies/JWTs cause 431 errors.

## Graceful shutdown interaction
`server.close()` stops new connections but keep-alive sockets stay open until idle; call
`server.closeIdleConnections()` (Node 19+) and set a hard deadline with
`server.closeAllConnections()`.

## Outbound: reuse connections
Node 19+ enables keep-alive on the global agent by default. For heavy outbound traffic:
```ts
import { Agent, setGlobalDispatcher } from "undici";   // powers global fetch()
setGlobalDispatcher(new Agent({ connections: 100, keepAliveTimeout: 30_000, headersTimeout: 10_000, bodyTimeout: 30_000 }));
```
`fetch()` has no default overall timeout: pass `signal: AbortSignal.timeout(5000)`.

## Verify
- [ ] keepAliveTimeout > LB idle timeout, headersTimeout > keepAliveTimeout.
- [ ] Load test through the real LB shows zero 502s over a long run with idle gaps.
