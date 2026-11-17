---
id: computing-software.networking-hardware-and-wireless.caddy.reverse-proxy-header-manipulation
name: reverse-proxy-header-manipulation
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [header-up, header-down, x-forwarded-for, trusted-proxies, host-header, re2, reverse-proxy]
level: practitioner
status: docs-checked
description: "Rewrite headers between Caddy and the backend with header_up and header_down: set, add, delete, wildcard and RE2 replace, plus forwarded-header defaults."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/reverse_proxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control what the upstream sees and what the client receives.

`header_up [+|-]<field> [<value|regexp> [<replacement>]]` edits the request going upstream; `header_down` edits the response coming back. No prefix sets, `+` adds another value, `-` deletes, and two arguments do a regular-expression search and replace (RE2, with `$1` style capture references). Examples: `header_up Some-Header "the value"`; `header_down +Some-Header "first value"`; `header_up -Some-Header`; `header_up -Some-*` (suffix wildcard); `header_up -*` (all headers, not recommended); `header_up Some-Header "^prefix-([A-Za-z0-9]*)$" "replaced-$1-suffix"`.

Defaults: incoming headers, including `Host`, pass through unchanged except that Caddy sets or augments `X-Forwarded-For`, sets `X-Forwarded-Proto` and `X-Forwarded-Host`. Incoming values of these are ignored to prevent spoofing. If Caddy sits behind a CDN or other proxy, trust its ranges with `trusted_proxies [private_ranges] <ranges...>`; the page strongly prefers the `servers > trusted_proxies` global option, which applies to all proxies and enables client IP parsing. It warns that Cloudflare in front can leave `X-Forwarded-For` spoofable and links a workaround.

With the `http` transport, `Accept-Encoding: gzip` is added if missing; disable with `compression off`.

HTTPS upstreams: Host must match the TLS server name. Since v2.11.0 Caddy does this automatically; earlier versions used `header_up Host {upstream_hostport}`. Opt out with `header_up Host {hostport}`.

## Checked
2026-11-03. Confirmed against the Caddy reverse_proxy directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
