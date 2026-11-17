---
id: computing-software.cloud-infrastructure-engineering.thanos.compactor-resources
name: compactor-resources
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-compact, compactor-sizing, memory, disk]
level: practitioner
status: docs-checked
description: "Size CPU, memory, network and disk for the Thanos compactor from the documented rules."
sources: ["https://thanos.io/tip/components/compact.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Compactor resource sizing

- **CPU:** give it as many cores as `--compact.concurrency`.
- **Memory:** peak usage equals Prometheus compaction, per source block: 1/32 of all symbols, 1/32 of all posting offsets, plus a single series with all labels and chunks. Multiply by `--compact.concurrency` (default 1). Look at process or OS memory, not only Go heap, because compaction relies heavily on mmap outside Go runtime stats.
- **Network:** potentially the highest bandwidth of any component, as it downloads every block it compacts or downsamples and uploads results. Place it near the bucket's zone.
- **Disk:** for a medium bucket about 100GB is enough; multiply by `--compact.concurrency` as well. The worst case is room for two times the largest compaction range of smaller blocks (for example two weeks), because source blocks are downloaded and the result is written before uploading.

On-disk data is safe to delete between restarts and is the first thing to try for a crash-looping compactor; a persistent disk lets the bucket state cache survive restarts. The `--hash-func=SHA256` flag hashes produced files, which avoids downloading some files twice at some performance cost.

## Checked

2026-11-03. Confirmed against the Thanos Compactor page (components/compact.md): downsampling passes (40 hours, 10 days), retention flags and defaults, delete-delay, halting and thanos_compact_halted, resources, vertical compaction and deduplication flags. Fixed: retention example now uses equal retention per level as the page recommends; persistent-label wording; sharding by selector.relabel-config. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
