---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.tsdb-block-layout-and-compaction
name: tsdb-block-layout-and-compaction
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [prometheus, tsdb, block-layout, chunks-index-meta, compaction-tuning, block-compaction, promtool-tsdb, head-block, retention]
level: advanced
status: verified
description: "Read a Prometheus data dir (head, WAL, 2h blocks, chunks/index/meta.json, tombstones), how compaction levels merge blocks, and the flags that change it."
sources: ["https://prometheus.io/docs/prometheus/latest/storage/", "https://github.com/prometheus/prometheus/blob/main/tsdb/docs/format/README.md", "https://ganeshvernekar.com/blog/prometheus-tsdb-compaction-and-retention/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TSDB block layout and compaction

## 1. What is on disk
```
data/
  chunks_head/              # mmapped chunks of the in-memory head block
  wal/                      # 128 MiB segments 00000012, checkpoint.00000011/
  wbl/                      # write-behind log, only when out-of-order is enabled
  01HZX...ULID/             # one persisted block
    meta.json               # ulid, minTime, maxTime, stats.numSeries/numSamples, compaction.level, compaction.sources, version
    index                   # symbol table, series -> chunk refs, postings (label -> series ids)
    chunks/000001           # up to 512 MiB segment files of XOR-compressed chunks
    tombstones              # deletions not yet compacted away
  lock, queries.active
```
- Head covers the most recent ~2-3 h in memory; it is cut into a 2 h block once it spans 1.5x the block range (3 h).
- `promtool tsdb list -r data/` prints every block with time range, series, samples, chunks and size.
- `promtool tsdb analyze data/ [ULID]` shows churn, label-pair and label-name cardinality for one block (the newest by default; `--limit=20` lines per list).
- `cat data/<ULID>/meta.json | jq '.compaction'` shows `level` and the source blocks it was merged from.

## 2. Compaction
- Level 1 blocks span 2 h (`--storage.tsdb.min-block-duration`, default 2h). Compaction merges adjacent blocks into
  ranges that grow by x3 (2 h -> 6 h -> 18 h -> 54 h ...) up to `--storage.tsdb.max-block-duration`, default
  10 % of retention time capped at 31 d.
- Compaction also applies tombstones (rewrites blocks without deleted series) and enforces retention by deleting
  whole blocks whose `maxTime` is older than `--storage.tsdb.retention.time` or that push total size over
  `--storage.tsdb.retention.size`. Retention is block-granular, so data older than the limit can linger up to
  one block range.
- Overlapping blocks (from backfill or out-of-order) are vertically compacted automatically (always on since 2.39).

## 3. When to change the defaults
| Situation | Setting |
|---|---|
| Thanos sidecar / object-store uploader | `--storage.tsdb.min-block-duration=2h --storage.tsdb.max-block-duration=2h` (no local compaction; the compactor does it) |
| Large single node, long retention | leave defaults; bigger blocks mean fewer index lookups for long queries |
| Disk spikes during compaction | budget ~2x the largest block in free space; a compaction writes the new block before deleting sources |

## Gotchas
- Never copy or delete files inside a live block; remove whole ULID directories only while Prometheus is stopped (or let retention do it).
- `retention.size` counts WAL and head chunks too (only blocks are deleted to honour it); Prometheus docs recommend at most 80-85 % of the volume so compaction headroom remains.
- A block left with a `.tmp-for-creation` or `.tmp-for-deletion` suffix is a crash leftover; Prometheus cleans it at start.
- Compaction failures show as `prometheus_tsdb_compactions_failed_total` increasing and blocks piling up at level 1.

## Verify
- [ ] `promtool tsdb list -r` shows contiguous, non-overlapping ranges and level > 1 blocks for older data.
- [ ] `prometheus_tsdb_compactions_failed_total` is flat; `prometheus_tsdb_blocks_loaded` is stable over a day.
- [ ] Oldest block `minTime` is within one block range of the configured retention.
