---
id: computing-software.networking-hardware-and-wireless.caddy.url-pattern-matcher
name: url-pattern-matcher
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [url-pattern, urlpattern, named-groups, hostname-capture, base-url, ignore-case, caddyfile]
level: advanced
status: docs-checked
description: "Match URLs with the url_pattern matcher: named groups, regex groups, optional parts, absolute patterns, base_url, ignore_case and capture placeholders."
sources:
  - https://caddyserver.com/docs/caddyfile/matchers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: capture URL components with the WHATWG URLPattern syntax.

`url_pattern <pattern> { base_url <url>  ignore_case }`. Compared with `path` it adds named groups (`:id`), regex-limited groups (`:id([0-9]+)`), optional parts (`{/*}?`) and wildcards anywhere. A relative pattern (starting with `/`) matches the path on any scheme and host; an absolute one (`https://example.com/books/:id`) also checks scheme and host, which may contain groups (`https://:sub.example.com/*`). With no query part in the pattern, any query is allowed. `base_url` resolves a relative pattern against a URL, so `/books/:id` with `https://example.com` equals the absolute form. Matching is case-sensitive unless `ignore_case`.

The path is URL-decoded and cleaned of dot segments before matching, and multiple slashes merge unless the pattern has them. The scheme is `https` for TLS connections and `http` otherwise; the host includes any port from the Host header, so non-standard ports belong in the pattern (`https://example.com:8443/*`).

Captures: `{http.url_pattern.<component>.<group>}` where component is `protocol`, `hostname`, `port`, `pathname` or `search`, and group is a name or a zero-based index for unnamed groups. After `/books/:id/*` matches `/books/42/chapters/1`, `pathname.id` is `42` and `pathname.0` is `chapters/1`.

Examples: `@book url_pattern /books/:id([0-9]+)` with `respond @book "Book number {http.url_pattern.pathname.id}"`; `@docs url_pattern /docs{/*}?`. Only one `url_pattern` per set; use `expression url_pattern('<pattern>', '<base_url>')` for more.

## Checked

2026-11-03: read caddyfile/matchers against this skill. Confirmed: syntax with base_url and ignore_case, relative versus absolute patterns, captures {http.url_pattern.<component>.<group>}, one matcher per set and the expression form.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
