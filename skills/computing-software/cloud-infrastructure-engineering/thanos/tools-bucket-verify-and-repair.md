---
id: computing-software.cloud-infrastructure-engineering.thanos.tools-bucket-verify-and-repair
name: tools-bucket-verify-and-repair
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-tools, bucket-verify, repair, index-issues]
level: advanced
status: docs-checked
description: "Verify bucket blocks and optionally repair them while the compactor is disabled."
sources: ["https://thanos.io/tip/components/tools.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# tools bucket verify

`thanos tools bucket verify --objstore.config-file=bucket.yml` verifies blocks in the bucket and can optionally repair them.

With `--repair`, make sure the compactor job is disabled first.

Choose what to check with `--issues`: `overlapped_blocks` can only be verified; `index_known_issues` and `duplicated_compaction` can be verified and repaired. Depending on the issue, verify may need to download the blocks to disk. `--id` limits it to given blocks, and `--objstore-backup.config` names a bucket where repair logic backs up blocks before removal.

Related bucket commands:
- `tools bucket mark --id <ULID> ...` manually marks blocks for deletion; if the compactor is compacting exactly that block, the operation is potentially a no-op.
- `tools bucket replicate --objstore.config-file ... --objstore-to.config ...` copies between buckets, and only works with Thanos blocks whose `meta.json` carries Thanos metadata.
- `tools bucket upload-blocks` uploads locally created blocks to the bucket.

**Verify.** Run verify without `--repair` first and read the findings.

## Checked

2026-11-08. Read the Bucket Verify, Bucket mark, Bucket replicate and Bucket Upload Blocks headings and notes of the raw Thanos tools page (docs/components/tools.md), including the verify --help text. Removed the claim about the compactor singleton rule and the use-when advice, which the page does not state. Partial read: upload-blocks flags not read.

Method: documentation only; no commands were run.
