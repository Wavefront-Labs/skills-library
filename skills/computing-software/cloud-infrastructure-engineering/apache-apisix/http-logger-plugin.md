---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.http-logger-plugin
name: http-logger-plugin
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, http-logger, logging, log-format, batch-processor, plugin-metadata, plugin]
level: practitioner
status: docs-checked
description: "Ship APISIX logs to an HTTP endpoint with http-logger: uri, auth_header, log_format via plugin metadata, body logging limits, concat_method and batch defaults."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/http-logger.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# http-logger plugin

Plugin attributes:
- `uri` (required): receiving HTTP(S) endpoint; `auth_header` optional.
- `timeout`: 3; `ssl_verify`: false; `concat_method`: `json` (default) or `new_line`.
- `log_format`: custom JSON map using NGINX variables; `log_format_extra` adds fields to the default entry and is ignored if `log_format` is set.
- `include_req_body`, `include_resp_body`: false; the `_expr` variants take lua-resty-expr conditions.
- `max_req_body_bytes`, `max_resp_body_bytes`: 524288.

Batching defaults: submit every 5 seconds or at 1000 queued entries.

Plugin metadata (`/apisix/admin/plugin_metadata/http-logger`) sets a global format and `max_pending_entries` (8192). A `log_format` on the plugin instance wins over metadata.

```json
{
  "log_format": {
    "host": "$host",
    "@timestamp": "$time_iso8601",
    "client_ip": "$remote_addr"
  }
}
```

A custom `log_format` prevents `include_req_body` and `include_resp_body` from adding bodies; use `$request_body` in the format instead.

## Checked

2026-11-04. Confirmed against the APISIX http-logger plugin page: attribute defaults (timeout 3, ssl_verify false, concat_method values, 524288 body limits), log_format and log_format_extra precedence, batch defaults of 5 seconds or 1000 entries, plugin metadata max_pending_entries 8192, the $request_body workaround. Nothing removed.

Method: documentation only; no commands were run.
