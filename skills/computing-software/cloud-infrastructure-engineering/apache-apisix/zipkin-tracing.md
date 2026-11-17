---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.zipkin-tracing
name: zipkin-tracing
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, zipkin, tracing, sample-ratio, span-version, jaeger, plugin]
level: practitioner
status: docs-checked
description: "Trace APISIX requests with zipkin: endpoint, sample_ratio, service_name, span_version 1 versus 2, set_ngx_var log variables and Jaeger or SkyWalking collectors."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/zipkin.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zipkin tracing

Attributes:
- `endpoint` (required): Zipkin collector URL receiving POSTs.
- `sample_ratio` (required): 0.00001 to 1; 1 traces every request.
- `service_name`: `APISIX`.
- `server_addr`: defaults to `$server_addr`; an IPv4 address the reporter uses.
- `span_version`: 2 (default) or 1.

```json
{
  "plugins": {
    "zipkin": {
      "endpoint": "http://127.0.0.1:9411/api/v2/spans",
      "sample_ratio": 1,
      "span_version": 2
    }
  }
}
```

Notes:
- Tracing adds per-request cost; lower `sample_ratio` on busy routes. Unsampled requests skip span tag construction.
- Span version 2 creates `request`, `proxy` and `response` spans. Version 1 creates `request`, `rewrite`, `access`, `proxy` and `body_filter` spans.
- Set `plugin_attr.zipkin.set_ngx_var: true` in `config.yaml` (default false, reload needed) to expose `zipkin_context_traceparent`, `zipkin_trace_id` and `zipkin_span_id` for logs.
- Jaeger and Apache SkyWalking can receive traces through the Zipkin v1 and v2 APIs.

## Checked

2026-11-04. Confirmed against the APISIX zipkin plugin page: endpoint, sample_ratio range, service_name, server_addr, span_version values, the performance note, the v1 and v2 span lists, set_ngx_var default and variable names with reload, Jaeger and SkyWalking compatibility. Nothing removed.

Method: documentation only; no commands were run.
