---
id: computing-software.cloud-infrastructure-engineering.thanos.compactor-downsampling
name: compactor-downsampling
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-compact, downsampling, aggrchunk, 5m-1h-resolution]
level: advanced
status: docs-checked
description: "Know when the compactor downsamples to 5m and 1h and what a downsampled chunk stores."
sources: ["https://thanos.io/tip/components/compact.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Compactor downsampling

Downsampling rewrites series at lower resolution so long-range queries fetch fewer samples without losing precision. The compactor creates a new block with downsampled chunks, stored as `AggrChunk`, holding `raw`, `count`, `sum`, `min`, `max` and `counter` aggregations per 5m or 1h window.

**Two passes**
- Raw blocks older than 40 hours (2d) are downsampled to 5m.
- 5m blocks older than 10 days (2w) are downsampled to 1h.

There is a delay because downsampled chunks hold fewer samples; chunks are fixed size, so data spanning more time is needed to fill them.

Native histograms are downsampled by reducing the schema; the docs note they store only three aggregates.

Resolution means distance between data points: raw equals the scrape interval, 5m has one point per 5 minutes, 1h one per hour.

`--downsampling.disable` turns it off, which the docs suggest only if you never query long ranges. Tune parallelism with `--downsample.concurrency` (default 1).

If retention at a level is shorter than the minimum age of the next pass, data is deleted before it can be downsampled. Downsampling does not save space: each raw block gains two more blocks, so storage can grow by roughly 3x when all resolutions are kept (the default).

## Checked

2026-11-03. Confirmed against the Thanos Compactor page (components/compact.md): downsampling passes (40 hours, 10 days), retention flags and defaults, delete-delay, halting and thanos_compact_halted, resources, vertical compaction and deduplication flags. Fixed: retention example now uses equal retention per level as the page recommends; persistent-label wording; sharding by selector.relabel-config. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
