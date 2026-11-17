---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-operator-sharding
name: prometheus-operator-sharding
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus-operator, operator-sharding, prometheus-shards, hashmod, horizontal-scaling, thanos-query]
level: advanced
status: docs-checked
description: "Scale scraping horizontally with Prometheus CR spec.shards: default hash sharding, custom __tmp_hash, scraping a target on all shards, topology sharding, retention and querying."
sources: ["https://prometheus-operator.dev/docs/platform/sharding/", "https://prometheus-operator.dev/docs/api-reference/api/#monitoring.coreos.com/v1.PrometheusSpec"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sharding Prometheus with the operator

The operator creates `.spec.shards` StatefulSets multiplied by `.spec.replicas` pods. Use it when vertical scaling is
exhausted and scraped targets need distributing across several Prometheus shards.

## Default distribution
By default shards use the Prometheus modulus (hash) configuration, hashing the `__address__` label for ServiceMonitor and
PodMonitor resources and the `__param_target__` label for Probe resources. Each target is assigned to exactly one shard.
In the docs' worked example, raising a two-replica Prometheus to `shards: 2` adds pods named
`prometheus-prometheus-shard-1-0` and `prometheus-prometheus-shard-1-1` next to `prometheus-prometheus-0` and `-1`.

```yaml
spec:
  shards: 2
  replicas: 2        # per shard
```

## Customising distribution
- Custom target distribution: set the `__tmp_hash` label during discovery with relabeling; the operator uses its value
  instead of the default labels. The page's example shards by pod namespace and name:
  `sourceLabels: [__meta_kubernetes_pod_namespace, __meta_kubernetes_pod_name]`, `separator: /`, `targetLabel: __tmp_hash`.
  It can also be applied at the scrape class level.
- Scrape a target from every shard (for singletons such as kube-state-metrics): set `__tmp_disable_sharding` to a
  non-empty value with relabeling (`targetLabel: __tmp_disable_sharding`, `replacement: "true"`).
- Topology-aware sharding (beta; needs the `PrometheusTopologySharding` feature gate on the operator):
  `shardingStrategy.mode: Topology` with `topology.values` listing zones pins each shard to a zone via relabeling, a
  `nodeSelector` and a zone external label (name configurable via `externalLabelName`). The shard count must be at least
  the number of topology values; with 4 shards and 2 zones, shards 0 and 2 go to the first zone and 1 and 3 to the second.

## Querying and rules
No single shard holds all data. The docs say to query globally with a Thanos querier connected to all Thanos sidecars,
to use the Thanos ruler to evaluate rules across shards, or to remote write the samples to a central location.

## Scaling limitations
- Scaling the shard count down does not reshard existing data onto the remaining instances; it must be moved manually.
- Scaling up does not reshard existing data either; it stays available from the same instances.
- Retaining scaled-down shards (beta; needs the `PrometheusShardRetentionPolicy` feature gate): by default pods of removed
  shards are deleted along with access to their history. Setting `.spec.shardRetentionPolicy.whenScaled: Retain` keeps
  them running and queryable through Thanos sidecar and querier until the Prometheus retention time passes (override with
  `retain.retentionPeriod`). With size-based retention only, retained shards are kept forever by default.

## Verify
- [ ] After enabling shards, `kubectl get pods` shows the expected `shard-N` pods and each shard scrapes only part of the
      targets (check each shard's targets page).
- [ ] Global queries go through Thanos Query or the central remote-write store, not a single shard.

## Checked

Checked 2026-11-08 against the Prometheus Operator sharding page (the API reference was used for field names only).
Removed because the pages do not state them: the injected `hashmod` relabel snippet and modulus detail, `prometheus_replica`
external label behaviour, every-shard-evaluates-all-rules and per-shard alert advice, the ~10-15M series sizing rule, the
functional-sharding alternative, and the PromQL verification expressions.
Method: docs-only read of cited pages, 2026-11-08
