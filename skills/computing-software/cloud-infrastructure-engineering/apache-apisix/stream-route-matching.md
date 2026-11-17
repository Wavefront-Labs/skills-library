---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.stream-route-matching
name: stream-route-matching
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, stream-routes, sni, snis, remote-addr, server-port, tls-passthrough]
level: advanced
status: docs-checked
description: "Create APISIX stream routes that match by remote_addr, server_addr and server_port, sni or snis, with TLS upstream scheme and tls_passthrough behavior."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/stream-proxy.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Stream route matching

Create with PUT to `/apisix/admin/stream_routes/{id}` and the `X-API-KEY` header. Match keys:
- `remote_addr`: client address.
- `server_addr` plus `server_port`: APISIX listen address and port.
- `sni`: one server name; or `snis`: an array. Use one, not both.

```json
{ "server_addr": "127.0.0.1", "server_port": 2000,
  "upstream": { "nodes": { "127.0.0.1:1995": 1 }, "type": "roundrobin" } }
```

```json
{ "snis": ["a.test.com", "b.test.com"],
  "upstream": { "nodes": { "127.0.0.1:5991": 1 }, "type": "roundrobin" } }
```

Upstream over TLS: `"upstream": {"scheme": "tls", ...}`.

SNI notes:
- `snis` wildcards match as a suffix (`*.test.com` matches `a.b.test.com`); a single `*` matches any SNI; connections without SNI fall through to address-based routes.
- With a `tls` upstream the client's SNI is passed on; otherwise the dummy SNI `apisix_backend` is used.
- `tls_passthrough: true` forwards the handshake unchanged while routing still uses SNI. `tls` upstreams return 503 on passthrough ports.
- A port with both `tls: true` and `tls_passthrough: true` is mixed: each route picks passthrough with its own flag (default false). Mixed ports add an internal hop and reject `proxy_protocol_to_upstream`.

## Checked

2026-11-04: read the Stream Proxy page (route filtering, TLS over TCP, TLS upstream, TLS passthrough and mixed-port sections); the match attributes, sni and snis examples, one-of rule, suffix wildcard behaviour, apisix_backend dummy SNI, passthrough 503 for tls upstreams and mixed-port rules match. Nothing removed.

Method: documentation only; no commands were run.
