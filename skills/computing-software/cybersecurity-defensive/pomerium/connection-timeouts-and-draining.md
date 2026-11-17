---
id: computing-software.cybersecurity-defensive.pomerium.connection-timeouts-and-draining
name: connection-timeouts-and-draining
category: computing-software
field: cybersecurity-defensive
product: pomerium
tags: [timeout-idle, idle-timeout, connection-draining, listeners, long-lived-connections]
level: advanced
status: docs-checked
description: "Tune Pomerium timeouts for long-lived connections, understand connection draining on config changes, and map its listeners and settings."
sources:
  - https://raw.githubusercontent.com/pomerium/documentation/main/content/docs/internals/connection.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Timeouts**
- Upstream connect (incl. TLS handshake): 10s, not configurable.
- Stream idle: global `timeout_idle`; per-route `idle_timeout` can disable it but not exceed the global value.
- Request total: global `timeout_write`; raise for large uploads.
- Upstream round trip: per-route `timeout`, defaulting to `default_upstream_timeout`.

**Long-lived connections** (WebSockets, gRPC streaming, SSE, TCP): TCP routes and routes with `allow_websockets` adjust automatically. For gRPC streaming or SSE set the route `idle_timeout` to `0`.

**Draining**: most changes (adding a route) do not disturb live connections. Major global changes such as TLS certificate changes recreate the handler; old connections are told to close (HTTP/2 GOAWAY, HTTP/1 `Connection: close`) and are terminated after about 10 minutes. Watch `envoy_listener_manager_total_filter_chains_draining` (1 means draining). For long-lived workloads use long-lived certificates and avoid big global changes.

**HTTP versions**: HTTP/1.1 and HTTP/2 by default; HTTP/3 via `codec_type`.

**Listeners and settings**: `http-ingress` (port 80, `http_redirect_address`), `https-ingress` (443, `address`), `quic-ingress` (UDP, `codec_type: http3`), `grpc-ingress` (`grpc_addr`), `envoy-admin` (`envoy_admin_address`, restrict at network layer), `metrics-ingress` (9902, `metrics_address`), `ssh` (22, `ssh_address`).

## Checked

2026-11-04. Read the Connections page: the four timeouts and their settings, long-lived connection handling, draining behaviour with the 10 minute grace period and metric, HTTP version defaults and the listener table all confirmed. Nothing removed.

Method: documentation only; no commands were run.
