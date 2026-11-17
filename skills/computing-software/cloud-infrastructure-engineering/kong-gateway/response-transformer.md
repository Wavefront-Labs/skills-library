---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.response-transformer
name: response-transformer
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, response-transformer, json-types, remove-rename, plugins, transformation]
level: practitioner
status: docs-checked
description: "response-transformer plugin: remove, rename, replace, add, append for headers and JSON properties, json_types, name:value format and the order of operations."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong/plugins/response-transformer/schema.lua
  - https://developer.konghq.com/plugins/response-transformer/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# response-transformer

Modifies the upstream response before Kong returns it. Order of operations: remove, rename, replace, add, append.

Config sections (HTTP protocols only), each with arrays defaulting to empty:

| Section | Fields |
|---|---|
| `remove` | `json`, `headers` |
| `rename` | `json`, `headers` |
| `replace` | `json`, `json_types`, `headers` |
| `add` | `json`, `json_types`, `headers` |
| `append` | `json`, `json_types`, `headers` |

Format rules:
- `rename`, `replace`, `add` and `append` entries are colon-separated pairs matching `^[^:]+:.*$` (`name:value`).
- For `rename` headers, both sides must be valid header names.
- `json_types` entries are `boolean`, `number` or `string`; they set the JSON type of values written by `replace`, `add` and `append`.
- `remove` takes plain names.

Related: Response Transformer Advanced.

## Checked

2026-11-04. Confirmed against the response-transformer schema.lua (sections and fields, empty-array defaults, colon-pair pattern, header-name validation on rename, json_types values) and the plugin page (order of execution, Response Transformer Advanced).

Method: documentation only; no commands were run.
