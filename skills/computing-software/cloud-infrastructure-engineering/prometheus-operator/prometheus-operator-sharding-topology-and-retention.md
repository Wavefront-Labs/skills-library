---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-sharding-topology-and-retention
name: prometheus-operator-sharding-topology-and-retention
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [topology-sharding, shard-retention-policy, zone-aware, whenscaled-retain, feature-gate-sharding]
level: advanced
status: docs-checked
description: "Use beta zone-aware (topology) sharding and the shard retention policy that keeps scaled-down shards queryable until retention expires."
sources: ["https://prometheus-operator.dev/docs/platform/sharding/", "https://prometheus-operator.dev/docs/platform/operator/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
## Topology-aware sharding (beta)
Requires the `PrometheusTopologySharding` feature gate on the operator. In multi-zone clusters, address-based sharding ignores zones and causes costly cross-zone traffic. With `spec.shardingStrategy.mode: Topology` the operator:
- adds relabeling so each shard keeps only targets from its zone;
- adds a `nodeSelector` scheduling the shard pods in that zone;
- adds a `zone` external label (name configurable by `externalLabelName`).

Provide `topology.values` (for example `europe-west4-a` and `europe-west4-b`). `spec.shards` must be at least the number of values; a multiple spreads evenly. With 4 shards over 2 zones, shards 0 and 2 go to the first zone and 1 and 3 to the second.

Note: the operator CLI reference lists both `PrometheusTopologySharding` and `PrometheusShardRetentionPolicy` as enabled by default, controlled with `--feature-gates`; check the gate state for the version you run.

## Shard retention policy (beta)
Requires the `PrometheusShardRetentionPolicy` gate. By default scaling down deletes the removed shards' pods and access to their history. Set `spec.shardRetentionPolicy.whenScaled: Retain` to keep them running, still queryable via Thanos sidecar and querier. The operator deletes them when the Prometheus retention time elapses; override with `shardRetentionPolicy.retain.retentionPeriod: 7d`.

Gotcha: if the resource uses size-based retention only (no retention time), retained shards are kept forever by default.

## Checked

2026-11-08. Read the sharding page in full and the operator CLI reference page in full. Added a note that the CLI reference lists both feature gates as enabled by default.

Method: documentation only; no commands were run.
