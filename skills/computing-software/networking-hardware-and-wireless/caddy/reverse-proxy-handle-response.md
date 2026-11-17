---
id: computing-software.networking-hardware-and-wireless.caddy.reverse-proxy-handle-response
name: reverse-proxy-handle-response
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [handle-response, replace-status, copy-response, response-matcher, rp-placeholders, reverse-proxy]
level: advanced
status: docs-checked
description: "Intercept upstream responses in reverse_proxy with handle_response, replace_status, copy_response and copy_response_headers and the rp placeholders."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/reverse_proxy
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: act on what the backend returned before the client sees it.

Define named response matchers inside the proxy block (`@name { status <code...>  header <field> [<value>] }`) and use `replace_status [<matcher>] <code>` to change just the status, or `handle_response [<matcher>] { ... }` for a full route. The first matching `handle_response` runs; without a matcher it applies to all responses. The backend response is not written; the route must write one, and if it does not, handling continues with handlers ordered after `reverse_proxy`.

Two special directives exist only inside `handle_response`: `copy_response [<matcher>] [<status>] { status <status> }` copies the backend's body to the client (optionally with a new status; it is ordered before `respond`), and `copy_response_headers [<matcher>] { include <fields...>  exclude <fields...> }` copies headers (include or exclude, not both; ordered after `header`).

Placeholders there: `{rp.status_code}`, `{rp.status_text}` and `{rp.header.*}`.

Limit: a subsequent `reverse_proxy` cannot receive the new response; every use gets the original request body (or as modified by a different module).

## Checked
2026-11-03. Confirmed against the Caddy reverse_proxy directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
