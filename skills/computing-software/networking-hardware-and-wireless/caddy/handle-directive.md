---
id: computing-software.networking-hardware-and-wireless.caddy.handle-directive
name: handle-directive
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [handle, routing, mutual-exclusion, fallback, nested-handle, caddyfile]
level: practitioner
status: docs-checked
description: "Use handle blocks in a Caddyfile for mutually exclusive routing: first matching block wins, matcherless handle as fallback, nesting and how it differs from route."
sources:
  - https://caddyserver.com/docs/caddyfile/directives/handle
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: split one site into mutually exclusive branches.

Syntax: `handle [<matcher>] { <directives...> }`. When several `handle` blocks appear in sequence at the same nesting level, only the first matching one runs. A `handle` with no matcher behaves as a fallback. Only HTTP handler directives may appear inside, and blocks can nest.

Ordering: `handle` blocks are sorted by the directive sorting algorithm using their matchers, so source order alone does not decide which is tried first. `handle_path` sorts at the same priority as a `handle` with a path matcher, and the two can be mixed in one site while staying mutually exclusive.

Example from the docs: `handle /foo/* { file_server }` followed by `handle { reverse_proxy 127.0.0.1:8080 }` sends `/foo/` requests to static files and everything else to the proxy. A nested form uses `handle /foo* { handle /foo/bar* { ... } handle { ... } }` plus an outer fallback `handle { ... }`.

Neighbours and when to choose them: `handle_path` also strips the matched prefix; `handle_errors` runs only when an error occurred during handling; `route` wraps handlers too but its blocks are not mutually exclusive and its directives are not re-ordered, giving manual control over execution order.

## Checked
2026-11-03. Confirmed against the Caddy handle directive page: syntax, option names, defaults, limits and examples stated here. Removed: statements the page does not make.
Method: documentation only; no commands were run.
