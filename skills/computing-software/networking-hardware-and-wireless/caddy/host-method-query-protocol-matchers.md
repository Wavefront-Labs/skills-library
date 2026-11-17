---
id: computing-software.networking-hardware-and-wireless.caddy.host-method-query-protocol-matchers
name: host-method-query-protocol-matchers
category: computing-software
field: networking-hardware-and-wireless
product: caddy
tags: [host-matcher, method-matcher, query-matcher, protocol-matcher, http2, caddyfile]
level: practitioner
status: docs-checked
description: "Use the host, method, query and protocol matchers in the Caddyfile: OR/AND merge rules, key=value query semantics, version suffixes and CEL equivalents."
sources:
  - https://caddyserver.com/docs/caddyfile/matchers
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: select requests on host, verb, query string or protocol.

- `host <hosts...>`: matches the Host header; useful in wildcard-hostname site blocks needing per-host logic. Multiple host matchers are OR-ed. `@site host example.com www.example.com`; CEL `host('app1.example.com', 'app2.example.com')`.
- `method <verbs...>`: case-insensitive in the Caddyfile (converted to uppercase) but uppercase is required inside CEL. Multiple are OR-ed. `@put-delete method PUT DELETE`; CEL `method('GET', 'HEAD', 'OPTIONS')`.
- `query <key>=<val>...`: keys match exactly (case-sensitive), `*` matches any value, values may use placeholders, and `query ""` matches requests with no query. Several matchers: same keys OR-ed, different keys AND-ed. Query values are arrays since keys can repeat; a key matches if any configured value is present. Illegal queries (unescaped semicolons, bad syntax) never match. `@search query q=*`; `@sorted query sort=asc sort=desc`; CEL `query({'sort': ['asc', 'desc'], 'q': '*'})`.
- `protocol http|https|grpc|http/<version>[+]`: broad names or a minimum like `http/2+`. Only one protocol matcher per set. `@http2 protocol http/2+`.

Combine them in one named matcher for AND, or use `expression` for OR across types.

## Checked

2026-11-03: read caddyfile/matchers against this skill. Confirmed: host, method, query and protocol matcher semantics, OR/AND merge rules, CEL forms and examples.
Removed: nothing; no claim failed the check.
Method: documentation only; no commands were run.
