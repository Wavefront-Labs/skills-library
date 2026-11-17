---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.prometheus-tsdb-storage-and-retention
name: prometheus-tsdb-storage-and-retention
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, tsdb, wal, storage-retention, tsdb-blocks, retention-time, retention-size, head-block, compaction, chunks, index, tombstones, snapshot, admin-api, delete-series, clean-tombstones, backup, disk-sizing, wal-replay, out-of-order, persistent-volume, pca]
level: advanced
status: docs-checked
description: "Operate the Prometheus TSDB: WAL, head and blocks, disk sizing from samples/sec, retention by time and size, snapshots via the admin API, deleting series, and slow WAL replays."
sources: ["https://prometheus.io/docs/prometheus/latest/storage/", "https://github.com/prometheus/prometheus/blob/main/tsdb/docs/format/README.md", "https://prometheus.io/docs/prometheus/latest/querying/api/#tsdb-admin-apis"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TSDB storage and retention

**Goal:** size, protect and prune Prometheus' local storage so it never fills the disk,
restarts fast, and can be backed up or trimmed without data loss.

## 1. How data lands on disk
```
data/
  wal/                 # write-ahead log segments (128MB by default) + checkpoints
  chunks_head/         # memory-mapped head chunks
  01HXXXX.../          # 2h block: chunks/, index, meta.json, tombstones
  01HYYYY.../          # compacted block (up to 10% of retention, max 31d)
```
- Incoming samples go to the **head** (in memory) and the **WAL**. Every 2 h the head is cut
  into an immutable **block**; blocks are later compacted into larger ones spanning up to 10% of
  the retention time or 31 days, whichever is smaller.
- Deletes only write **tombstones**; space is reclaimed at the next compaction of that block.
- WAL replay on startup is what makes restarts slow on big servers; follow its progress at
  `/api/v1/status/walreplay` (served before the server is ready).

## 2. Retention flags
```bash
prometheus \
  --storage.tsdb.path=/prometheus \
  --storage.tsdb.retention.time=30d \          # default 15d if neither time nor size is set; whichever of time/size trips first wins
  --storage.tsdb.retention.size=200GB \        # only blocks are deleted, but WAL and m-mapped chunks count toward the total
  --storage.tsdb.wal-compression \             # on by default since 2.20.0
  --web.enable-admin-api                       # needed for snapshot/delete endpoints
```
In current releases the two retention flags are marked deprecated; the `tsdb.retention` section of the config
file (`time`, `size`, `percentage`) takes precedence over them. Blocks must be fully expired before they are
removed, and the background cleanup can take up to two hours. Size-based retention removes the oldest data first.

## 3. Sizing
`bytes_needed ≈ retention_seconds × ingested_samples_per_second × bytes_per_sample`
with bytes_per_sample averaging 1-2 (the docs' figure). Measure instead of guessing:
```promql
rate(prometheus_tsdb_head_samples_appended_total[5m])          # samples/s
prometheus_tsdb_head_series                                     # active series (RAM driver)
prometheus_tsdb_storage_blocks_bytes                            # on-disk now
prometheus_tsdb_wal_segment_current, prometheus_tsdb_wal_storage_size_bytes
```
Example: 100k samples/s × 1.5 B × 30 d (2.59e6 s) ≈ 390 GB. Memory scales with active series
(`prometheus_tsdb_head_series`); measure it rather than using a per-series rule of thumb.

## 4. Snapshots and backups
```bash
curl -XPOST http://localhost:9090/api/v1/admin/tsdb/snapshot
# -> {"status":"success","data":{"name":"20261015T120000Z-6f1c..."}}
# hard-linked copy in data/snapshots/<name>/ ; rsync it elsewhere, then delete
rm -rf /prometheus/snapshots/<name>
```
- A snapshot covers finished blocks plus the head (`?skip_head=true` skips head-only data). The docs recommend
  snapshots for backups: a backup without one can lose the samples since the last block was cut (every two
  hours, covering the last three hours of samples).
- Restore: stop Prometheus, place the block directories into `data/`, start. The
  `--storage.tsdb.allow-overlapping-blocks` flag is only needed on v2.38 and below.
- Local storage must be a POSIX-compliant filesystem; NFS (including AWS EFS) is not supported.
- Long retention belongs in Thanos/Mimir; local TSDB is for the hot window.

## 5. Deleting data
```bash
curl -XPOST -g 'http://localhost:9090/api/v1/admin/tsdb/delete_series?match[]=container_tasks_state&start=2026-01-01T00:00:00Z'
curl -XPOST http://localhost:9090/api/v1/admin/tsdb/clean_tombstones     # reclaim now
```
Both return 204 on success. Omitting `start` and `end` clears all data for the matched series.
Use for leaked cardinality (a bad label rollout) rather than waiting for retention.
Protect the admin API behind auth or network policy; it is destructive.

## 6. Operational checks and gotchas
- Alert before the volume fills, for example on a predicted exhaustion:
  `predict_linear(node_filesystem_avail_bytes{mountpoint="/prometheus"}[6h], 24*3600) < 0`.
- Corrupted storage: back up the directory, restore good blocks from backup, and as a last resort remove
  the corrupted block directories or WAL files; that loses the time range they cover.
- `prometheus_tsdb_compactions_failed_total` rising → check disk I/O and space; during compaction the
  source blocks and the new block coexist on disk, so on-disk size can briefly exceed the retention size.
- Kubernetes: always a PersistentVolume with `ReadWriteOnce`; emptyDir loses everything,
  and two replicas must never share a volume.
- Out-of-order samples are rejected by default (`out_of_order_time_window` defaults to 0s). It is set in
  the `tsdb` section of the config file, not as a flag.
- Exemplar storage is experimental and needs `--enable-feature=exemplar-storage`.

## Checked
2026-10-28. Confirmed against prometheus.io Storage page (retention defaults, 10%/31d compaction cap, 1-2 bytes
per sample, wal-compression default since 2.20.0, snapshot advice, overlapping-blocks v2.38 note, NFS caution),
the command-line and configuration pages (retention flags deprecated, `tsdb.retention`, `out_of_order_time_window`),
the TSDB admin API and status API pages, the WAL format doc (128MB segments) and Prometheus source (metric names
`prometheus_tsdb_wal_*`, `prometheus_tsdb_wal_corruptions_total`). Removed: min/max block duration flags,
zstd flag value, 6h/18h compaction steps, per-series RAM figure, disk-headroom percentage, exemplar persistence
and native-histogram store claims, a non-existent out-of-order flag, a log line not found in source.
Method: documentation only; no commands were run.

## Verify
- [ ] Disk growth per day roughly matches the sizing formula.
- [ ] A snapshot restores into a scratch Prometheus and queries return old data.
- [ ] `prometheus_tsdb_compactions_failed_total` and `prometheus_tsdb_wal_corruptions_total` are 0.
- [ ] Restart time (WAL replay) is known and acceptable; if not, shard the server.
