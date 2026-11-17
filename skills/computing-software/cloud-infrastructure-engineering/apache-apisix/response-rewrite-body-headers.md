---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.response-rewrite-body-headers
name: response-rewrite-body-headers
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, response-rewrite, response-headers, body, filters, status-code, plugin]
level: practitioner
status: docs-checked
description: "Rewrite APISIX responses with response-rewrite: status_code, body, body_base64, header add/set/remove, regex filters, vars conditions and phase caveats."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/response-rewrite.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# response-rewrite

Attributes (all optional):
- `status_code`: 200-598; default keeps the original.
- `body`: replaces the body and resets Content-Length. Do not combine with `filters`.
- `body_base64`: false; decodes the configured `body` only, not the upstream response.
- `headers`: `add` (array), `set` (object), `remove` (array); run in order add, remove, set. Values accept NGINX variables.
- `vars`: lua-resty-expr conditions that gate the plugin.
- `filters`: regex replace on the body, each with `regex`, `replace`, `scope` (`once` default, or `global`) and `options` (default `jo`).
- `max_resp_body_size`: 67108864 bytes buffered for filters.

Only rewrite 200 responses:

```json
"response-rewrite": {
  "body": "{\"code\":\"ok\",\"message\":\"new json body\"}",
  "headers": { "set": { "X-Server-id": 3, "X-Server-balancer-addr": "$balancer_ip:$balancer_port" } },
  "vars": [["status","==",200]]
}
```

Regex filter:

```json
"response-rewrite": { "filters": [ { "regex": "X-Amzn-Trace-Id", "scope": "global", "replace": "X-Amzn-Trace-Id-Replace" } ] }
```

Phase caveat: header_filter and body_filter still run after another plugin exits early, so an auth failure from `key-auth` can also be rewritten (for example to 200).

## Checked

2026-11-04: read the response-rewrite plugin page; the attributes table (status_code 200-598, body and Content-Length, body_base64 scope, headers order, vars, filters with once and jo defaults, max_resp_body_size 67108864), the 200-only example, the regex filter example and the key-auth phase caveat match. Nothing removed.

Method: documentation only; no commands were run.
