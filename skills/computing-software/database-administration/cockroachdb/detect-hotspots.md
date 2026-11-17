---
id: computing-software.database-administration.cockroachdb.detect-hotspots
name: detect-hotspots
category: computing-software
field: database-administration
product: cockroachdb
tags: [detect-hotspots, hot-node, hot-range, popular-key, latch-conflict-wait]
level: advanced
status: docs-checked
description: "Diagnose CockroachDB hotspots: node outliers in latch wait and CPU metrics, no split key found and popular key detected logs in KV_DISTRIBUTION, then hot ranges."
sources:
  - https://www.cockroachlabs.com/docs/stable/detect-hotspots
  - https://www.cockroachlabs.com/docs/stable/understand-hotspots
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: confirm and localize a hotspot, then pick a mitigation.

Concepts: a hotspot is a skewed access pattern, usually seen as higher CPU on a few nodes; also disk I/O or memory. A hot node is the usual symptom. A hot node shows clearly higher utilization than its peers.

Step 1, find a node outlier:
- Custom chart in DB Console Advanced Debug: metric `kv.concurrency.latch_conflict_wait_durations-avg`, with `PER NODE/STORE` selected.
- Hardware dashboard CPU Percent: a hottest node 20% or more above the cluster average is the page's threshold for suspicion.
Note the node ID and time window. If neither metric shows an outlier, consider causes other than a hotspot.

Step 2, search logs on that node for `no split key found`, emitted on the `KV_DISTRIBUTION` channel when one replica uses a large share of the node's resources. The tag segment gives node (`n5`) and range (`r1115`). The message ends with one of: `popular key detected, clear direction detected`; `popular key detected, no clear direction`; `no popular key, clear direction detected`; `no popular key, no clear direction`.
- `popular key detected` means a large share of reads or writes target one row in a range; correlated with latch conflict outliers it is likely a write hotspot.

Step 3, take the range ID to the `hot_ranges_stats` event log on the `HEALTH` channel (near the metric outlier time), note the `Databases`, `Tables` and `Indexes` values, then determine the table and index and mitigate (for example hash-sharded indexes for sequential keys, better key design, splitting by load).

## Checked

2026-11-03. Confirmed against the detect hotspots and understand hotspots pages: latch wait metric, CPU threshold of 20%, `no split key found` on `KV_DISTRIBUTION`, the four message endings, `hot_ranges_stats` on `HEALTH`, mitigation examples. Removed: the load-based splitting tradeoff, the capacity claim and the invented verification step.
Method: documentation only; no commands were run.
