---
id: computing-software.networking-hardware-and-wireless.envoy.upstream-connection-pooling
name: upstream-connection-pooling
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, connection-pool, http1, http2, http3, max-concurrent-streams, max-requests-per-connection, goaway]
level: practitioner
status: docs-checked
description: "How Envoy HTTP connection pools behave for HTTP/1.1 and HTTP/2 upstreams, including stream limits, GOAWAY and when new connections open."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/upstream/connection_pooling.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# upstream connection pooling
Envoy layers abstract connection pools over HTTP/1.1, HTTP/2 and HTTP/3 so filters do not care about multiplexing.

HTTP/1.1: connections are acquired as needed up to the circuit-breaker limit. A request binds to a connection when one frees up or a new connection is ready. There is no pipelining, so a severed upstream connection resets only one downstream request.

HTTP/2: many requests are multiplexed on a connection up to `max_concurrent_streams` (in `http2_protocol_options`) and the cluster's `max_requests_per_connection`. With no limits a single connection is used. On a GOAWAY frame or on hitting max requests per connection the pool drains that connection. A connection at its stream limit is marked busy until a stream frees. The HTTP/2 pool establishes as many connections as are needed; with no limits that is a single connection.

```yaml
clusters:
- name: backend
  max_requests_per_connection: 1000
  typed_extension_protocol_options:
    envoy.extensions.upstreams.http.v3.HttpProtocolOptions:
      "@type": type.googleapis.com/envoy.extensions.upstreams.http.v3.HttpProtocolOptions
      explicit_http_config:
        http2_protocol_options: { max_concurrent_streams: 100 }
```
Gotchas from the docs: each worker thread keeps its own pools per cluster, and separate pools are also allocated per routing priority, socket options and transport socket options. When health checking marks a host unavailable, all its pool connections are closed and fresh ones are made when it returns. For a forward proxy the docs recommend `AutoHttpConfig`, which selects HTTP/2 or HTTP/1.1 by ALPN.

## Checked
2026-11-03. Confirmed against connection_pooling.rst and the HttpProtocolOptions reference. Removed or corrected: the 'HTTP/2 preferred for a reverse proxy' gotcha, the circuit-breaker limit on new HTTP/2 connections and the stats verify step.
Method: documentation only; no commands were run.
