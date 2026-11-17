---
id: computing-software.cloud-infrastructure-engineering.thanos.tools-bucket-inspect-and-ls
name: tools-bucket-inspect-and-ls
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-tools, bucket-ls, bucket-inspect, bucket-web]
level: intro
status: docs-checked
description: "Inspect a Thanos bucket with tools bucket ls, inspect and web."
sources: ["https://thanos.io/tip/components/tools.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# tools bucket: ls, inspect and web

`thanos tools bucket` is a set of troubleshooting commands for object storage, normally run standalone. Each takes `--objstore.config-file`.

- `thanos tools bucket ls -o json --objstore.config-file=bucket.yml` lists all blocks, with `-o json` for scripting.
- `thanos tools bucket inspect -l environment=\"prod\" --objstore.config-file=bucket.yml` prints a detailed ASCII table of blocks, optionally filtered by external label with `-l`.
- `thanos tools bucket web --objstore.config-file=bucket.yml` starts a local interactive web UI of the bucket's blocks, refreshed periodically.

For a UI backed by a long-running service, the compactor also has a block viewer, with `--block-viewer.global.sync-block-interval=1m` and `--block-viewer.global.sync-block-timeout=5m`, and `--bucket-web-label` choosing the external label used as group title.

**Verify.** `inspect` prints an ASCII table of the blocks in the bucket.

## Checked

2026-11-08. Read the Bucket section intro, Bucket Web, Bucket ls and Bucket inspect sections of the raw Thanos tools page (docs/components/tools.md), and the block-viewer and bucket-web-label flag help in the Compactor page (docs/components/compact.md). Partial read: the long flag lists of each subcommand were skimmed only. Reworded the Verify line to what the page states.

Method: documentation only; no commands were run.
