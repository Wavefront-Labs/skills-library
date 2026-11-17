---
id: computing-software.cloud-infrastructure-engineering.observability.groupbyattrs-processor
name: groupbyattrs-processor
category: computing-software
field: cloud-infrastructure-engineering
product: observability
tags: [groupbyattrs-processor, resourcedetection-processor, transforming-telemetry, resource-attributes, otel-collector]
level: advanced
status: docs-checked
description: "Use the groupbyattrs processor to promote record attributes to resource attributes and regroup batches, and order it correctly with resourcedetection and k8sattributes."
sources: ["https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/groupbyattrsprocessor", "https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/processor/resourcedetectionprocessor"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# groupbyattrs processor (with resourcedetection)

## What it does
Moves listed record-level attributes (span/log/datapoint) up to the **Resource** and regroups records so each
distinct resource holds its records. Without keys it only compacts batches (merges records sharing an identical
resource).

```yaml
processors:
  groupbyattrs/host:
    keys: [host.name, k8s.pod.name]
  groupbyattrs/compact: {}
```

## When you need it
- Extracting resources from flat data formats such as Fluent Bit logs or Prometheus metrics, or associating Prometheus
  metrics with a Resource that describes the host, based on a label present on all metrics.
- Optimising data packaging by extracting common attributes.
- Compacting records that share the same Resource and scope but sit under several ResourceSpans/ResourceMetrics/
  ResourceLogs (use an empty key list). The README recommends running it together with `batch` as a consecutive step.

## Ordering in a pipeline
```yaml
processors: [memory_limiter, groupbyattrs/host, k8sattributes, resourcedetection, transform, batch, groupbyattrs/compact]
```
- `resourcedetection` adds the collector's environment (cloud, host); with `override: false` it does not replace
  attributes already on the telemetry.
- Compaction after `batch` merges duplicate Resource objects left by fragmented input.

## Gotchas
- The grouping attributes are removed from the records and set on the new Resource, which also inherits the original
  Resource attributes; check that downstream queries look for the key at resource level.
- Records that have none of the listed keys stay on their original Resource.
- Metrics of different data types (for example GAUGE and SUM with the same name) are not merged into one Metric.

## Verify
`debug` exporter detailed: the key now appears on the Resource and no longer on the records;
`otelcol_processor_groupbyattrs_num_grouped_spans`, `..._num_grouped_logs` and `..._num_grouped_metrics` increase.

## Checked

2026-10-24. groupbyattrs processor README and documentation.md, and resourcedetection processor README (main branch). Confirmed: stability beta, regrouping and removal of keys from records, inheritance of Resource attributes, compaction with an empty key list, the recommendation to follow with `batch`, the internal metric names, and `override` on resourcedetection. Removed unconfirmed claims about Loki labels, `target_info` and k8sattributes input.

Method: documentation only; no commands were run.
