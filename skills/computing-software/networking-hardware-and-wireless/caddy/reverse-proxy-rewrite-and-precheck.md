---
id: computing-software.networking-hardware-and-wireless.caddy.reverse-proxy-rewrite-and-precheck
name: reverse-proxy-rewrite-and-precheck
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [reverse-proxy, method, rewrite, precheck, request-clone, forward-auth]
level: advanced
status: docs-checked
description: "Change the proxied request's method and URI per handler with reverse_proxy method and rewrite, the clone semantics and the pre-check pattern."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/reverse_proxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: send a modified request upstream without affecting later handlers.

By default the upstream request uses the incoming method and URI, unless a rewrite earlier in the chain changed them. Before proxying, Caddy clones the request, so modifications inside the handler do not leak to other handlers; this matters when handling continues after the proxy.

Two subdirectives alter the clone:
- `method <method>`: changes the HTTP method. If it becomes `GET` or `HEAD`, the incoming body is not sent upstream by this handler, which leaves it for another handler to consume.
- `rewrite <to>`: changes the path and query, like the `rewrite` directive except the change does not persist beyond this handler.

Typical use is the pre-check pattern: send a derived request to another server to decide how to continue. For example, ask an authentication gateway whether a session cookie is valid and either continue or redirect to a login page. Caddy provides the `forward_auth` shortcut directive to remove most of the boilerplate for that.

## Checked
2026-11-03. Confirmed against the Caddy reverse_proxy directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
