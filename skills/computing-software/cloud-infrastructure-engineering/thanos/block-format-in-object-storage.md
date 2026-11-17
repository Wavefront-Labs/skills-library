---
id: computing-software.cloud-infrastructure-engineering.thanos.block-format-in-object-storage
name: block-format-in-object-storage
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-blocks, meta-json, tsdb-block-layout, deletion-mark]
level: advanced
status: docs-checked
description: "Read the layout of a Thanos block directory in object storage and what meta.json records."
sources: ["https://thanos.io/tip/thanos/storage.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Block format in object storage

Thanos stores native Prometheus TSDB blocks. A block is a directory (prefix) named by ULID, such as `01ARZ3NDEKTSV4RRFFQ69G5FAV`, holding series for a time span (for example 2h) from one source.

Files inside:
- `chunks/` with numbered segment files (`000001`, `000002`, ...; maximum 512MiB per segment file)
- `index`
- `meta.json`
- optional `deletion-mark.json`
- optional `no-compact-mark.json`

All files are strictly immutable. Modification (rewrite, deletion, compaction) creates a new block and removes the old one with a delay. Unknown files in the directory are ignored on read but may be removed on delete.

`meta.json` (currently version v1 for both the TSDB and Thanos sections) records the block ULID, `minTime`/`maxTime`, `stats.numSeries`, `compaction.level`, `compaction.sources` and parents, and the Thanos section with external labels (`labels`), `thanos.downsample.resolution` (0 means no downsampling) and source.

## Checked

2026-11-03. Confirmed against the Thanos storage page (thanos/storage.md): block layout, immutability, meta.json fields, 512MiB chunk segment limit. Removed: closing 'Verify' tips and other statements the page does not state.

Method: documentation only; no commands were run.
