---
id: computing-software.cloud-infrastructure-engineering.grafana-alloy.grafana-alloy-clustering-distribute-workload
name: grafana-alloy-clustering-distribute-workload
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-alloy
tags: [clustering-block, lokisourcekubernetes, pyroscopescrape, duplicate-scraping, hash-ring]
level: practitioner
status: docs-checked
description: "Enable the clustering block on scrape and log components, verify distribution, and avoid node-specific labels."
sources: ["https://github.com/grafana/alloy/blob/main/docs/sources/configure/clustering/distribute-workload.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Distributing workload across cluster nodes

Prerequisites: clustering enabled on the instances, and an identical configuration file everywhere. Add the block to each participating component:

```alloy
loki.source.kubernetes "pods" {
  targets    = discovery.kubernetes.pods.targets
  forward_to = [loki.write.default.receiver]
  clustering {
    enabled = true
  }
}
```

Components that support `clustering`: `prometheus.scrape`, `prometheus.operator.podmonitors`, `prometheus.operator.probes`, `prometheus.operator.scrapeconfigs`, `prometheus.operator.servicemonitors`, `pyroscope.scrape`, `loki.source.kubernetes`, `loki.source.kubernetes_events`, `loki.source.podlogs`, and `database_observability.mysql`.

## Gotchas
- Components do not participate automatically. In cluster mode, a component without `clustering { enabled = true }` runs its full workload on every node, producing duplicate scraping, log collection or profiling.
- Target labels must be identical across nodes. A node-specific label such as `constants.hostname` added during discovery breaks consistent hashing, so ownership cannot be decided.

## Verify
After a reload, open the component details page on two nodes and compare **Debug Info**: their target sets must not overlap.

## Behaviour
All nodes use consistent hashing; each processes only its own subset; when a node joins or leaves, roughly 1/N of targets move.

## Checked

2026-11-08. Read in full the raw Alloy docs page behind the cited URL (docs/sources/configure/clustering/distribute-workload.md): prerequisites, the clustering block, the component list, the duplicate-workload note, the Debug Info validation steps, and the consistent-label note. Nothing removed.

Method: documentation only; no commands were run.
