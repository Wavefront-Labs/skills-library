---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-collector.metricstransform-processor
name: metricstransform-processor
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-collector
tags: [opentelemetry-collector, processors, metricstransform, rename, labels, aggregate]
level: advanced
status: docs-checked
description: "Rename metrics, add labels and aggregate away dimensions with the metricstransform processor."
sources:
  - https://github.com/open-telemetry/opentelemetry-collector-contrib/blob/main/processor/metricstransformprocessor/README.md
  - https://opentelemetry.io/docs/collector/transforming-telemetry/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The metrics transform processor renames metrics, adds, renames or deletes label keys and values, scales values and aggregates across labels.

```yaml
processors:
  metricstransform/rename:
    transforms:
      - include: system.cpu.usage
        action: update
        new_name: system.cpu.usage_time
  metricstransform/clustername:
    transforms:
      - include: ^.*$
        match_type: regexp
        action: update
        operations:
          - action: update_label
            label: cluster_name
            new_label: cluster-name
```

Details from the README:

- `match_type` is `strict` (default) or `regexp`.
- `action` is `update` (in place), `insert` (apply operations to a copy) or `combine`, which merges all matching metrics into one new metric and removes the originals. `insert` and `combine` require `new_name`; `combine` requires `aggregation_type`.
- Operations include `add_label`, `update_label`, `delete_label_value`, `toggle_scalar_data_type`, `experimental_scale_value`, `aggregate_labels` and `aggregate_label_values`; aggregation types are sum, mean, min, max, count and median.
- Transforms apply in order, so later ones see earlier results.
- Aggregation works only within one batch of metrics, never across batches, so it is not suitable for combining multiple nodes or clients.
- Only the `sum` aggregation type is supported for histogram and exponential histogram data.
- The README's own sample block spells the key `metrics_transform`, but the transforming-telemetry page uses `metricstransform/<name>` as in the examples above.

## Checked

Method: docs-checked 2026-11-09 against the metricstransform processor README (read in full) and the transforming-telemetry page (renaming section).
