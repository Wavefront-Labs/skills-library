---
id: computing-software.cloud-infrastructure-engineering.kong-gateway.correlation-id
name: correlation-id
category: computing-software
field: cloud-infrastructure-engineering
product: kong-gateway
tags: [kong-gateway, kong, correlation-id, kong-request-id, generator, plugins, tracing]
level: intro
status: docs-checked
description: "correlation-id plugin: header_name Kong-Request-ID, generator uuid, uuid#counter (default) or tracker, and echo_downstream to return the ID to the client."
sources:
  - https://raw.githubusercontent.com/Kong/kong/master/kong/plugins/correlation-id/schema.lua
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# correlation-id

| Field | Default | Notes |
|---|---|---|
| `header_name` | `Kong-Request-ID` | header carrying the correlation ID |
| `generator` | `uuid#counter` | one of `uuid`, `uuid#counter`, `tracker` |
| `echo_downstream` | `false` | return the header to the client in the response |

## Checked

2026-11-04. Confirmed against the correlation-id schema.lua: header_name default Kong-Request-ID, generator one_of uuid, uuid#counter, tracker with default uuid#counter, echo_downstream default false. Removed the note about the core X-Kong-Request-Id header and the headers/headers_upstream settings: the cited page does not state it.

Method: documentation only; no commands were run.
