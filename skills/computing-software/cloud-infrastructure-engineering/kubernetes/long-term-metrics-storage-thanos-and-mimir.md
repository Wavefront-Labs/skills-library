---
id: computing-software.cloud-infrastructure-engineering.kubernetes.long-term-metrics-storage-thanos-and-mimir
name: long-term-metrics-storage-thanos-and-mimir
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, thanos, mimir, cortex, remote-write, long-term-storage, multi-cluster-monitoring, prometheus-federation, object-storage, compactor, query-frontend, downsampling]
level: sme
status: docs-checked
description: "Choosing and running Thanos or Mimir for long-term, multi-cluster Prometheus storage: sidecar vs remote-write ingestion, compaction/downsampling, and query-path failure modes."
sources: ["https://thanos.io/tip/components/compact.md/", "https://thanos.io/tip/components/query.md/", "https://thanos.io/tip/components/sidecar.md/", "https://thanos.io/tip/components/receive.md/", "https://grafana.com/docs/mimir/latest/references/architecture/components/compactor/", "https://grafana.com/docs/mimir/latest/references/architecture/components/query-frontend/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Long-term Prometheus storage in Kubernetes: Thanos vs Mimir, and where it breaks

**Goal:** know why single-cluster Prometheus (local TSDB, weeks of retention) stops being
enough once you have multiple clusters or need months of history, and the operational traps
in the two dominant answers.

## 1. Why local Prometheus isn't enough
Prometheus's local TSDB is designed for a bounded retention window on local disk — fine
per-cluster, but it doesn't natively give you: a single query pane across many clusters, cheap
long-term (months/years) retention on object storage, or HA without duplicate/inconsistent
results between two Prometheus replicas scraping the same targets. Thanos and Mimir
both solve this by adding a storage/query layer on top of or instead of local Prometheus, backed by
object storage.

## 2. Two different ingestion paths — this is the real architecture decision
- **Sidecar model (Thanos's original pattern)**: a `thanos-sidecar` container runs alongside
  each Prometheus pod, optionally uploading Prometheus's TSDB blocks (produced every 2 hours) to
  object storage; the Thanos Querier fans out queries across StoreAPIs: sidecars (recent data) and
  the Store Gateway (historical data in object storage). The sidecar uploads only uncompacted blocks, and
  local compaction must be disabled by setting `--storage.tsdb.min-block-duration` and
  `--storage.tsdb.max-block-duration` equal (the 2h default); keep Prometheus retention at least three
  times the block duration. Prometheus itself is
  unmodified and keeps working standalone if the sidecar/object storage is down — **this
  is the key resilience property**: local scraping and alerting continue even if the
  long-term storage layer is unavailable.
- **Remote-write model (also supported by Thanos via `thanos receive`, which implements the
  Prometheus Remote Write API)**: each Prometheus pushes samples via `remote_write` to a central
  ingestion tier (Mimir: distributor and ingester components writing blocks to object storage). This centralizes ingestion and is the natural fit for many small/ephemeral
  clusters (edge clusters, short-lived CI clusters) where running a full sidecar/store setup
  per cluster is overkill — but it makes the central ingest tier a shared dependency; each source
  Prometheus buffers in its `remote_write` queue (`queue_config`), so size and monitor it.
- Choosing between them is mostly: sidecar model if you want each cluster's monitoring to
  survive the long-term-storage layer being down; remote-write model if you have many
  clusters and want centralized ingestion/alerting without running Thanos components in
  every one. Mixed deployments (sidecar for a few large clusters, remote-write for many
  small ones feeding the same backend) are common and valid.

## 3. Compaction, downsampling, and the query-path gotchas
- **Thanos Compactor** compacts blocks in object storage and creates 5m downsampled blocks for data
  older than 40 hours and 1h downsampled blocks for data older than 10 days. The docs say it is not
  concurrency safe and must be deployed as a singleton against a bucket (only one instance per stream
  of blocks). **Mimir's compactor** is different: compactors shard work among themselves with a hash
  ring (optionally shuffle-sharded per tenant, with split-and-merge compaction for large tenants). The Mimir
  documents read here do not describe downsampling.
- Thanos downsampled blocks have coarser resolution (5m or 1h), so very short spikes are no longer
  visible in long-range queries on downsampled data.
- The **query-frontend** (Thanos and Mimir) splits long-range queries into smaller queries (Mimir's
  default split interval is 24 hours) and can cache results.
- Compaction and querying generate object storage requests; watch your store's request limits.

## 4. Multi-cluster query fan-out specifics
- Thanos Querier/Mimir's query path needs network reachability to every source
  (sidecars or ingesters) across clusters — a cross-cluster network partition causes
  **partial results with a warning**, not a hard failure, by default for Thanos Querier
  (`--query.partial-response`, default true) — know whether your dashboards are configured to warn visibly on partial
  responses or silently show incomplete data as if it were complete.
- Thanos Querier deduplicates HA pairs using replica labels passed with `--query.replica-label`
  (one label name chosen for the whole cluster); without it, deduplication is off and series are
  returned once per replica. `--deduplication.func` selects `penalty` (default) or `chain`.

## Gotchas
- A dashboard that worked fine against single-cluster Prometheus can silently misbehave
  against a federated Thanos/Mimir query (wrong assumptions about label uniqueness across
  clusters — e.g. `pod` names colliding between two clusters without a `cluster` label to
  disambiguate).
- Retention/downsampling policy changes (lowering a retention window to save object storage
  cost) are often decided without checking whether any PrometheusRule's burn-rate alert
  windows (see
  `computing-software.cloud-infrastructure-engineering.kubernetes.slo-dashboards-for-kubernetes-workloads`)
  depend on a longer raw-resolution window than the new policy keeps.

## Verify
- [ ] Thanos Compactor runs as a verified singleton per bucket; Mimir compactors are configured for ring sharding.
- [ ] A long-range dashboard panel's displayed precision matches awareness of the downsampling schedule — nobody is surprised a 3-month-old spike looks smoothed.
- [ ] `remote_write` queue health is monitored on every source Prometheus, if using the remote-write path.
- [ ] A cross-cluster query during a simulated network partition is confirmed to show a visible partial-response warning, not silently incomplete data.

## Checked

2026-10-26, against Thanos docs (thanos-io/thanos docs/components: compact, query, sidecar, receive; latest commit 2026-10-23) and Mimir docs (grafana/mimir docs/sources/mimir: compactor and query-frontend architecture pages; latest commit 2026-10-24). Confirmed: Thanos sidecar block upload and settings, singleton compactor rule, downsampling thresholds (5m after 40h, 1h after 10 days), `--query.replica-label`, `--query.partial-response` default, Thanos Receive remote write, Mimir compactor ring sharding and split-and-merge, query-frontend split interval. Wrong: the single rule that every compactor must be a singleton (Mimir compactors shard), the implication that Mimir downsamples. Removed unconfirmed claims about Cortex, cache poisoning, object-store throttling and remote_write queue overflow behaviour.

Method: documentation only; no commands were run.
