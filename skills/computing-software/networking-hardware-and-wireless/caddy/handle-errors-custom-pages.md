---
id: computing-software.networking-hardware-and-wireless.caddy.handle-errors-custom-pages
name: handle-errors-custom-pages
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [handle-errors, error-pages, err-status-code, placeholders, 4xx, 5xx, caddyfile]
level: practitioner
status: docs-checked
description: "Serve custom error responses with handle_errors in a Caddyfile: status code filters including 4xx and 5xx, err placeholders, and which responses do not trigger it."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/handle_errors
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: control what clients see when request handling fails.

Syntax: `handle_errors [<status_codes...>] { <directives...> }`. Codes may be 3-digit numbers or the ranges `4xx` and `5xx`. With no codes it matches any error and acts as the fallback. Repeat the directive to treat errors differently. The block is an ordinary route, so it can serve files, run templates or proxy elsewhere, and the request context (site `root`, `vars`) carries over.

Placeholders inside: `{err.status_code}`, `{err.status_text}`, `{err.message}`, `{err.trace}` (origin of the error) and `{err.id}` (identifier for this occurrence).

Patterns from the page: `handle_errors { rewrite /{err.status_code}.html  file_server }` serves `404.html` for 404s; `file_server` keeps the error status. To fall back when a file is missing, define `@custom_err file /err-{err.status_code}.html /err.html`, then `handle @custom_err { rewrite {file_match.relative}  file_server }` and a final `respond "{err.status_code} {err.status_text}"`. Separate treatment: `handle_errors 404 410 { ... }`, `handle_errors 5xx { ... }`, then a bare `handle_errors { ... }`.

Important limits: some directives, notably `reverse_proxy`, can write an error-class status without raising an error, and that does not trigger error routes. Use the `error` directive to raise one deliberately.

## Checked
2026-11-03. Confirmed against the Caddy handle_errors directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
