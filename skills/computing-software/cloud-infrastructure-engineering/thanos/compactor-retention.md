---
id: computing-software.cloud-infrastructure-engineering.thanos.compactor-retention
name: compactor-retention
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-compact, retention, retention-resolution-raw, bucket-retention]
level: practitioner
status: docs-checked
description: "Set per-resolution retention for raw, 5m and 1h blocks and avoid deleting data before it is downsampled."
sources: ["https://thanos.io/tip/components/compact.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Compactor retention

By default there is no retention: data is kept forever, which the docs call valid and recommended. Set limits per resolution:

```
thanos compact \
  --retention.resolution-raw=90d \
  --retention.resolution-5m=90d \
  --retention.resolution-1h=90d
```

All three default to `0d` (keep forever); the docs also say unset or `0s` means no retention.

**Order of operations.** Retention is applied right after the compaction and downsampling loops. If those loops fail, nothing is ever deleted.

**Interaction with downsampling.** Raw data is downsampled to 5m after 40 hours, and 5m data to 1h after 10 days. If a resolution's retention is shorter than the minimum age of the next pass, blocks are deleted before downsampling can finish. The rule of thumb in the docs: set the same retention for every level, greater than the maximum date range (10 days for the 5m to 1h pass). Keeping raw data shorter than 5m/1h data means you can no longer zoom in on old data.

**Deleting.** Blocks are first marked with `deletion-mark.json` and removed after `--delete-delay` (default 48h).

A block is only deleted once its max time is older than the retention.

## Checked

2026-11-03. Confirmed against the Thanos Compactor page (components/compact.md): downsampling passes (40 hours, 10 days), retention flags and defaults, delete-delay, halting and thanos_compact_halted, resources, vertical compaction and deduplication flags. Fixed: retention example now uses equal retention per level as the page recommends; persistent-label wording; sharding by selector.relabel-config. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
