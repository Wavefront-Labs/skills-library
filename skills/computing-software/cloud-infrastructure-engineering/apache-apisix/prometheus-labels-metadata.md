---
id: computing-software.cloud-infrastructure-engineering.apache-apisix.prometheus-labels-metadata
name: prometheus-labels-metadata
category: computing-software
field: cloud-infrastructure-engineering
product: apache-apisix
tags: [apache-apisix, apisix, prometheus, extra-labels, disabled-labels, cardinality, plugin-metadata]
level: advanced
status: docs-checked
description: "Tune APISIX Prometheus label cardinality: add extra_labels in plugin_attr and collapse labels with disabled_labels plugin metadata at runtime."
sources:
  - https://raw.githubusercontent.com/apache/apisix/master/docs/en/latest/plugins/prometheus.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prometheus labels and metadata

Add labels in `conf/config.yaml`:

```yaml
plugin_attr:
  prometheus:
    metrics:
      http_status:
        extra_labels:
          - upstream_addr: $upstream_addr
          - route_name: $route_name
```

- Supported on `http_status`, `http_latency`, `bandwidth`, the `llm_*` metrics and the `ai_cache_*` metrics.
- An undefined variable produces an empty label value.
- Reload APISIX for `extra_labels` changes to take effect.

Reduce cardinality at runtime, with no restart, through plugin metadata:

```shell
curl "http://127.0.0.1:9180/apisix/admin/plugin_metadata/prometheus" -X PUT \
  -H "X-API-KEY: ${admin_key}" \
  -d '{"disabled_labels": {"http_status": ["node", "consumer"], "http_latency": ["node"]}}'
```

Listed labels are collapsed to an empty string. They stay in the schema, so dashboards and alerts keep working.

Structural labels cannot be disabled: `code` on `http_status`; `type` on `http_latency`, `bandwidth` and `llm_latency`; `layer` on `ai_cache_hits_total`.

## Checked

2026-11-04: read the prometheus plugin page; extra_labels config and the list of supported metrics, the empty-value rule for undefined variables, the disabled_labels plugin-metadata example, the collapse-to-empty-string behaviour and the structural labels all match. Added the reload requirement from the page.

Method: documentation only; no commands were run.
