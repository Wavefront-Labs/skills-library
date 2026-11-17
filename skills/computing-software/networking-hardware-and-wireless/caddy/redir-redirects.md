---
id: computing-software.networking-hardware-and-wireless.caddy.redir-redirects
name: redir-redirects
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [redir, redirect, 301, 302, 308, location-header, caddyfile]
level: practitioner
status: docs-checked
description: "Issue HTTP redirects in a Caddyfile with redir: status code forms (permanent, html, 307/308), keeping the URI with the uri placeholder, and path-to-path moves."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/redir
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: send clients to another URL.

Syntax: `redir [<matcher>] <to> [<code>]`. `<to>` becomes the `Location` header. `<code>` can be a positive integer in the 3xx range (or 401), `temporary` (302 Found, the default), `permanent` (301 Moved Permanently), `html` (an HTML document performs the redirect, useful for browsers but not API clients) or a placeholder that evaluates to a status code.

Method semantics: `temporary` and `permanent` let the user agent change the method, for example POST to GET. When the method must be preserved on the second request, use `307` or `308` explicitly. Caddy itself uses 308 for its automatic HTTP to HTTPS redirects.

Ordering: redir implies the request is rejected as-is, so its directive order is very early.

Examples: `www.example.com { redir https://example.com }` redirects everything to the apex without the path; add `{uri}` (`redir https://example.com{uri}`) to preserve path and query; append `permanent` for a 301. A path-level move is `redir /about-us /about` placed beside `reverse_proxy localhost:9000`.

Without `{uri}` the redirect target replaces the whole URL, so the original path and query are not carried over.

## Checked
2026-11-03. Confirmed against the Caddy redir directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
