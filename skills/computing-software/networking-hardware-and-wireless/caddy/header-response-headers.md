---
id: computing-software.networking-hardware-and-wireless.caddy.header-response-headers
name: header-response-headers
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [header, response-headers, defer, re2, cors, cache-control, hsts, caddyfile]
level: practitioner
status: docs-checked
description: "Manipulate response headers in a Caddyfile with header: set, add, delete, default and deferred operations, RE2 replacement and match conditions, with the page's patterns."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/header
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: set, remove or rewrite response headers correctly, including after a proxy has written its own.

Syntax: `header [<matcher>] [[+|-|?|>]<field> [<value>|<find>] [<replace>]]`, or a block with one operation per line. Prefixes: none sets (overwrites); `+` adds another value; `-` deletes (leading or trailing `*` wildcards delete all matching fields); `?` sets a default only if the field is not yet present; `>` sets with `defer` enabled. Two values after the field mean search and replace: `<find>` is an RE2 regular expression (placeholders allowed), `<replace>` may use `$1`, `$2` capture groups, and `""` removes the match.

Defer: operations normally run immediately. They are deferred to write time automatically when you delete with `-`, use a `?` default, use the `>` prefix, or have a `match` block. Without defer, a header set before `reverse_proxy` can be overwritten by the upstream; the page's fix is `header /no-cache* >Cache-Control no-cache`. A `?` operation inside a multi-operation block is split into its own handler.

`match <inline_response_matcher>` limits operations to qualifying responses, such as `match status 2xx` or `match status 500` (used with `-Cache-Control` and `-CDN-Cache-Control` to stop caching errors).

Recipes: `header Location http:// https://` rewrites redirects; `header ?Cache-Control "max-age=3600"` supplies a default; `header >Access-Control-Allow-Origin "\*" "allowed-partner.com"` replaces a wildcard CORS value, and the `*` must be escaped because find is a regex; `header >Set-Cookie (.*) "$1; SameSite=None;"` appends an attribute. Security headers example: `Strict-Transport-Security max-age=31536000;`, `X-Content-Type-Options nosniff`, `X-Frame-Options DENY`, which the page warns to use only if you understand the implications.

Wrap in `route` for mutually exclusive variants: `header Cache-Control max-age=3600` then `header /static/* Cache-Control max-age=31536000`.

## Checked
2026-11-03. Confirmed against the Caddy header directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
