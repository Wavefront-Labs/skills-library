---
id: computing-software.cloud-infrastructure-engineering.thanos.compactor-vertical-compaction
name: compactor-vertical-compaction
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-compact, vertical-compaction, offline-deduplication, replica-label]
level: sme
status: docs-checked
description: "Enable vertical compaction and offline deduplication safely, with the irreversible risks spelled out."
sources: ["https://thanos.io/tip/components/compact.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Vertical compaction and offline deduplication

Vertical compaction merges overlapping blocks (multiple streams) into one. Valid use cases per the docs:
- races between several compactors, or between Thanos and Prometheus compaction (safe, but extra compute);
- backfilling where data already exists for that time range;
- offline deduplication of replicated series, with one-to-one or penalty strategies.

Enable it with the hidden flag `--compact.enable-vertical-compaction`. To group streams differently for deduplication, set `--deduplication.replica-label=LABEL` (repeatable; the process is irreversible) to ignore those labels when loading blocks.

`--deduplication.func` is experimental: empty uses the default 1:1 merger, `penalty` uses the penalty algorithm.

**Risks stated by the docs**
- Uploading blocks with the same external labels from unrelated Prometheus servers can merge unrelated series.
- Merged disjoint series cannot easily be split again.
- Penalty deduplication has known limitations, for example breaking `rate`/`irate`.

The docs advise backing up your data first before enabling penalty deduplication.

## Checked

2026-11-03. Confirmed against the Thanos Compactor page (components/compact.md): downsampling passes (40 hours, 10 days), retention flags and defaults, delete-delay, halting and thanos_compact_halted, resources, vertical compaction and deduplication flags. Fixed: retention example now uses equal retention per level as the page recommends; persistent-label wording; sharding by selector.relabel-config. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
