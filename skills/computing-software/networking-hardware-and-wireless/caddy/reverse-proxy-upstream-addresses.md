---
id: computing-software.networking-hardware-and-wireless.caddy.reverse-proxy-upstream-addresses
name: reverse-proxy-upstream-addresses
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [reverse-proxy, upstreams, h2c, unix-socket, port-range, scheme, caddyfile]
level: practitioner
status: docs-checked
description: "Write valid reverse_proxy upstream addresses: schemes (https, h2c), unix sockets, port ranges, IPv6 zones, no paths, and placeholder caveats."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/reverse_proxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: point reverse_proxy at backends correctly.

Upstreams are listed inline or with `to`. Accepted forms: `localhost:4000`, `127.0.0.1:4000`, `[::1]:4000`, `http://localhost:4000`, `https://example.com`, `h2c://127.0.0.1`, bare `example.com`, `unix//var/php.sock`, `unix+h2c//var/grpc.sock`, `localhost:8001-8006` and `[fe80::ea9f:80ff:fe46:cbfd%eth0]:443`.

Connections are plaintext HTTP by default. In URL form the scheme sets transport defaults: `https://` uses the `http` transport with `tls` on; `h2c://` allows cleartext HTTP/2; `http://` is the same as no scheme. Schemes cannot be mixed in one proxy, because they modify the shared transport, and an explicit transport block is never overwritten. A link-local IPv6 address with a zone (`%eth0`) breaks URL parsing, so configure the transport explicitly instead of using a scheme. In network-address form the network prefix (`unix/`) cannot combine with a URL scheme; `unix+h2c/` is the special-case shortcut. A port range expands to several upstreams on the same host.

Upstreams must not contain a path or query, because that would imply rewriting while proxying; use `rewrite` for that.

Placeholders are allowed only in non-URL addresses and make the upstream "dynamically static": many backends behave as one for health checks and balancing. A port must be present, from the placeholder or a static suffix. Prefer a dynamic upstreams module where possible.

## Checked
2026-11-03. Confirmed against the Caddy reverse_proxy directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
