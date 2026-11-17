---
id: computing-software.cloud-infrastructure-engineering.vector.log-to-metric-transform
name: log-to-metric-transform
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [log-to-metric, transform, counter, gauge, metrics, tags, vector]
level: practitioner
status: docs-checked
description: "Turn log events into metric events with log_to_metric and know that it does not aggregate."
sources:
  - https://vector.dev/docs/reference/configuration/transforms/log_to_metric/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`log_to_metric` converts log events into metric events. It is stateless. Each entry in `metrics` names a source `field` and a `type` (counter, gauge, histogram, set or summary), plus optional naming and tags.

```yaml
transforms:
  request_counter:
    type: log_to_metric
    inputs: [parsed]
    metrics:
      - type: counter
        field: status
        name: http_requests_total
        namespace: app
        tags:
          status: "{{ status }}"
```

Options per metric: `field` (required, templatable), `name` (overrides the field name), `namespace`, `kind` (`incremental` by default, or `absolute`), `tags` (keys and values templatable), and for counters `increment_by_value: true` to add the field's value instead of 1. A top-level `all_metrics` flag changes the behaviour: `metrics` is ignored and all incoming events are processed and converted when possible.

Behaviour to remember:

- One log can produce several metrics; they are emitted individually and downstream components do not know they came from one log.
- A null target field is ignored and no metric is emitted.
- The transform does not reduce many logs to one metric. Reduction happens at the destination: the `prometheus_exporter` sink reduces for the next scrape, while other sinks forward individual metrics for the backend to reduce. Use `aggregate` to cut volume earlier.

Keep tag values low cardinality.

Verify with the console sink and JSON encoding.

## Checked

2026-11-03. Read transforms/log_to_metric. Confirmed: stateless, per-metric options (`field`, `name`, `namespace`, `kind` default incremental, `tags` templating, `increment_by_value`), `all_metrics`, one log yielding multiple metrics, null target ignored, and the prometheus_exporter reduction note. Reworded: the `all_metrics` description to match the page.

Method: documentation only; no commands were run.
