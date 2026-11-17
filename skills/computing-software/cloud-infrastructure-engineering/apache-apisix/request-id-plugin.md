---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.request-id-plugin
name: request-id-plugin
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, request-id, correlation-id, uuid, nanoid, ksuid, plugin]
level: intro
status: docs-checked
description: "Stamp requests with an ID in APISIX using request-id: header_name, algorithm (uuid, nanoid, range_id, ksuid), include_in_response and range_id settings."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/request-id.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# request-id plugin

Attributes and defaults:
- `header_name`: `X-Request-Id`. A non-empty incoming value is reused; an empty one counts as missing and a new ID is generated.
- `include_in_response`: true, so the ID is added to the response under `header_name`.
- `algorithm`: `uuid` (default), `nanoid`, `range_id`, `ksuid`.
- `range_id.char_set`: letters and digits by default, minimum length 6.
- `range_id.length`: 16 by default, at least 6.

```json
{
  "plugins": {
    "request-id": {
      "header_name": "X-Req-Identifier",
      "include_in_response": true,
      "algorithm": "range_id",
      "range_id": { "char_set": "abcdefghijklmnopqrstuvwxyz0123456789", "length": 12 }
    }
  }
}
```

Notes:
- Setting `include_in_response` to false still forwards the ID to the upstream but hides it from the client.
- From APISIX 3.15.0 the ID appears in access and error logs; with the plugin disabled the log value falls back to NGINX `$request_id`.
- `ksuid` IDs are sequential and embed a timestamp.

## Checked

2026-11-04. Confirmed against the APISIX request-id plugin page: header_name, empty-value handling, include_in_response, algorithm values, range_id defaults, the upstream-only example, 3.15.0 log behaviour and the $request_id fallback, ksuid wording. Nothing removed.

Method: documentation only; no commands were run.
