---
id: computing-software.cloud-infrastructure-engineering.thanos.compactor-delete-delay-and-halt
name: compactor-delete-delay-and-halt
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-compact, delete-delay, halt-on-error, partial-uploads]
level: advanced
status: docs-checked
description: "Handle aborted partial uploads with --delete-delay and recognise a halted compactor."
sources: ["https://thanos.io/tip/components/compact.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Compactor delete delay and halting

**Aborted partial uploads.** If a compactor crashes while uploading a compacted block, compaction restarts with a new block ID and the partial upload is never retried. `--delete-delay=48h` (default) makes the compactor delete directories without `meta.json` only after that age. The docs say this value has to be smaller than the upload duration and consistency delay. Separately, with a non-zero `--delete-delay` blocks are first marked for deletion and removed after the delay; with 0 they are deleted straight away, which can cause query failures if a store gateway still has the block loaded.

**Halting.** On certain data failures the compactor halts rather than crashing: it stays running, does nothing, and sets metric `thanos_compact_halted` to 1. The reason is that retrying a heavy compaction is pointless when, for example, there is already an overlapped state in the bucket.

The hidden flag `--no-debug.halt-on-error` makes it exit instead on a halt error.

Two blocks with the same external labels that overlap in time cause a halt.

## Checked

2026-11-03. Confirmed against the Thanos Compactor page (components/compact.md): downsampling passes (40 hours, 10 days), retention flags and defaults, delete-delay, halting and thanos_compact_halted, resources, vertical compaction and deduplication flags. Fixed: retention example now uses equal retention per level as the page recommends; persistent-label wording; sharding by selector.relabel-config. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
