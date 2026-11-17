---
id: computing-software.cloud-infrastructure-engineering.thanos.compactor-overview
name: compactor-overview
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-compact, compactor, singleton, block-compaction]
level: intro
status: docs-checked
description: "What thanos compact does to bucket data and why only one instance may run per bucket stream."
sources: ["https://thanos.io/tip/components/compact.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Compactor overview

`thanos compact` applies Prometheus 2.0 compaction to blocks in object storage and also downsamples and enforces retention. It is not concurrency safe and must be deployed as a singleton against a bucket.

Run it as a long-lived service or a one-shot:

```
thanos compact \
  --data-dir /path/to/compact \
  --objstore.config-file bucket.yml \
  --wait
```

With `--wait`, runs repeat every `--wait-interval` (default 5m). Background cleanup of partial uploads and blocks with deletion marks repeats every `--compact.cleanup-interval=5m` (0s only cleans at the end of an iteration).

Compaction reduces block count and index size, because series usually outlive the 2h minimum block.

**Concurrency flags** (all default to 1): `--compact.concurrency`, `--compact.blocks-fetch-concurrency`, `--downsample.concurrency`, `--block-files-concurrency`.

`--consistency-delay=30m` is the minimum age of fresh non-compacted blocks before they are processed.

## Checked

2026-11-03. Confirmed against the Thanos Compactor page (components/compact.md): downsampling passes (40 hours, 10 days), retention flags and defaults, delete-delay, halting and thanos_compact_halted, resources, vertical compaction and deduplication flags. Fixed: retention example now uses equal retention per level as the page recommends; persistent-label wording; sharding by selector.relabel-config. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
