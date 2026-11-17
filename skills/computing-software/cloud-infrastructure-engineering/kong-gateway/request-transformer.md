---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.request-transformer
name: request-transformer
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, request-transformer, templates, uri-captures, plugins, transformation]
level: practitioner
status: docs-checked
description: "request-transformer plugin: remove, rename, replace, add, append order of operations, header/querystring/body/uri targets, templates like $(headers.x), and limits."
sources:
  - https://developer.konghq.com/plugins/request-transformer/
  - https://raw.githubusercontent.com/Kong/kong/master/kong/plugins/request-transformer/schema.lua
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# request-transformer

Operations run in this order: remove, rename, replace, add, append.

Config sections and targets:
- `remove`: `body`, `headers`, `querystring` (plain names)
- `rename`: `body`, `headers`, `querystring`, as `old:new` pairs
- `replace`: `body`, `headers`, `querystring`, plus `uri`
- `add`, `append`: `body`, `headers`, `querystring`, as `name:value`
- `http_method`: change the method

Templates in values:
- `$(headers.{NAME})` or `$(headers["{NAME}"])`
- `$(query_params.{NAME})`
- `$(uri_captures.{GROUP})`
- `$(shared.{VARIABLE})`

Fallback expression: `$(uri_captures["user-id"] or query_params["user"] or "unknown")`.

Notes:
- Values containing commas must use array notation, not comma-separated lists.
- `X-Forwarded-*` headers cannot be overwritten; use post-function for that.
- Templates read a snapshot of the request taken before transformation, so changing a parameter does not alter another template's value.
- Trailing whitespace or newlines in multi-line templates become part of the output.

Related: Request Transformer Advanced.

## Checked

2026-11-04. Confirmed against the request-transformer schema.lua (remove/rename/replace/add/append sections with body, headers, querystring targets, replace.uri, http_method) and the plugin page (execution order, template forms, fallback expression, comma and X-Forwarded-* notes, non-mutable snapshot, trailing whitespace note).

Method: documentation only; no commands were run.
