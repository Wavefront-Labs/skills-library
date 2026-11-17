---
id: computing-software.networking-hardware-and-wireless.caddy.reverse-proxy-upstream-tls-and-keepalive
name: reverse-proxy-upstream-tls-and-keepalive
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [upstream-tls, tls-server-name, tls-client-auth, keepalive, http-versions, max-conns-per-host, reverse-proxy]
level: advanced
status: docs-checked
description: "Secure and pool reverse_proxy upstream connections: tls options, SNI name, client auth, trust pool, keepalive settings, HTTP versions and connection caps."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/reverse_proxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: configure TLS to backends and connection pooling in `transport http`.

TLS: `tls` turns it on (automatic with `https://` upstreams or any `tls_*` option). `tls_client_auth` takes either a domain for which Caddy obtains and renews a certificate, or `<cert_file> <key_file>`. `tls_server_name` sets the name used to verify the upstream certificate (default: the upstream host; needed when the address is an IP); a request placeholder works but clones the transport per request, costing performance. `tls_trust_pool <module>` sets trusted CAs like the `tls` directive's `trust_pool`. `tls_insecure_skip_verify` disables verification and must not be used in production. Others: `tls_curves`, `tls_timeout` (default no timeout), `tls_renegotiation never|once|freely` (default `never`), `tls_except_ports` (disable TLS for listed ports, useful with dynamic upstreams).

Pooling: `keepalive` is `off` or a duration, default `2m`; if it exceeds the upstream's own keepalive timeout, HTTP/1.1 requests may fail with "connection reset by peer", idempotent ones are retried, others yield 502. `keepalive_interval` default `30s`; `keepalive_idle_conns` no limit; `keepalive_idle_conns_per_host` default `32`; `max_conns_per_host` caps dialing, active and idle connections, default none.

`versions` accepts `1.1`, `2`, `h2c`, `3`; default `1.1 2`, or `h2c 2` for `h2c://` upstreams. `h2c` bypasses Go's default transport so it is exclusive of other features; `3` is experimental.

## Checked
2026-11-03. Confirmed against the Caddy reverse_proxy directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
