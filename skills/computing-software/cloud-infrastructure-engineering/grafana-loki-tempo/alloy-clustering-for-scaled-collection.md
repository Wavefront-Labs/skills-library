---
id: computing-software.cloud-infrastructure-engineering.grafana-loki-tempo.alloy-clustering-for-scaled-collection
name: alloy-clustering-for-scaled-collection
category: computing-software
field: cloud-infrastructure-engineering
product: grafana-loki-tempo
tags: [alloy-clustering, alloy, cluster-mode, target-distribution, statefulset, join-address, consistent-hashing]
level: practitioner
status: docs-checked
description: "Cluster Alloy replicas so scrape targets are shared without duplication, with peer discovery and rollout caveats."
sources: ["https://grafana.com/docs/alloy/latest/get-started/clustering/", "https://grafana.com/docs/alloy/latest/reference/cli/run/", "https://grafana.com/docs/alloy/latest/troubleshoot/debug/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: scale metric scraping horizontally by letting Alloy replicas share the targets.

Clustering uses an eventually consistent model with a gossip protocol. It assumes all participating deployments are interchangeable and run identical configurations. A standalone Alloy behaves like a single-node cluster.

Start replicas with `--cluster.*` flags on `alloy run`:
```
alloy run /etc/alloy/config.alloy \
  --cluster.enabled=true \
  --cluster.join-addresses=alloy-peers.monitoring.svc:12345 \
  --cluster.rejoin-interval=60s
```
`--cluster.join-addresses` takes a comma-separated list of IP addresses or DNS names and is mutually exclusive with `--cluster.discover-peers`. `--cluster.rejoin-interval` defaults to `60s`. Other flags cover the node name, advertised address, TLS between peers, and a cluster name that keeps unrelated nodes out.

Cluster-enabled components must also opt in with a `clustering` block:
```
prometheus.scrape "all" {
  targets    = discovery.kubernetes.pods.targets
  forward_to = [prometheus.remote_write.mimir.receiver]
  clustering { enabled = true }
}
```
For target auto-distribution all deployments must use the same service discovery APIs and scrape the same targets. When a node joins or leaves, each component locally recalculates ownership with consistent hashing, so only about 1/N of targets move, without communicating ownership over the network. Components documented with clustering support include `prometheus.scrape`, `pyroscope.scrape`, `prometheus.operator.podmonitors` and `prometheus.operator.servicemonitors`.

Gotchas
- Do not enable clustering if you do not need it: it adds logs, metrics and processing overhead. A common mistake is enabling it on log-collecting DaemonSets, where each instance only reads Pods on its own node.
- `--cluster.wait-for-size` holds cluster-enabled components until the cluster reaches that many instances. Set it well below the expected instance count (and below any HPA or PodDisruptionBudget minimums) and pair it with `--cluster.wait-timeout`, since components stop processing while the condition is unmet.
- With a mix of very large and average targets, too many instances give uneven load; scaling vertically can be better.
- Node names must be unique; the cluster rejects conflicting names.

## Verify
The Alloy UI clustering page lists each node's name, advertised address and state (Viewer, Participant or Terminating) and marks the local node.

## Checked
Method: docs-checked 2026-11-09 against the Alloy docs clustering concept page, the alloy run CLI reference and the debug page (raw markdown from the grafana/alloy repo, read in full). The original cited configure/clustering page was not available as raw markdown, so Helm settings and rollout-gap claims were dropped.
