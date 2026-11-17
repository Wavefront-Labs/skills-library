---
id: computing-software.networking-hardware-and-wireless.caddy.uri-path-manipulation
name: uri-path-manipulation
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [uri, strip-prefix, strip-suffix, path-regexp, replace, normalization, caddyfile]
level: practitioner
status: docs-checked
description: "Edit the request path with the Caddyfile uri directive: strip_prefix, strip_suffix, replace with limit and path_regexp, plus normalisation and escaped-slash rules."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/uri
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: make partial changes to a request URI, unlike `rewrite`, which replaces it.

Forms: `uri [<matcher>] strip_prefix <target>`, `strip_suffix <target>`, `replace <target> <replacement> [<limit>]` (substring replacement over the whole URI, optional maximum count), and `path_regexp <target> <replacement>` (regular expression on the path only). Replacements support `$name`, `${name}` and `$1` capture references; `""` removes the match. A prefix target may omit its leading slash. In JSON both `uri` and `rewrite` produce the same rewrite handler, with `uri` setting fields like `strip_path_prefix` and `path_regexp`.

Examples: `uri strip_prefix /api`; `uri strip_suffix .php`; `uri replace /docs/ /v1/docs/`; `uri path_regexp /{2,} /` collapses repeated slashes in the path only.

Normalisation: mutations act on the normalised, unescaped URI, but escapes in your pattern match only those literal escapes. `uri strip_prefix /a/b` rewrites both `/a/b/c` and `/a%2Fb/c` to `/c`, whereas `strip_prefix /a%2Fb` matches only the escaped form. The path is cleaned of dot segments first; multiple slashes merge unless the target has them too. After stripping, the path always begins with `/` and is cleaned again: `/api` becomes `/`, `/apix` becomes `/x`, and `/api../secret` becomes `/secret`.

`handle_path` is the shortcut when you also want mutual exclusivity.

## Checked
2026-11-03. Confirmed against the Caddy uri directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
