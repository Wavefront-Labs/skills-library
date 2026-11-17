---
id: computing-software.networking-hardware-and-wireless.caddy.matchers-syntax-named-matchers
name: matchers-syntax-named-matchers
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [matchers, named-matchers, matcher-set, wildcard-matcher, websocket, caddyfile, request-matchers]
level: intro
status: docs-checked
description: "Understand Caddyfile request matcher tokens: wildcard, path and @named matchers, AND semantics inside a set, one-line form, site-block scope and the websocket example."
sources:
  - https://caddyserver.com/docs/caddyfile/matchers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: scope a directive to some requests.

A directive that supports matchers shows `[<matcher>]` in its syntax. The token right after the directive name takes one of three forms: `*` (all requests; also the default when omitted), `/path` (starts with a slash, an inlined path matcher), or `@name` (a named matcher). So `reverse_proxy localhost:9000` and `reverse_proxy * localhost:9000` are identical, while `reverse_proxy /api/* localhost:9000` applies only to that prefix. The wildcard is needed only to disambiguate when the directive's first real argument looks like a path, as in `root * <site-directory>` (needed before v2.8.0).

Anything that is not a path or wildcard must be a named matcher, defined inside the site block that uses it: `@name { ... }`, or on one line `@name <matcher> ...`. Use it as `directive @name`. A definition is a matcher set; all matchers in it are AND-ed. Multiple matchers of the same type merge by their own rules (documented per matcher). For arbitrary boolean logic use the `expression` matcher.

Example from the page, proxying HTTP/1.1 WebSocket upgrades to one backend: `@websockets { header Connection *Upgrade*  header Upgrade websocket }`, then `reverse_proxy @websockets localhost:6001` and `reverse_proxy localhost:8080` for everything else. Single-matcher one-liner: `@post method POST`.

Special case: an `expression` matcher whose only content is one quoted CEL string may omit the word `expression`, e.g. ``@not-found `{err.status_code} == 404` ``.

## Checked

2026-11-03: read caddyfile/matchers against this skill. Confirmed: the three matcher token forms, wildcard disambiguation and root * before v2.8.0, named matcher definition, AND merging, WebSocket example, expression shorthand.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
