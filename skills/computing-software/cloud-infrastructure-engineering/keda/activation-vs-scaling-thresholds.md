---
id: computing-software.cloud-infrastructure-engineering.keda.activation-vs-scaling-thresholds
name: activation-vs-scaling-thresholds
category: computing-software
field: cloud-infrastructure-engineering
product: keda
tags: [activation, activationthreshold, scale-from-zero, activation-phase, scaling-phase, hpa]
level: practitioner
status: docs-checked
description: "Separate KEDA's activation phase (0 to 1) from the HPA scaling phase (1 to N), and use activation parameters that must be strictly exceeded."
sources:
  - https://keda.sh/docs/2.17/concepts/scaling-deployments/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
KEDA autoscaling has two phases.

Activation phase: the KEDA operator decides whether to scale from or to zero using the scaler's `IsActive` result. It applies only to 0 to 1 and 1 to 0. This matters for sources whose idle value is not 0, for example Prometheus queries ranging from -X to X.

Scaling phase: once KEDA has scaled to 1 instance, the HPA controller decides 1 to N using the generated HPA and the metrics KEDA exposes through its metrics server.

Each scaler defines a scaling parameter and, optionally, an activation twin named with an `activation` prefix: `threshold` scales, `activationThreshold` activates. Rules from the page:
- Activation values are optional and default to 0.
- Activation requires the metric to be strictly greater than the value. `activationThreshold: 0` activates only at 1 or more.
- Activation wins over scaling. With `threshold: 10` and `activationThreshold: 50`, 40 messages leave the scaler inactive and the workload at zero even though the HPA would want 4 instances.
- If `minReplicaCount` is 1 or more, the scaler is always active and the activation value is ignored.
- A scaler with no `activation*` property does not support custom activation; its value is always 0.

## Checked

2026-11-03. Confirmed on the KEDA 2.17 Scaling Deployments page: activation vs scaling phases, strictly-greater rule, activation priority, minReplicaCount of 1 or more, scalers without an activation property.

Method: documentation only; no commands were run.
