---
id: computing-software.networking-hardware-and-wireless.envoy.http-connection-manager-lifecycle
name: http-connection-manager-lifecycle
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, http-connection-manager, hcm, http2, http3, codec, stream-lifecycle]
level: practitioner
status: docs-checked
description: "What the HTTP connection manager network filter does, which protocols it speaks, and when a proxied HTTP stream is destroyed or reset."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/http/http_connection_management.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# http connection manager lifecycle
The HTTP connection manager (HCM, `envoy.filters.network.http_connection_manager`) is the built-in network filter that turns raw bytes into HTTP events (headers, body, trailers). It also owns what is common to every HTTP connection: access logging, request ID generation and tracing, request and response header manipulation, route table management and statistics.

Protocols: native HTTP/1.1, HTTP/2 and HTTP/3, including WebSockets. Envoy was designed first as an HTTP/2 multiplexing proxy, so a codec API converts each wire protocol into protocol-agnostic streams; the HTTP/1.1 codec presents serial requests as if they were HTTP/2 streams.

Lifecycle details:
- Proxying starts once the downstream codec has decoded the request headers.
- For HTTP upstreams the stream is destroyed when the response reaches end-of-stream, even if the request is still incomplete. An incomplete request at that moment is reset.
- For TCP upstreams (a CONNECT terminated into TCP) with an HTTP/2 or HTTP/3 downstream, independent half close is enabled: the stream ends after both directions finish and the response is 2xx. Setting runtime guard `envoy.reloadable_features.tcp_tunnel_allow_upstream_half_close` to `false` disables it.

Gotcha: an early upstream response (for example a 4xx before the body is uploaded) resets the downstream request, which clients may report as a mid-upload error. Verify with the `http.<stat_prefix>.*` counters and `%RESPONSE_CODE_DETAILS%` in the access log.

## Checked

2026-11-03. Confirmed against: http_connection_manager arch overview, HCM stats page and the substitution formatter page (RESPONSE_CODE_DETAILS). Removed or corrected: nothing.

Method: documentation only; no commands were run.
