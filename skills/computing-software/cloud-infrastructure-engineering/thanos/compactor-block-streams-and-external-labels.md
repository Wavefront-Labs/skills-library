---
id: computing-software.cloud-infrastructure-engineering.thanos.compactor-block-streams-and-external-labels
name: compactor-block-streams-and-external-labels
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-compact, compaction-groups, external-labels, overlap]
level: advanced
status: docs-checked
description: "Understand how external labels define compaction groups and why they must be unique and persistent."
sources: ["https://thanos.io/tip/components/compact.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Compaction groups and external labels

The compactor groups blocks into "streams" (compaction groups). Blocks with identical external labels are treated as coming from the same source, because those labels are attached by the Prometheus instance (or Thanos component) that produced the block.

The docs flag this as critical: labels must be both
- **unique**: each Prometheus instance's label set differs from every other, so the compactor can group correctly; and
- **persistent**: one Prometheus instance keeps the same labels when it restarts, so the compactor keeps compacting its blocks even if the instance is down for a while.

**Single compactor rule.** Only one compactor may run against one stream in one bucket. Not all object stores have safe locking, so you must ensure this yourself. Running more than one can cause overlap issues that must be repaired manually.

The same reasoning explains why `--shipper.upload-compacted` is separate and why Prometheus's own compaction has to be disabled when sidecars upload.

Several compactors can run against one bucket if each handles a separate stream of blocks. Select streams by external labels with `--selector.relabel-config` (or `--selector.relabel-config-file`), which follows the Thanos sharding relabel syntax.

Prometheus does not store external labels itself; they are added to the `ThanosMeta` section of each block's `meta.json` at upload time. With the default settings, two blocks with the same external labels that overlap in time are treated as unhealthy and halt the compactor.

## Checked

2026-11-03. Confirmed against the Thanos Compactor page (components/compact.md): downsampling passes (40 hours, 10 days), retention flags and defaults, delete-delay, halting and thanos_compact_halted, resources, vertical compaction and deduplication flags. Fixed: retention example now uses equal retention per level as the page recommends; persistent-label wording; sharding by selector.relabel-config. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
