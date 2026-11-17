---
id: computing-software.cloud-infrastructure-engineering.keda.fallback-replicas-on-scaler-failure
name: fallback-replicas-on-scaler-failure
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [fallback, failurethreshold, fallback-behavior, averagevalue, scaler-errors]
level: advanced
status: docs-checked
description: "Configure ScaledObject fallback so a failing scaler drives a safe replica count, with static, currentReplicas, currentReplicasIfHigher and currentReplicasIfLower behaviours."
sources:
  - https://keda.sh/docs/2.17/reference/scaledobject-spec/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Without `fallback`, a scaler that cannot read its source simply stops sending a metric to the HPA. The optional `spec.fallback` section changes that: KEDA counts consecutive failures per scaler, and once the count passes `failureThreshold` it returns a normalised metric of `target metric value * fallback replicas`. Because the HPA metric is an `AverageValue`, the HPA scales to that replica count. Both `failureThreshold` and `replicas` are mandatory when the section exists.

`fallback.behavior` chooses the replica number used:
- `static` (default): use `fallback.replicas`.
- `currentReplicas`: use the current replica count.
- `currentReplicasIfHigher`: current count if above `fallback.replicas`, else `fallback.replicas`.
- `currentReplicasIfLower`: current count if below `fallback.replicas`, else `fallback.replicas`.

Example from the page: Prometheus unreachable three times in a row with `replicas: 6` and `static` scales to 6.

Limits: only scalers whose metric target is `AverageValue` are supported, so CPU, memory and scalers using `Value` behave as if fallback were disabled. It works on ScaledObjects only, not ScaledJobs. Scaling modifier formulas do not alter metrics while fallback is in effect. The admission webhook rejects a fallback configured with a non-AverageValue metric type.

## Checked

2026-11-03. Confirmed on the 2.17 ScaledObject specification and admission webhook pages: failureThreshold, replicas, behavior values, AverageValue-only limit, ScaledObject-only, formula interaction.

Method: documentation only; no commands were run.
