---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.request-validation-schema
name: request-validation-schema
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, request-validation, json-schema, header-schema, body-schema, plugin]
level: practitioner
status: docs-checked
description: "Validate request headers and bodies in APISIX with request-validation: header_schema, body_schema, rejected_code and rejected_msg, and the default 400 messages."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/request-validation.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# request-validation schema

Attributes:
- `header_schema`, `body_schema`: JSON Schema objects; set at least one.
- `rejected_code`: 400 by default (200-599).
- `rejected_msg`: custom message.
- `max_req_body_size`: 67108864 bytes (minimum 1) buffered into memory; requests with a larger body are rejected.

Require a curl User-Agent and a known Host:

```json
{
  "request-validation": {
    "header_schema": {
      "type": "object",
      "required": ["User-Agent", "Host"],
      "properties": {
        "User-Agent": { "type": "string", "pattern": "^curl/" },
        "Host": { "type": "string", "enum": ["httpbin.org", "httpbin"] }
      }
    },
    "rejected_code": 403,
    "rejected_msg": "Request header validation failed."
  }
}
```

Without `rejected_code` and `rejected_msg`, a failure returns 400 with text such as:
- `property "Host" validation failed: matches none of the enum value`
- `property "User-Agent" validation failed: failed to match pattern "^curl/" with "cli-mock"`
- `property "required_payload" is required` for a missing body field.

## Checked

2026-11-04: read the request-validation plugin page; attributes (max_req_body_size 67108864 and >= 1, rejected_code 400 and 200-599), the at-least-one-schema note, the header schema and 403 custom message example, and the three error texts match. Removed the aside about the status code for oversized bodies.

Method: documentation only; no commands were run.
