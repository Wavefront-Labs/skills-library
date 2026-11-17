---
id: computing-software.cloud-infrastructure-engineering.opentelemetry-operator.opentelemetry-operator-collector-autoscaling-pdb
name: opentelemetry-operator-collector-autoscaling-pdb
category: computing-software
field: cloud-infrastructure-engineering
product: opentelemetry-operator
tags: [opentelemetry-operator, autoscaler, hpa, poddisruptionbudget, maxreplicas, replicas]
level: practitioner
status: docs-checked
description: "Configure HorizontalPodAutoscaler behaviour and PodDisruptionBudget for a Collector through spec.autoscaler and spec.podDisruptionBudget, and avoid mixing with replicas."
sources: ["https://github.com/open-telemetry/opentelemetry-operator/blob/main/docs/api/opentelemetrycollectors.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Autoscaler and PodDisruptionBudget fields

Replicas. `spec.replicas` (default 1) sets pod count when you are not autoscaling.

Autoscaler. `spec.autoscaler` configures the HPA for the workload. Fields from the v1beta1 reference:
- `maxReplicas`: upper bound. Setting it is what enables autoscaling.
- `minReplicas`: lower bound, at least 1; set it when you use autoscaling.
- `targetCPUUtilization`: average CPU across replicas that triggers scale-up; defaults to 90 percent.
- `targetMemoryUtilization`: average memory utilization target.
- `metrics`: custom HPA metrics; currently the only supported custom metric type is Pod. Use the two target fields for plain CPU or memory scaling.
- `behavior`: HorizontalPodAutoscalerBehavior with `scaleUp` and `scaleDown` policies.

PodDisruptionBudget. `spec.podDisruptionBudget` takes `minAvailable` or `maxUnavailable` (int or percentage string), mutually exclusive (the reference says `maxUnavailable` is mutually exclusive with `minAvailable`). If unspecified the Collector gets a PDB with `maxUnavailable` of one by default. The Target Allocator embedded spec has its own `podDisruptionBudget`, also defaulting to a maxUnavailable of one for a valid allocation strategy.

## Checked

2026-11-04. Confirmed in the generated OpenTelemetryCollector API reference (docs/api/opentelemetrycollectors.md, read as raw Markdown because the GitHub page view is a stub): `spec.replicas` default 1, the `spec.autoscaler` fields (`behavior`, `maxReplicas` enabling autoscaling, `metrics` with only type Pod supported, `minReplicas` at least 1, `targetCPUUtilization` default 90 percent, `targetMemoryUtilization`), the default PDB with a maxUnavailable of one for the Collector and for the Target Allocator (for a valid allocation strategy), and `minAvailable` and `maxUnavailable` as int or string. Removed the unconfirmed 'minimum 1' for `maxReplicas` (only `minReplicas` has that statement).

Method: documentation only; no commands were run.
