---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-foreach-dynamic-pipelines
name: grafana-alloy-foreach-dynamic-pipelines
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [foreach, template, collection, hash-string-id, enable-metrics, dynamic-pipelines, prometheusexporterredis]
level: advanced
status: docs-checked
description: "Run one component pipeline per list item with the experimental foreach block, for example one prometheus.exporter.redis per discovered target."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/reference/config-blocks/foreach.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# foreach: a pipeline per item

`foreach` is an experimental block that runs a separate pipeline for each item in a list.

```alloy
foreach "redis" {
  collection = discovery.relabel.redis.output
  var        = "each"
  template {
    prometheus.exporter.redis "default" {
      redis_addr = each["__address__"]
    }
    prometheus.scrape "default" {
      targets    = prometheus.exporter.redis.default.targets
      forward_to = [prometheus.relabel.default.receiver]
    }
    prometheus.relabel "default" {
      rule {
        replacement  = each["__meta_kubernetes_namespace"]
        target_label = "k8s_namespace"
        action       = "replace"
      }
      forward_to = [prometheus.remote_write.mimir.receiver]
    }
  }
}
```

## Arguments
- `collection` (list(any), required) and `var` (string, required: name of the current item).
- `id` (string): field of each item used to identify child components.
- `hash_string_id` (bool, default `false`): hash the id; recommended when ids are long strings, since ids appear in metrics, logs and the UI.
- `enable_metrics` (bool, default `false`): expose debug metrics; a large collection creates many series on `/metrics`.

## Scope rules
The `template` block (required) looks like a normal config; components inside it can use exports of components outside, but components outside cannot use exports of components inside the template. With `id = "name"` and `enable_metrics`, component paths look like `/foreach.pods/foreach_app-1_1/component.default`; if the item is not an object or lacks the field, the whole item is used.

Use it because `prometheus.exporter.*` components need one instance address while `discovery.*` returns a list of targets.

## Checked

2026-11-08. Read the foreach block reference page in full. Confirmed: experimental stability label, the five arguments with types and defaults, `hash_string_id` and `enable_metrics` guidance, the `template` block and its scope rules, the `id` component path example and fallback, and the redis exporter rationale and example.

Method: documentation only; no commands were run.
