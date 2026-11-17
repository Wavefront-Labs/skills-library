---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.container-rightsizing
name: container-rightsizing
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, workload-optimisation, container-rightsizing, kubernetes-requests, vertical-pod-autoscaler, goldilocks, resource-requests-limits]
level: practitioner
status: docs-checked
description: "Rightsize container CPU and memory requests from observed usage with VPA recommendations, Goldilocks or Kubecost, then shrink nodes so savings reach the bill."
sources: ["https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/", "https://github.com/kubernetes/autoscaler/tree/master/vertical-pod-autoscaler", "https://www.opencost.io/docs/", "https://kubernetes.io/docs/concepts/workloads/autoscaling/vertical-pod-autoscale/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container request rightsizing

## Why it matters
The scheduler places pods by their **requests**, not their usage. Inflated requests leave nodes mostly idle, and
savings only appear when nodes are removed.

## Steps
1. Measure usage per container over a representative period (include peaks and month-end jobs): CPU and memory
   percentiles from your metrics system.
2. Get recommendations: the Vertical Pod Autoscaler (VPA) recommender, which the Kubernetes docs describe as adjusting
   requests to match actual usage, or a cost tool such as OpenCost.
3. Set requests from observed usage with headroom, memory more conservatively than CPU. The Kubernetes docs explain why:
   CPU limits are enforced by throttling, while a container that exceeds its memory limit may be OOM-killed.
4. Roll out gradually via GitOps; watch OOMKills, CPU throttling and latency.
5. **Bin-pack**: use cluster autoscaler or Karpenter consolidation to remove freed nodes; check
   PodDisruptionBudgets allow it.
6. Repeat on a schedule, or let VPA apply changes for suitable workloads. Kubernetes also supports in-place Pod resize
   through the Pod `/resize` subresource and `resizePolicy`.

## Gotchas
- VPA must be installed separately; it is a CRD, not part of the core API.
- Rightsizing pods without node consolidation saves nothing.

## Verify
- [ ] Cluster request-to-allocatable ratio and node count reduced; no SLO regression.

## Checked
2026-11-01. Confirmed in the Kubernetes resource management page (requests, CPU throttling, memory OOM kills, in-place
resize via /resize and resizePolicy), the Kubernetes VPA page (adjusts requests to usage, separate install, CRD) and the
VPA README. Removed: percentile targets, Goldilocks and Kubecost claims, GKE recommendations, Autopilot/Fargate
billing claim, VPA/HPA conflict claim, Java heap flag and the `updateMode` value.
Method: documentation only; no commands were run.
