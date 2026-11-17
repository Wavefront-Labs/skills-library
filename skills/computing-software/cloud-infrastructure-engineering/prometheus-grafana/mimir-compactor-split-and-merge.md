---
id: computing-software.cloud-infrastructure-engineering.prometheus-grafana.mimir-compactor-split-and-merge
name: mimir-compactor-split-and-merge
category: computing-software
field: cloud-infrastructure-engineering
product: prometheus-grafana
tags: [mimir-compactor, split-and-merge-compaction, mimir, compaction, object-storage]
level: advanced
status: docs-checked
description: "Operate the Mimir compactor: split-and-merge shard and group settings, block ranges, disk sizing, retention, no-compact marks with mimirtool, and out-of-disk handling."
sources: ["https://grafana.com/docs/mimir/latest/references/architecture/components/compactor/", "https://grafana.com/docs/mimir/latest/configure/configuration-parameters/", "https://grafana.com/docs/mimir/latest/manage/mimir-runbooks/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mimir compactor (split-and-merge)

The compactor is stateless and compacts per tenant. It merges blocks uploaded by ingesters for the same time range
(2 hour ranges by default) into one block and deduplicates replicated samples (vertical compaction), then compacts
adjacent ranges into larger blocks (horizontal compaction). It also keeps the per-tenant bucket index updated and
deletes blocks outside the retention period. Split-and-merge is for large tenants: it avoids TSDB index limits and
indefinitely growing blocks.

## How split-and-merge works
- Split stage (first level, for example 2h): source blocks are divided into N groups (`-compactor.split-groups`); each
  group is compacted into M split blocks (`-compactor.split-and-merge-shards`), each holding a subset of series. The
  default configuration disables the split stage.
- Merge stage: the N split blocks of each shard are merged, reducing N * M blocks to M, then merge continues on the
  other ranges (for example 12h and 24h) within the same shard.
- Docs recommend 1 shard per 8 million active series in a tenant (about 16 for 100 million) and a power-of-two shard
  count. Beyond roughly 96 shards the page describes trade-offs: more blocks per tenant, more index-headers on
  store-gateways, more merge jobs and more compactor disk.
- More split groups give more, smaller split jobs so several compactors can work in parallel, at the cost of more
  intermediate blocks.
- Changing the shard count affects only blocks not yet split; already split blocks keep the configuration stored in
  their `meta.json`.

## Settings (names and defaults from the configuration reference)

| YAML key | CLI flag | Default |
|---|---|---|
| `compactor.block_ranges` | `-compactor.block-ranges` | 2h, 12h, 24h |
| `compactor.data_dir` | `-compactor.data-dir` | `./data-compactor/` |
| `compactor.compaction_interval` | `-compactor.compaction-interval` | 1h |
| `compactor.compaction_concurrency` | `-compactor.compaction-concurrency` | 1 |
| `compactor.cleanup_interval` | `-compactor.cleanup-interval` | 15m |
| `limits.compactor_split_and_merge_shards` | `-compactor.split-and-merge-shards` | 0 (splitting disabled) |
| `limits.compactor_split_groups` | `-compactor.split-groups` | 1 |
| `limits.compactor_blocks_retention_period` | `-compactor.blocks-retention-period` | 0s (no retention) |
| `limits.compactor_tenant_shard_size` | `-compactor.compactor-tenant-shard-size` | 0 (all compactors) |

`compactor_split_and_merge_shards` values greater than 1 are rounded up to the next power of two. The limits are
per-tenant overrides. Compactors register in a hash ring; with shuffle sharding enabled (tenant shard size above 0 and
below the number of compactors) only that many compactors compact a given tenant. Each compaction uses one CPU core, and
`-compactor.compaction-concurrency` is the number of concurrent compactions in one instance.

## Disk sizing
The compactor stores downloaded input blocks and produced blocks under `-compactor.data-dir`. Put it on a volume other
than the root volume; on Kubernetes run compactors as a StatefulSet. Minimum estimate from the docs:
`compactor.compaction-concurrency * max_compaction_range_blocks_size * 2`, where the size is for the largest tenant over
the longest block range. With a 24h largest range the page also gives 150GB per 10M active series of the largest tenant
(for example 450GB for 30M series at concurrency 1).

If the compactor runs out of disk the runbook says the job will likely hit the same limit on each retry; confirm by
searching logs for `no space left on device`.

## Deletion and retention
After a successful compaction the original blocks are soft-deleted (marked via a `deletion-mark.json` in the bucket) and
hard-deleted after `-compactor.deletion-delay`, giving queriers, rulers and store-gateways time to find the new
blocks. Retention is disabled by default; set the retention period explicitly. Do not share one bucket between
ruler/alertmanager storage and blocks: the page says it causes compactor issues.

## Problem blocks
A block that cannot be compacted (for example one that produces out-of-order chunks, or a result block that exceeds the
symbol table size) is marked `no-compact` so later runs are not blocked. The runbook uses mimirtool:

```bash
mimirtool blocks mark --backend gcs --gcs.bucket-name <bucket> --mark-type no-compact --tenant <tenant-id> --details "<reason>" --blocks "<block-1>,<block-2>"
```

`--mark-type` accepts `deletion` or `no-compact`. A symbol-table error indicates the shard count is too low for the
tenant. Find the source block IDs in compactor logs as the runbook describes before marking.

## Job order
`-compactor.compaction-jobs-order` is `smallest-range-oldest-blocks-first` (default; all split jobs go to the front of
the queue) or `newest-blocks-first`.

## Checked

Checked 2026-11-08 against the Mimir compactor architecture page, the configuration parameters reference (YAML keys,
CLI flags and defaults) and the runbooks (`mimirtool blocks mark`, out-of-disk and out-of-order/symbol-table sections).
Removed because the pages do not state them: the `cortex_*` health metric names, the 24h alert threshold, the `markblocks`
tool under `tools/`, `tsdb-*` tools, the object-store latency metric, the "1y" retention example and the
"retries forever" wording.
Method: docs-only read of cited pages, 2026-11-08
