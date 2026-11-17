---
id: computing-software.cloud-infrastructure-engineering.prometheus-operator.prometheus-operator-sharding
name: prometheus-operator-sharding
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-operator
tags: [sharding, shards, modulus, tmp-hash, tmp-disable-sharding, scale-out]
level: advanced
status: docs-checked
description: "Scale Prometheus horizontally with spec.shards, understand the default modulus hashing, custom __tmp_hash distribution and all-shard scraping."
sources: ["https://prometheus-operator.dev/docs/platform/sharding/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
When ingest outgrows one Prometheus, split scrape targets across shards. The operator creates `spec.shards` StatefulSets, each with `spec.replicas` pods (the first shard keeps the plain name; others are `...-shard-N`).

## Default distribution
Prometheus `modulus` relabeling hashes `__address__` for ServiceMonitors and PodMonitors, and `__param_target__` for Probes. To query globally, put a Thanos Querier over all sidecars (and use Thanos Ruler for rules) or remote-write to a central store.

**Limits:** scaling shards up or down does not reshard existing data; old data stays where it was and removed shards' data must be moved manually.

## Custom distribution
Set the `__tmp_hash` label by relabeling at discovery and the operator uses it for shard assignment instead of the default. For example, relabel `sourceLabels: [__meta_kubernetes_pod_namespace, __meta_kubernetes_pod_name]` with `separator: /` to `targetLabel: __tmp_hash`. It works at scrape class level too.

## Scrape from every shard
Set `__tmp_disable_sharding` to a non-empty value with a relabeling (`targetLabel: __tmp_disable_sharding`, `replacement: "true"`) for singleton targets like kube-state-metrics that each shard needs.

## Example
`shards: 2`, `replicas: 2` yields pods `prometheus-prometheus-0/1` and `prometheus-prometheus-shard-1-0/1`; three example-app targets then split between the shards.

## Checked

2026-11-08. Read the Prometheus Operator sharding page in full (raw markdown from the operator repo). Claims on modulus hashing, __tmp_hash, __tmp_disable_sharding, resharding limits and example pod names match.

Method: documentation only; no commands were run.
