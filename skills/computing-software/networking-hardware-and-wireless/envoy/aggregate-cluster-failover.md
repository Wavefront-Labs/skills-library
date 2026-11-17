---
id: computing-software.networking-hardware-and-wireless.envoy.aggregate-cluster-failover
name: aggregate-cluster-failover
category: computing-software
field: networking-hardware-and-wireless
product: envoy
tags: [networking-hardware-and-wireless, envoy, aggregate-cluster, cluster-failover, linearize-priority-set, cluster-fallback, priority]
level: practitioner
status: docs-checked
description: "Fail over between Envoy clusters with different types or LB policies using an aggregate cluster and its linearised priority set."
sources:
  - https://github.com/envoyproxy/envoy/blob/main/docs/root/intro/arch_overview/upstream/aggregate_cluster.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# aggregate cluster failover
An aggregate cluster lets Envoy fail over between clusters that differ in configuration: EDS to STRICT_DNS, ROUND_ROBIN to MAGLEV, or a `0.1s` connect timeout to `1s`. It references other clusters by name in its `clusters` list, and the list order defines fallback priority.

Load balancing is two-tier: the aggregate's top-level balancer picks the cluster and priority, then the chosen cluster's own balancer picks the host. Internally the top level linearises all priority sets across referenced clusters into one list, so existing priority and health logic is reused. Example from the docs: primary with 3 priorities, secondary and tertiary with 2 each give the order Primary P0..P2, Secondary, Tertiary.

```yaml
clusters:
- name: aggregate_cluster
  connect_timeout: 0.25s
  lb_policy: CLUSTER_PROVIDED
  cluster_type:
    name: envoy.clusters.aggregate
    typed_config:
      "@type": type.googleapis.com/envoy.extensions.clusters.aggregate.v3.ClusterConfig
      clusters: [primary, secondary]
```
Gotchas from the docs: PriorityLoad retry plugins (`retry_priority`) do not work with an aggregate cluster, and Stateful Sessions are incompatible with it. Circuit breaking is handled by the underlying clusters, not the aggregate; the only aggregate-level breaker is `max_retries`. Top-tier traffic is split by each cluster's health score across all its priorities, using the 1.4 default overprovisioning factor.

## Checked
2026-11-03. Confirmed against aggregate_cluster.rst, including the ClusterConfig example and the retry, stateful session and circuit breaker notes. Removed or corrected: the unsupported 'confirm' note, the health/panic claim and the failover verify step.
Method: documentation only; no commands were run.
