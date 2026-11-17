---
id: computing-software.cloud-infrastructure-engineering.thanos.sidecar-upload-compacted-blocks
name: sidecar-upload-compacted-blocks
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-sidecar, shipper, upload-compacted, migration]
level: advanced
status: docs-checked
description: "Migrate historical Prometheus data to object storage with --shipper.upload-compacted."
sources: ["https://thanos.io/tip/components/sidecar.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Sidecar: uploading compacted blocks

To keep history when moving from plain Prometheus to Thanos, start the sidecar with `--shipper.upload-compacted`. It also uploads blocks Prometheus already compacted; a `compaction.level` greater than 1 in a block's `meta.json` indicates that.

For this, Prometheus local compaction must be disabled by pinning block durations:

```
--storage.tsdb.min-block-duration=2h
--storage.tsdb.max-block-duration=2h
```

The flag lives separately because of the compactor singleton rule: compacted blocks must reach the bucket before anything else, and uploading both compacted and non-compacted blocks from a sidecar while a Compactor runs can cause trouble.

Related flag: `--shipper.upload-concurrency` (default 0) sets goroutines used to upload block files.

## Checked

2026-11-03. Confirmed against the Thanos Sidecar page (components/sidecar.md) and the Thanos troubleshooting page: Store API over remote-read, 2h upload, block-duration requirement for upload, reloader flags, HTTP client config, upload-compacted, defaults. Fixed: the 2h fixed-block requirement applies to sidecar upload only. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
