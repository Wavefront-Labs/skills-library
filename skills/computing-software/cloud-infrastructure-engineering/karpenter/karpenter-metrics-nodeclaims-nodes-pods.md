---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-metrics-nodeclaims-nodes-pods
name: karpenter-metrics-nodeclaims-nodes-pods
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [metrics, nodeclaims, nodes, pods, startup-duration, allocatable]
level: practitioner
status: docs-checked
description: "Karpenter nodeclaim, node and pod metrics: creation and termination counters, allocatable and request totals, pod startup and bound durations, eviction counters."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/reference/metrics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Karpenter nodeclaim, node and pod metrics

Nodeclaims:
- `karpenter_nodeclaims_created_total` (STABLE): labelled by creation reason, owning nodepool, and whether minValues was relaxed.
- `karpenter_nodeclaims_terminated_total`, `karpenter_nodeclaims_disrupted_total`, `karpenter_nodeclaims_unhealthy_disrupted_total` (unhealthy nodeclaims disrupted, labelled by node condition, nodepool and image ID).
- `karpenter_nodeclaims_termination_duration_seconds` and `karpenter_nodeclaims_instance_termination_duration_seconds` (the cloud instance part).

Nodes:
- `karpenter_nodes_allocatable` (BETA), `karpenter_nodes_system_overhead`.
- `karpenter_nodes_total_pod_requests`, `_total_pod_limits`, `_total_daemon_requests`, `_total_daemon_limits`: per-node resource totals, including DaemonSet pods.
- `karpenter_nodes_created_total`, `_terminated_total`, `_drained_total`, `_lifetime_duration_seconds`, `_current_lifetime_seconds`, `_termination_duration_seconds`.

Pods:
- `karpenter_pods_startup_duration_seconds` (STABLE): pod creation until running.
- `karpenter_pods_state`, `_bound_duration_seconds`, `_unbound_time_seconds`, `_unstarted_time_seconds`.
- `karpenter_pods_scheduling_decision_duration_seconds`, and the `karpenter_pods_provisioning_*` variants, which time from when Karpenter first thinks the pod can schedule (a point in memory, not the pod creation timestamp).
- `karpenter_pods_eviction_requests_total` and `karpenter_pods_drained_total` for drain progress.

## Checked

2026-11-04. Confirmed against the Metrics reference (v1.13) (identifiers, defaults, limits and prose). Removed the unconfirmed alert advice and PromQL examples; corrected what the provisioning_* metrics measure.

Method: documentation only; no commands were run.
