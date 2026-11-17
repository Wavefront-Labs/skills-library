---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.thanos-querier-deduplication
name: thanos-querier-deduplication
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [replica-label-dedup, thanos-dedup, thanos-query, prometheus-ha-pair, deduplication]
level: advanced
status: docs-checked
description: "Deduplicate HA Prometheus replicas in Thanos Query with --query.replica-label, penalty vs chain algorithms, the dedup API parameter, and offline vertical-compaction dedup risks."
sources: ["https://thanos.io/tip/components/query.md/#deduplication", "https://thanos.io/tip/components/compact.md/#vertical-compactions", "https://thanos.io/tip/operating/compactor-backlog.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thanos Querier deduplication

Prometheus cannot replicate its database, so HA is run as multiple replicas. Thanos Querier pulls data from both and
deduplicates, filling gaps transparently to the consumer.

## Query-time deduplication
A fixed single or multiple replica labels must be chosen for the entire cluster and passed to query nodes on startup.
Series distinguished only by those labels are merged into one series, which also hides gaps in a single source.

```bash
thanos query \
  --http-address "0.0.0.0:9090" \
  --query.replica-label "replica" \
  --query.replica-label "replicaX" \
  --endpoint "<store-api>:<grpc-port>" \
  --endpoint "<store-api2>:<grpc-port>"
```
The flag repeats for multiple labels. The page's example: sidecars labelled `cluster=1,env=2,replica=A`,
`...replica=B` and a second cluster's `replica=A` give 2 results for `up{job="prometheus",env="2"}` with the flag and 3
without it.

API parameters on the Query API:
- `dedup` (boolean): default true, but the effect depends on the `--query.replica-label` configuration.
- `replicaLabels` (repeatable): overrides the `--query.replica-label` flag at query time.

## Algorithms (`--deduplication.func`)
- `penalty` (default): fills gaps only after a certain penalty window, which avoids flapping between replicas because of
  minor differences or delays.
- `chain`: 1:1 deduplication that merges all available points without a penalty; useful for Receive-based deployments
  where each replica holds the same data (penalty may cause gaps there). The page notes that deduplication of HA groups is
  not supported by the chain algorithm.

## Offline deduplication (Thanos Compact, vertical compaction)
Vertical compaction merges multiple streams of blocks into one and is enabled with the hidden flag
`--compact.enable-vertical-compaction`. Use `--deduplication.replica-label=LABEL` (repeatable) to ignore labels when
grouping block streams, and `--deduplication.func=FUNC` to choose the algorithm; the compactor default is the original
one-to-one deduplication, and penalty is enabled with `--deduplication.func=penalty`.

```bash
thanos compact --compact.enable-vertical-compaction --deduplication.replica-label=replica --deduplication.func=penalty ...
```
Use cases named in the docs: races between multiple compactors, backfilling, and offline deduplication of replicated
series (one-to-one for Receive replication; penalty for Prometheus HA replicas).

Risks the docs state: configuration errors are irreversible (blocks from different Prometheus servers with the same
external labels can overlap and merge into useless series; merged disjoint series have no easy way to be split back),
and the penalty offline algorithm has limitations (for example breaking `rate`/`irate`), so back up data first and use it
at your own risk.

## Verify
- [ ] A query for a metric with dedup on returns one series per target, and the same query with `dedup=false` returns one
      per replica.
- [ ] Stopping one replica leaves no gap in Thanos Query results.

## Checked

Checked 2026-11-08 against the Thanos Query page (deduplication, algorithms, API parameters) and the Thanos Compact
vertical-compaction section. Removed because the pages do not state them: the `prometheus_replica` Operator label example,
the DNS SRV endpoint syntax, "halving storage", and the claims about recording rules and alerts needing the replica label
and about rate artefacts at penalty switch points. The compactor-backlog page was not needed for any remaining claim.
Method: docs-only read of cited pages, 2026-11-08
