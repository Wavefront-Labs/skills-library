---
id: computing-software.networking-hardware-and-wireless.caddy.reverse-proxy-http-transport-timeouts
name: reverse-proxy-http-transport-timeouts
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [http-transport, dial-timeout, response-header-timeout, proxy-protocol, read-buffer, resolvers, reverse-proxy]
level: advanced
status: docs-checked
description: "Tune the reverse_proxy http transport: dial, response header, read and write timeouts, buffers, max_response_header, PROXY protocol and DNS resolvers."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/reverse_proxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set connection-level limits for `transport http { ... }`.

Defaults and meaning:
- `dial_timeout` 3s: time to connect to the upstream socket.
- `dial_fallback_delay` 300ms: wait before an RFC 6555 Fast Fallback connection; negative disables.
- `response_header_timeout`: wait for response headers; default none.
- `expect_continue_timeout`: wait for first response headers after writing request headers when `Expect: 100-continue` is present; default none.
- `read_timeout` and `write_timeout`: wait for the next read or write to the backend; default none.
- `read_buffer` and `write_buffer`: 4KiB each; `max_response_header`: 10MiB; sizes accept go-humanize formats.
- `proxy_protocol v1|v2`: prepend PROXY protocol data with the real client IP; only if the upstream parses it; best with `servers > trusted_proxies` when Caddy is behind another proxy; off by default.
- `resolvers <ip...>`: override system DNS.
- `network_proxy <module>`: by default Caddy honours `HTTP_PROXY`, `HTTPS_PROXY` and `NO_PROXY`; module `none` ignores them and `url <url>` overrides with one URL. Traffic flows client, reverse_proxy, network_proxy, upstream.

Example: `reverse_proxy app:8080 { transport http { dial_timeout 2s  response_header_timeout 30s } }`.

## Checked
2026-11-03. Confirmed against the Caddy reverse_proxy directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
