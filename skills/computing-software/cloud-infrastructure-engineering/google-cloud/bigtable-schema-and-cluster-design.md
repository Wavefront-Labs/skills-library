---
id: computing-software.cloud-infrastructure-engineering.google-cloud.bigtable-schema-and-cluster-design
name: bigtable-schema-and-cluster-design
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, bigtable, cloud-bigtable, wide-column, row-key-design, hotspotting, column-families, garbage-collection-policy, replication, multi-cluster-routing, app-profiles, bigtable-autoscaling, key-visualizer, cbt, hbase-api, bigtable-backups, time-series, tall-vs-wide]
level: advanced
status: docs-checked
description: "Design and run Bigtable: row keys that spread load, column families with GC policies, tall vs wide time series, replication and app-profile routing, autoscaling, backups, and Key Visualizer."
sources: ["https://docs.cloud.google.com/bigtable/docs/schema-design", "https://docs.cloud.google.com/bigtable/quotas", "https://docs.cloud.google.com/bigtable/docs/performance", "https://docs.cloud.google.com/bigtable/docs/replication-overview", "https://docs.cloud.google.com/sdk/gcloud/reference/bigtable/instances/create", "https://docs.cloud.google.com/sdk/gcloud/reference/bigtable/app-profiles/create", "https://docs.cloud.google.com/sdk/gcloud/reference/bigtable/backups/create", "https://github.com/googleapis/cloud-bigtable-cbt-cli/blob/main/cbtdoc.go"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bigtable schema and cluster design

**Goal:** low-latency reads and writes at scale, which Bigtable delivers only
when the row key spreads traffic, the table is shaped for the access pattern, and the cluster is sized for throughput and storage.

## 1. Row key design (everything depends on this)
- Rows are sorted lexicographically by key and sharded into tablets by key range; **sequential keys hotspot** one node. Timestamps, incrementing IDs, or a low-cardinality prefix (`country#…`) are the classic mistakes.
- Pattern: `<high-cardinality-id>#<reverse-or-bucketed-time>` e.g. `device123#20261015T1030` — reads of one device's recent data become a single scan, writes spread across devices.
- Field promotion: put the most common filter in the key; Bigtable has **no secondary indexes** as such; GoogleSQL continuous materialized views can pre-compute alternative layouts.
- Keep keys short (hard limit 4 KB per row key); avoid hashing *unless* you never range-scan (a hash prefix kills locality).
- Salting (`<hash%N>#<key>`) spreads hot sequential writes across N ranges at the cost of N parallel reads.

## 2. Table shape
- **Column families**: few (the documented recommendation is at most 100), short names (`cf`, `m`), each with its own **GC policy** — `cbt setgcpolicy tbl m maxversions=1 or maxage=30d`. Without a policy, every write keeps every version.
- Hard limits: 4 KB row key, 100 MB per cell value, 256 MB per row; recommended: 10 MB per cell value and 100 MB total per row.
- **Tall vs wide** for time series: tall (one row per event, `id#time`) for unbounded series; wide (one row per `id#bucket`, columns per timestamp) when a row's data is read together and bounded. Column qualifiers can carry data (timestamp as qualifier, empty value).
- Use cell timestamps (`write at ts`) for versioned data and rely on `maxversions` GC rather than custom cleanup.

## 3. Instance and clusters
```bash
gcloud bigtable instances create prod --display-name=prod \
  --cluster-config=id=prod-euw1,zone=europe-west1-b,nodes=3,autoscaling-min-nodes=3,autoscaling-max-nodes=10,autoscaling-cpu-target=60 \
  --cluster-config=id=prod-euw4,zone=europe-west4-a,nodes=3 \
  --cluster-storage-type=ssd
```
- Sizing: per SSD node the docs give up to 17,000 rows/s reads, 14,000 rows/s writes or 220 MBps scans (best case), 5 TB SSD per node, and keep CPU at or below 60% (latency-optimised) or 90% (throughput-optimised). HDD is generally not recommended.
- **Replication**: additional clusters replicate asynchronously (eventually consistent; seconds to minutes for a responsive instance); every cluster serves reads and writes. An instance can span up to 8 regions with one cluster per zone. Each cluster holds its own copy, which increases storage cost.
- **App profiles** decide routing: `--route-to=<cluster>` (single-cluster routing; add `--transactional-writes` to allow single-row transactions) vs `--route-any` (multi-cluster routing with automatic failover and eventual consistency). Create one per workload (`gcloud bigtable app-profiles create batch --instance=prod --route-to=prod-euw4 --transactional-writes`) and pass it in the client so batch jobs are separated from serving traffic. **Request priority** (`--priority=PRIORITY_LOW`, with `PRIORITY_MEDIUM` and `PRIORITY_HIGH`; default high) can be set on batch profiles.
- Autoscaling targets: CPU 10 to 80 percent, storage (SSD) 2560 to 5120 GiB per node; the minimum node count must still cover your stored data.

## 4. Operate
- `cbt` CLI: `cbt -instance prod createtable t families=m:maxversions=1`, `cbt read t prefix=device123# count=5`, `cbt count t`.
- **Key Visualizer** heatmap: the default metric is Ops (reads plus writes); it needs at least 1 GB of data per cluster. Drill down to the key prefix and fix the schema — adding nodes rarely fixes a hotspot.
- Backups: `gcloud bigtable backups create bk --instance=prod --cluster=prod-euw1 --table=t --retention-period=30d` (retention is at most 90 days; exactly one of `--retention-period` or `--expiration-date` is required). `gcloud bigtable backups copy` exists for copying backups.
- Metrics: `bigtable.googleapis.com/cluster/cpu_load_hottest_node` (the one that matters), `server/latencies`, `cluster/storage_utilization`, `replication/latency`.
- Change streams (`--change-stream-retention-period`, 1 to 7 days) feed Dataflow for CDC.

## Gotchas
- After scaling, performance can take up to 20 minutes under load to improve; scaling up does not fix a hotspot caused by key design.
- `cpu_load_hottest_node` far above the average CPU suggests a hotspot rather than under-provisioning.
- Deleting the cluster that a single-cluster app profile routes to breaks that profile's clients; update profiles first.
- Bulk loads through the default app profile compete with serving traffic; give them a separate profile.

## Verify
- [ ] Key Visualizer after load shows even heat; `cpu_load_hottest_node` stays close to the average.
- [ ] A GC policy exists on every family (`cbt ls t` lists them).
- [ ] With a multi-cluster app profile, losing one cluster keeps serving; single-cluster profile clients routed to it fail (as designed).

## Checked
Checked 2026-10-24 against the Bigtable quotas, performance, replication, Key Visualizer and monitoring pages, the gcloud `bigtable instances create`, `app-profiles create` and `backups create` references (docs.cloud.google.com), and the cbt CLI documentation. Confirmed the 4 KB, 100 MB and 256 MB limits and their recommendations, the 5 TB SSD per node figure, per-node throughput, CPU and storage guidance, the `--cluster-config` keys and autoscaling ranges, app-profile flags and priority values, the 90-day backup limit and cbt command syntax. Removed the 70%/35% CPU split, key-length advice, PITR statement, `bigtable.tables.*` IAM advice, latency promises and HBase-shim remark, which were not confirmed. Replication latency described as seconds to minutes per the replication overview.
Method: documentation only; no commands were run.
