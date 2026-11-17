---
id: computing-software.networking-hardware-and-wireless.envoy.local-reply-customization
name: local-reply-customization
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, local-reply, local-reply-config, mappers, body-format, status-code-filter]
level: practitioner
status: docs-checked
description: "Customise responses Envoy generates itself (503, 429, etc.) with LocalReplyConfig mappers, body formats and the ordering of substitution variables."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/configuration/http/http_conn_man/local_reply.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# local reply customization
The HTTP connection manager can modify local replies, meaning responses that Envoy itself produces rather than the upstream. Supported: content modification and format modification.

A list of `mappers` is given; each needs a `filter` and may have rewrite rules, applied in this order:
1. `body` sets a static body.
2. `headers_to_add` evaluates headers; substitution variables such as `%RESPONSE_CODE%` resolve to the original code here.
3. `status_code` rewrites the code in both the headers and the stream info.
4. `body_format_override` (or fallback `body_format`) formats the body; variables now resolve to the overridden code.

```yaml
local_reply_config:
  mappers:
  - filter:
      status_code_filter:
        comparison: { op: EQ, value: { default_value: 503, runtime_key: key_b } }
    status_code: 401
    body: { inline_string: "not allowed" }
```
Gotcha: because of that ordering `%RESPONSE_CODE%` can differ between `headers_to_add` and `body_format_override`; compute needed values with that in mind. Only Envoy-generated responses are affected, not upstream bodies. Verify by forcing a local reply (for example kill the upstream to get a 503) and checking headers and body, and `%RESPONSE_CODE_DETAILS%` in the access log.

## Checked

2026-11-03. Confirmed against: local_reply.rst (mapper rewrite order, body_format_override) and the substitution formatter page. Removed or corrected: nothing.

Method: documentation only; no commands were run.
