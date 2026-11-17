---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.opentelemetry-tracing
name: opentelemetry-tracing
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, opentelemetry, otel, tracing, sampler, collector, plugin-metadata]
level: advanced
status: docs-checked
description: "Export APISIX traces with opentelemetry: sampler names and fraction, additional_attributes, and collector, resource and batch_span_processor plugin metadata."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/opentelemetry.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenTelemetry tracing

The plugin is disabled by default: add `opentelemetry` under `plugins` in `config.yaml`. Optionally set `apisix.tracing: true` for tracing across the whole request lifecycle, which adds overhead.

Route attributes:
- `sampler.name`: `always_off` (default), `always_on`, `trace_id_ratio`, `parent_base`.
- `sampler.options.fraction`: 0 to 1 (default 0).
- `sampler.options.root`: `name` (`always_on`, `always_off`, `trace_id_ratio`) and `options.fraction`, used with `parent_base`.
- `additional_attributes` and `additional_header_prefix_attributes`: arrays of strings.

Collector settings go in plugin metadata, PUT to `apisix/admin/plugin_metadata/opentelemetry`:

```json
{
  "trace_id_source": "x-request-id",
  "resource": { "service.name": "APISIX" },
  "collector": {
    "address": "127.0.0.1:4318",
    "request_timeout": 3,
    "request_headers": { "Authorization": "<TOKEN>" }
  },
  "batch_span_processor": {
    "drop_on_queue_full": false,
    "max_queue_size": 1024,
    "batch_timeout": 2,
    "inactive_timeout": 1,
    "max_export_batch_size": 16
  },
  "set_ngx_var": false
}
```

The default sampler is `always_off`, so choose another sampler on the route or nothing is traced.

## Checked

2026-11-04. Confirmed against the APISIX opentelemetry plugin page: sampler names, fraction and root options, additional_attributes, the plugin metadata endpoint and its example values, the plugin being disabled by default. Corrected the prerequisite line: apisix.tracing is an optional switch for lifecycle-wide tracing, not a requirement.

Method: documentation only; no commands were run.
