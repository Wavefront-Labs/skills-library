---
id: computing-software.ai-ml-engineering.seldon-core-2.autoscaling-approaches-overview
name: autoscaling-approaches-overview
category: computing-software
field: ai-ml-engineering
product: seldon-core-2
tags: [seldon-core-2, autoscaling, inference-lag, hpa, multi-model-serving, scaling-strategy]
level: practitioner
status: docs-checked
description: "Choose a Seldon Core 2 autoscaling approach: native inference-lag scaling, Model HPA with custom metrics, or Model plus Server HPA for one-to-one serving."
sources: ["https://github.com/SeldonIO/seldon-core/blob/v2/docs-gb/scaling/README.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Choosing an autoscaling approach

Models and Servers are separate in Core 2, and Servers can host many Models, so scale both in a coordinated way. First choose a Model metric, then Server scaling.

## Step 1: Model metric
- Inference lag, native: the difference between incoming and outgoing requests in a period. Configure `minReplicas` or `maxReplicas` on the Model and install with helm value `autoscaling.autoscalingModelEnabled` set to true.
- Custom or Kubernetes-native metrics with a `HorizontalPodAutoscaler`: you expose metrics (for example with Prometheus) and target them.

## Step 2: Server scaling
- Native, managed by the scheduler: set `minReplicas` and `maxReplicas` on the Server and keep helm value `autoscaling.autoscalingServerEnabled` at its default true.
- HPA on Servers, only when Models and Servers map one to one (no multi-model serving), using an HPA that matches the one on the Model. This works with custom metrics only.

## Summary
| Approach | Metric | Multi-model serving | Main drawback |
|---|---|---|---|
| Seldon Core autoscaling | inference lag | yes | model scale down only when no traffic to that model |
| Model autoscaling with HPA | user defined | yes | needs a metrics store; possibly suboptimal server packing on scale down |
| Model and Server HPA | user defined | no | needs a metrics store; no multi-model serving |

Core services such as gateways and the dataflow engine scale separately; see the core services scaling skill.

## Checked
Method: docs-checked 2026-11-09 against docs-gb/scaling/README.md (read in full).
