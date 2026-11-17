---
id: computing-software.networking-hardware-and-wireless.caddy.route-literal-order
name: route-literal-order
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [route, directive-order, sorting, handler-chain, spa, redir, caddyfile]
level: advanced
status: docs-checked
description: "Take manual control of handler order in a Caddyfile with route: why directive sorting breaks redir versus file_server and API versus SPA fallbacks, with fixes."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/route
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run directives in exactly the order you wrote them.

`route [<matcher>] { <directives...> }` evaluates its contents as a single unit and does not re-sort them; only HTTP handler directives are allowed, and its inner directives are ordinary directives. Normally Caddy reorders directives after parsing so you need not care about order; use `route` when the built-in order is wrong.

Case 1: `file_server /specific.html` followed by `redir https://anothersite.com{uri}` fails, because after sorting `redir` runs earlier and its implicit `*` matcher is a superset of the file path. Wrapping both in a `route` makes `file_server` run first. Both are terminal handlers, so mutual exclusivity is implicit.

Case 2 (SPA with API): `try_files` sorts ahead of `reverse_proxy`, so API calls would be rewritten to `/index.html` before matching `/api*`. Fix: `root /srv`, then `route { reverse_proxy /api* localhost:9000  try_files {path} /index.html  file_server }`. The proxy now runs first. An alternative is two `handle` blocks, the first matching `/api*`.

Compared with its siblings: `handle` blocks are mutually exclusive and their contents are re-ordered; `route` blocks are neither. `handle_path` strips a prefix; `handle_errors` runs on errors.

Gotcha: a `route` does not make sibling routes exclusive, so use `handle` for branching and `route` only for ordering.

## Checked
2026-11-03. Confirmed against the Caddy route directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
