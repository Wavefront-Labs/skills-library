---
id: computing-software.networking-hardware-and-wireless.caddy.reverse-proxy-dynamic-upstreams
name: reverse-proxy-dynamic-upstreams
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [dynamic-upstreams, srv-records, a-records, dns, service-discovery, reverse-proxy, multi]
level: advanced
status: docs-checked
description: "Resolve reverse_proxy backends at request time with dynamic srv, a and multi modules, including refresh intervals, resolvers and health-check limits."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/reverse_proxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: fetch the upstream list from DNS instead of static config.

`dynamic <module> ...` is evaluated at every proxy loop iteration (potentially several times per request when retries are on) and is preferred over static upstreams; on error the proxy falls back to any static upstreams. Limits: active health checks do not run for dynamic upstreams, and load balancing and passive checks work best when the list is stable (especially with round robin), so the module should return only healthy backends.

SRV: `dynamic srv [<full_name>] { service  proto  name  refresh  resolvers  dial_timeout  dial_fallback_delay }`. `full_name` is `_service._proto.name`; `proto` is `tcp` or `udp`; `name` can be the full domain if service and proto are empty. `refresh` defaults to `1m`; `dial_fallback_delay` (RFC 6555 Fast Fallback) defaults to `300ms`.

A/AAAA: `dynamic a [<name> <port>] { name  port  refresh  resolvers  dial_timeout  dial_fallback_delay  versions ipv4|ipv6 }`. `versions` defaults to both `ipv4 ipv6`.

Multi: `dynamic multi { <source> [...] }` appends results of several modules, for example a primary SRV cluster backed by a secondary one.

`resolvers` overrides system DNS. Pair with the transport `tls_except_ports` option when some dynamic upstreams speak HTTP and others HTTPS.

## Checked
2026-11-03. Confirmed against the Caddy reverse_proxy directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
