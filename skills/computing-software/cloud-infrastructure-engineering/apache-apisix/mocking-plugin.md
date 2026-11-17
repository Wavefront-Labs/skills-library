---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.mocking-plugin
name: mocking-plugin
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, mocking, mock-response, response-example, response-schema, plugin]
level: intro
status: docs-checked
description: "Return mock responses from APISIX without an upstream using mocking: response_example or response_schema, status, content_type, delay and headers."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/mocking.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# mocking plugin

Attributes and defaults:
- `delay`: 0 seconds before responding.
- `response_status`: 200.
- `content_type`: `application/json;charset=utf8`.
- `response_example`: fixed body; supports NGINX variables such as `$remote_addr`.
- `response_schema`: JSON Schema used to generate a body. One of the two body options is needed.
- `with_mock_header`: true; adds `x-mock-by` showing the APISIX version.
- `response_headers`: extra headers.

```json
{
  "id": "mocking-route",
  "uri": "/anything",
  "plugins": {
    "mocking": {
      "delay": 1,
      "response_status": 201,
      "content_type": "application/json",
      "response_headers": { "X-User-Id": "100" },
      "response_example": "{\"Lastname\":\"Brown\",\"Age\":56}"
    }
  },
  "upstream": { "type": "roundrobin", "nodes": { "httpbin.org:80": 1 } }
}
```

Notes:
- Matching requests never reach the upstream.
- If both body options are set, `response_example` wins.
- `response_schema` supports string, number, integer, boolean, object and array; the body is random, and in the page's schema example a field with an `example` keeps that value.

## Checked

2026-11-04: read the mocking plugin page; the attributes table (defaults, response_example precedence, with_mock_header, response_headers), the supported schema types and the example route match. The delay value 1 in the sample is illustrative (delay is an integer in seconds). Reworded the schema-example note to what the page's example shows.

Method: documentation only; no commands were run.
