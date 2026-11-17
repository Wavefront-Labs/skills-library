---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-metrics-nodepools-interruption-cluster
name: karpenter-metrics-nodepools-interruption-cluster
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [metrics, nodepool, cost, limits, interruption, cluster-state, cloudprovider]
level: practitioner
status: docs-checked
description: "Karpenter NodePool usage, limit, allowed_disruptions and cost metrics, interruption queue metrics, cluster state and cloudprovider instance-type metrics."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/reference/metrics.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# NodePool, interruption, cluster and cloudprovider metrics

NodePool (all ALPHA):
- `karpenter_nodepools_usage`: resources provisioned, labelled by nodepool and resource type.
- `karpenter_nodepools_limit`: limits specified on the nodepool that restrict the quantity of resources provisioned, labelled by nodepool and resource type.
- `karpenter_nodepools_allowed_disruptions`: nodes that may disrupt concurrently under budgets; it changes rapidly as nodes come and go.
- `karpenter_nodepools_nodes_consuming_budgets`: nodes counted against the budget.
- `karpenter_nodepools_cost_total`: cost from Karpenter's perspective, units set by the cloud provider, includes NodeOverlay changes, not authoritative for billing.
- `karpenter_nodepools_cost_tracker_errors_total`.

Interruption (STABLE):
- `karpenter_interruption_received_messages_total`
- `karpenter_interruption_deleted_messages_total`
- `karpenter_interruption_message_queue_duration_seconds`
- `karpenter_interruption_instance_status_unhealthy_total`

Received messages are broken down by message type and whether the message was actionable; the queue-duration metric is the time a message waits on the queue before Karpenter processes it; the unhealthy-status metric counts unique unhealthy instance statuses from EC2 DescribeInstanceStatus by status check category.

Cluster state (STABLE): `karpenter_cluster_state_synced` is 1 when nodeclaims and nodes in the API server match Karpenter's cluster state, else 0; plus `karpenter_cluster_state_node_count` and `karpenter_cluster_state_unsynced_time_seconds`. `karpenter_cluster_utilization_percent` (ALPHA) is utilization of allocatable resources by pod requests.

Cloudprovider (BETA): `karpenter_cloudprovider_instance_type_cpu_cores`, `_memory_bytes`, `_offering_available`, `_offering_price_estimate` (estimated hourly price by instance type, capacity type and zone), plus `karpenter_cloudprovider_errors_total`, `karpenter_cloudprovider_duration_seconds` and the `karpenter_cloudprovider_batcher_batch_size` / `_batch_time_seconds` pair (request batch size and batching window per batcher).

## Checked

2026-11-08. Confirmed against the Metrics reference (v1.13) (names, stability levels, descriptions). Removed the unsupported "alert near 1" advice, the claim that missing deletes mean missing `sqs:DeleteMessage`, and the claim that an unsynced cluster blocks provisioning; added what the page says about each metric.

Method: documentation only; no commands were run.

