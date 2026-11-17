---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.thanos-compactor-retention-and-downsampling
name: thanos-compactor-retention-and-downsampling
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [thanos, thanos-compactor, compactor-retention, downsampling-config, retention-resolution, vertical-compaction, halted-compactor]
level: advanced
status: docs-checked
description: "Operate the Thanos compactor: per-resolution retention, 5m/1h downsampling, the singleton rule, vertical-compaction dedup, disk sizing, and recovering a halted compactor."
sources: ["https://thanos.io/tip/components/compact.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thanos compactor: retention and downsampling

```bash
thanos compact --wait \
  --data-dir=/var/thanos/compact --objstore.config-file=/etc/thanos/objstore.yml \
  --retention.resolution-raw=30d \
  --retention.resolution-5m=180d \
  --retention.resolution-1h=2y \
  --deduplication.replica-label=replica \
  --compact.enable-vertical-compaction \
  --delete-delay=48h
```

## Rules
- **Exactly one compactor per bucket** (or per disjoint `--selector.relabel-config` shard). Two compactors on
  the same blocks corrupt the bucket.
- Downsampling: blocks >= 40 h get a 5 m version; >= 10 d get 1 h. Downsampled blocks are *added*, so with
  equal retentions you store more, not less. Downsampling exists to make long-range queries fast.
- Keep `resolution-raw` >= ~40 h or downsampling has nothing to work on; set 5m and 1h retentions
  >= raw, otherwise zoomed-out panels go empty when raw expires.
- Downsampling exists so range queries over months or years stay fast; keep raw at least as long as 5m and 1h if you need to zoom in on old data.

## Dedup in the compactor
`--deduplication.replica-label` + vertical compaction (a hidden flag) merges HA-replica blocks into one.
Use `--deduplication.func=penalty` for Prometheus HA pairs (same algorithm as Query).

## Disk
Needs local disk for the blocks of one compaction group: in the worst case twice the largest (2-week) block span, times `--compact.concurrency`. The docs call about 100GB enough for a medium bucket; it is safe to delete on restart.

## Halted compactor
`thanos_compact_halted == 1` means it found overlapping blocks or a malformed block and stopped. Logs name
the block ULIDs. Fix: inspect with `thanos tools bucket inspect`, mark the bad one
(`thanos tools bucket mark --id=<ULID> --marker=no-compact-mark.json` or `deletion-mark.json`), restart.

## Monitor
```promql
thanos_compact_halted == 1
increase(thanos_compact_group_compactions_failures_total[1h]) > 0
time() - max(thanos_objstore_bucket_last_successful_upload_time{job="thanos-compact"}) > 86400
```

## Verify
- [ ] `thanos tools bucket inspect` shows levels growing and 5m/1h resolutions for older blocks.
- [ ] `thanos_compact_halted` 0 for a week; bucket size flattens once retention kicks in.

## Checked
- 2026-10-28. Confirmed against the Thanos Compact page (`--wait`, `--delete-delay=48h`, `--compact.concurrency`, 40 hour and 10 day downsampling passes, retention rules, hidden `--compact.enable-vertical-compaction`, halting and `thanos_compact_halted`, disk guidance), the mixin compact alerts (`thanos_compact_group_compactions_failures_total`, `thanos_objstore_bucket_last_successful_upload_time`) and the Tools page (`bucket mark`, `no-compact-mark.json`).
- Removed: `max_source_resolution=auto`, the "halving storage" claim, the 100-500 GB range and `thanos_compact_todo_compactions`.
Method: documentation only; no commands were run.
