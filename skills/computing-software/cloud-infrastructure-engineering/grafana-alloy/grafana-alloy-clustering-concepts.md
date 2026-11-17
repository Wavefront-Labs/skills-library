---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-clustering-concepts
name: grafana-alloy-clustering-concepts
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [clustering, consistent-hashing, gossip, target-auto-distribution, wait-for-size, hpa]
level: practitioner
status: docs-checked
description: "Alloy clustering: gossip, consistent hashing, target auto-distribution, wait-for-size and when not to cluster."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/get-started/clustering.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Alloy clustering concepts

Clustering gives workload distribution and high availability using an eventually consistent gossip protocol. It assumes nodes are interchangeable and run identical configurations. A standalone Alloy behaves like a single-node cluster. Configure with `--cluster.*` flags of `alloy run`; each component must also opt in through a `clustering` block.

## Target auto-distribution
The main use case: scrapers on every peer share the load. It requires every node to use the same service discovery APIs and scrape the same targets. Nodes use a local consistent hash with 512 tokens each, rebalance without network coordination, and when membership changes only about 1/N of targets move. Supporting components include `prometheus.scrape`, `pyroscope.scrape`, `prometheus.operator.podmonitors` and `prometheus.operator.servicemonitors`.

```alloy
prometheus.scrape "default" {
  targets    = discovery.kubernetes.pods.targets
  forward_to = [prometheus.remote_write.default.receiver]
  clustering {
    enabled = true
  }
}
```

## Best practices
- A few very large targets among many small ones cause uneven load; scale vertically instead of adding instances.
- `--cluster.wait-for-size` holds clustered components until enough nodes exist. Keep it well below the HPA and PodDisruptionBudget minimums, or traffic stops during rolling updates. Pair it with `--cluster.wait-timeout`, and remember that after the timeout the cluster may be too small.
- Do not enable clustering when unneeded: it adds logs, metrics and processing. A common mistake is clustering a log-collecting DaemonSet, where each instance only reads its own node.

Monitor via the UI clustering page.

## Checked

2026-11-08. Read in full the raw Alloy docs page behind the cited URL (docs/sources/get-started/clustering.md): the gossip and consistent-hashing model, 512 tokens, the 1/N redistribution, supported components, and all three best practices. Nothing removed.

Method: documentation only; no commands were run.
