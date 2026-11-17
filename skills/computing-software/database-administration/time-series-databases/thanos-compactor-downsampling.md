---
id: computing-software.database-administration.time-series-databases.thanos-compactor-downsampling
name: thanos-compactor-downsampling
category: computing-software
field: database-administration
product: time-series-databases
tags: [database-administration, time-series-databases, tsdb-prom-thanos, thanos-compactor-downsampling, prometheus, thanos]
level: practitioner
status: draft
description: "Compact, downsample and enforce retention in the Thanos bucket."
sources:
  - https://thanos.io/tip/thanos/getting-started.md/
  - https://prometheus.io/docs/prometheus/latest/storage/
  - https://prometheus.io/docs/introduction/overview/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Thanos compactor and downsampling

**Goal:** Compact, downsample and enforce retention in the Thanos bucket.

## Steps
- Run exactly one compactor per bucket: `thanos compact --data-dir /var/thanos/compact --objstore.config-file bucket.yml --wait`.
- It merges blocks and creates 5m and 1h resolution downsampled blocks (when raw is over 40h and 10d old respectively, documented, confirm).
- Retention per resolution: `--retention.resolution-raw=30d --retention.resolution-5m=180d --retention.resolution-1h=2y`.
- Downsampling reduces query time on long ranges, not storage; keep raw longer than 40h for it to run.
- Compactor needs local scratch space of several hundred GB for big tenants.
- Horizontal sharding of compaction is possible with relabel selectors.

**Gotcha:** Two compactors on one bucket corrupt blocks; guard with a single replica and strict deployment.

## Verify
- `thanos tools bucket inspect` shows blocks at 5m and 1h resolution.
- Compactor halt metric `thanos_compact_halted` is 0.
