---
id: computing-software.cloud-infrastructure-engineering.keda.trigger-fields-and-metric-types
name: trigger-fields-and-metric-types
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [triggers, metrictype, averagevalue, utilization, trigger-name, authenticationref]
level: practitioner
status: docs-checked
description: "Read the fields every KEDA trigger accepts and decide between AverageValue, Value and Utilization metric types with the worked queue examples."
sources:
  - https://keda.sh/docs/2.17/reference/scaledobject-spec/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each entry in `spec.triggers` has these fields:
- `type` (mandatory): the scaler, for example `kafka` or `prometheus`.
- `metadata` (mandatory): the scaler's own parameters.
- `name` (optional): defaults to a name generated from the type; used to tell metrics apart in Prometheus output and required for any trigger referenced in a scaling-modifier formula. Duplicate names are rejected by the admission webhook.
- `useCachedMetrics` (default `false`).
- `authenticationRef`: reference to a `TriggerAuthentication` or `ClusterTriggerAuthentication`.
- `metricType`: `AverageValue` (default), `Value` or `Utilization`.

Metric type semantics from the page, using a deployment with 3 running replicas and a queue:
- `AverageValue` divides the metric across replicas. Queue of 20 with threshold 5 gives 20 / 5 = 4 replicas regardless of the current count.
- `Value` does not average. For an average queue wait of 20 ms with threshold 5 ms, the HPA computes 3 * 20 / 5 = 12 replicas.

All scalers except CPU and memory support `AverageValue` and `Value`; CPU and memory support `AverageValue` and `Utilization`.

## Checked

2026-11-03. Confirmed on the 2.17 ScaledObject specification: trigger fields, metricType values, the 20/5 and 3*20/5 examples, scaler support.

Method: documentation only; no commands were run.
