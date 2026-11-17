---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-metrics-endpoint-and-stability
name: karpenter-metrics-endpoint-and-stability
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [metrics, prometheus, stability, observability, metrics-port]
level: practitioner
status: docs-checked
description: "Where Karpenter exposes Prometheus metrics, the STABLE/BETA/ALPHA stability levels, and the metric families (karpenter_, operator_, controller_runtime_, workqueue_, aws_sdk_go_)."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/reference/metrics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Karpenter metrics endpoint and stability levels

Karpenter publishes Prometheus-format metrics by default at `karpenter.kube-system.svc.cluster.local:8080/metrics`. The port is set with the `METRICS_PORT` environment variable (see the settings reference).

Each metric in the reference carries a stability level:
- STABLE (for example `karpenter_nodeclaims_created_total`, `karpenter_pods_startup_duration_seconds`, `karpenter_voluntary_disruption_decisions_total`, `karpenter_scheduler_scheduling_duration_seconds`, the `karpenter_interruption_*` and `karpenter_cluster_state_*` metrics, `controller_runtime_*`, `workqueue_*`, `aws_sdk_go_request_*`).
- BETA: for example `karpenter_nodes_allocatable`, `karpenter_scheduler_queue_depth`, `karpenter_voluntary_disruption_eligible_nodes`, `karpenter_cloudprovider_*` instance type metrics.
- ALPHA, for example all `karpenter_nodepools_*` metrics and `karpenter_cluster_utilization_percent`.
- DEPRECATED: the unprefixed `operator_termination_*` and `operator_status_condition_*` metrics; use the per-kind variants below.

Metric families by prefix:
- `karpenter_nodeclaims_*`, `karpenter_nodes_*`, `karpenter_pods_*`: object lifecycle and resource totals.
- `karpenter_voluntary_disruption_*`, `karpenter_scheduler_*`, `karpenter_interruption_*`: behaviour of the controllers.
- `operator_<kind>_status_condition_*` and `operator_<kind>_termination_*`: generated for nodeclaim, node, nodepool and ec2nodeclass (transitions_total, transition_seconds, current_status_seconds, count).
- `controller_runtime_*`, `workqueue_*`, `client_go_request_*`, `aws_sdk_go_request_*`, `leader_election_*`: framework and AWS SDK health.

## Checked

2026-11-04. Confirmed against the Metrics reference (v1.13) (identifiers, defaults, limits and prose). Removed unconfirmed meanings of STABLE/ALPHA and the scrape advice; added the DEPRECATED operator_* metrics.

Method: documentation only; no commands were run.
