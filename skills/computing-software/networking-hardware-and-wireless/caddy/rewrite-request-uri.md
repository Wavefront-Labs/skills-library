---
id: computing-software.networking-hardware-and-wireless.caddy.rewrite-request-uri
name: rewrite-request-uri
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [rewrite, uri, query-string, internal-rewrite, placeholders, caddyfile]
level: practitioner
status: docs-checked
description: "Internally rewrite the request URI in a Caddyfile with rewrite: path and query handling, placeholders, exclusivity, and the post-rewrite matcher caveat."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/rewrite
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: change the path or query a handler sees without telling the client.

Syntax: `rewrite [<matcher>] <to>`. Only the URI components present in `<to>` are changed. The path is everything before `?`; if there is no `?`, the entire token is the path. A placeholder that expands to something containing `?` (for example `rewrite {rp.header.X-Accel-Redirect}` with value `/file?v=2`) replaces the query too, unless `<to>` itself has a `?`. Anything from `#` on is dropped.

Behaviour: rewrite is internal and implies accepting the request with modifications. Rewrites in the same block are mutually exclusive, so only the first matching one runs and cascades cannot occur. A matcher that matched before the rewrite may not match the same request afterwards; to keep a rewrite and its consumers in one route, wrap them in `route` or `handle`.

Examples: `rewrite /index.html` sends everything to index.html and leaves the query unchanged; `rewrite /api{uri}` prefixes `/api` before `reverse_proxy localhost:8080`; `rewrite ?a=b` replaces only the query; `rewrite /api/* ?{query}&a=b` adds a pair while preserving the old query; `rewrite /index.php?{query}&p={path}` moves the original path into parameter `p`.

Version note: before v2.8.0 a `/`-leading target was ambiguous with a matcher, so a wildcard `*` was required (`rewrite * /foo`). That is no longer needed.

Related: `uri` for strip/replace edits, `try_files` for existence-based rewrites.

## Checked
2026-11-03. Confirmed against the Caddy rewrite directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
