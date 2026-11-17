---
id: computing-software.cloud-infrastructure-engineering.google-cloud.bigtable-monitoring-cpu-latency-and-key-visualizer
name: bigtable-monitoring-cpu-latency-and-key-visualizer
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, bigtable, bigtable-monitoring, bigtable-metrics, key-visualizer, hotspots]
level: practitioner
status: docs-checked
description: "Keep Bigtable healthy: CPU and storage-utilisation thresholds, latency metrics, hottest-node and hot-tablet views, Key Visualizer heatmaps, and alerts that fire before SLOs break."
sources: ["https://docs.cloud.google.com/bigtable/docs/monitoring-instance", "https://docs.cloud.google.com/bigtable/docs/keyvis-overview", "https://docs.cloud.google.com/bigtable/docs/performance", "https://docs.cloud.google.com/bigtable/docs/metrics", "https://docs.cloud.google.com/sdk/gcloud/reference/bigtable/hot-tablets/list"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bigtable monitoring

## 1. Metrics that matter
| Metric | Healthy |
|---|---|
| `bigtable.googleapis.com/cluster/cpu_load` | at most 60% for latency-optimised workloads, 90% for throughput-optimised (Bigtable performance guidance) |
| `cluster/cpu_load_hottest_node` | same limits; high with low average = hotspot (the hottest node can change quickly) |
| `cluster/storage_utilization` | no more than 70% of the hard storage limit (SSD 5 TB/node, HDD 16 TB/node) |
| `server/latencies` (by method, app profile) | p99 within SLO |
| `replication/max_delay` (and the replication latency input/output metrics) | for replicated instances |

Client-side metrics (`client/` prefix, for example `client/attempt_latencies` and `client/operation_latencies`) help separate network and retry time from server latency; Java clients can enable them.

## 2. Alerts
Alert on `cpu_load` and `cpu_load_hottest_node` above the limits in the table for a sustained period per cluster, and on `storage_utilization` above 0.7 (the storage alert threshold used in the Bigtable monitoring documentation). With autoscaling enabled, alerts then mean the autoscaler has reached its maximum.

## 3. Find hotspots
- **Key Visualizer** (Bigtable console → table → Key Visualizer): heatmap of ops/latency by row-key range over time.
  Bright (hot) areas mean high values for the chosen metric; a vertical band across all keys points to *when* something happened table-wide. See the Key Visualizer heatmap-patterns page for how to read common shapes.
- **Hot tablets**: `gcloud bigtable hot-tablets list <CLUSTER> --instance=<I>` lists hot tablets in a cluster (optional `--start-time` and `--end-time`; the default window is the past 24 hours).
- Fix with key design (salting, field promotion, reversing timestamps), not by adding nodes.

## Gotchas
- Key Visualizer is available for tables with at least 1 GB of data per cluster; a new table can take up to an hour to qualify and a few days (up to a week) for data to appear. Scans are produced every 15 minutes and kept for 14 days.
- After scaling up, performance can take up to 20 minutes under load to improve.
- Rows above the recommended 100 MB total value size hurt performance.

## Verify
- [ ] Dashboard has CPU, hottest node, storage and server latency per app profile.

## Checked
Checked 2026-10-24 against the Bigtable performance, monitoring, Key Visualizer overview and metrics pages, the quotas page and the gcloud `bigtable hot-tablets list` reference (docs.cloud.google.com). Confirmed metric names (`cluster/cpu_load`, `cluster/cpu_load_hottest_node`, `cluster/storage_utilization`, `server/latencies`, `replication/max_delay`, `client/` metrics), the 60%/90% CPU and 70% storage figures, the 1 GB Key Visualizer minimum, the 20-minute rebalance note and the hot-tablets flags. Removed the 70/50 and 35% CPU splits, the 30 GB and 10k rows/s Key Visualizer thresholds, the policy command, specific alert windows and autoscaler targets, and the diagonal-band interpretation, none of which the documentation confirms.
Method: documentation only; no commands were run.
