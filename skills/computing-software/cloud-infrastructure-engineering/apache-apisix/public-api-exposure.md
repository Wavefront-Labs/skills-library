---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.public-api-exposure
name: public-api-exposure
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, public-api, internal-endpoint, metrics, batch-requests, plugin]
level: practitioner
status: docs-checked
description: "Expose an APISIX internal endpoint on a public route with public-api: the uri attribute, the Prometheus metrics example and the CPU caveat."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/public-api.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# public-api exposure

Single attribute: `uri` (optional). It is the internal endpoint to expose; if unset, the route's own URI is exposed. The route's `uri` is the public path.

Expose Prometheus metrics at `/prometheus_metrics`:

```json
{
  "id": "prometheus-metrics",
  "uri": "/prometheus_metrics",
  "plugins": {
    "public-api": { "uri": "/apisix/prometheus/metrics" }
  }
}
```

Notes:
- For this use, disable the default export server with `plugin_attr.prometheus.enable_export_server: false` in `conf/config.yaml`.
- Serving metrics this way bypasses the privileged agent optimization, so heavy metric collection can use significant CPU and slow regular requests.
- To expose the batch-requests endpoint, set the plugin `uri` to `/apisix/batch-requests`.

## Checked

2026-11-04: read the public-api plugin page; the uri attribute, the prometheus_metrics route, enable_export_server false, the privileged-agent CPU caveat and the batch-requests example match. Nothing removed.

Method: documentation only; no commands were run.
