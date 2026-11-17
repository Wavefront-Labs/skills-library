---
id: computing-software.cloud-infrastructure-engineering.thanos.tools-bucket-rewrite
name: tools-bucket-rewrite
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-tools, bucket-rewrite, delete-series, change-log]
level: sme
status: docs-checked
description: "Delete or modify series in existing blocks with tools bucket rewrite, with dry-run and change log."
sources: ["https://thanos.io/tip/components/tools.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# tools bucket rewrite

`thanos tools bucket rewrite` rewrites chosen blocks while deleting or modifying series. It does a dry run by default; pass `--no-dry-run` to apply.

```
thanos tools bucket rewrite --no-dry-run \
  --id 01DN3SK96XDAEKRB1AN30AAW6E \
  --objstore.config "
type: FILESYSTEM
config:
  directory: /path/to/local/dir
" \
  --rewrite.to-delete-config "
- matchers: \"{__name__!~\\\".*total\\\"}\"
"
```

This example removes every series whose name does not end in `total` from a block in a local directory.

By default it also writes `change.log` to a temp directory; look for the log line `changelog will be available`.

**Limits.** Downsampled blocks (5m and 1h resolution) can only be rewritten by deleting whole series, meaning deletion requests without time intervals; deletions with intervals and relabeling would require re-encoding aggregated chunks.

Rewrite produces a new block. Deleting or marking the source block for deletion is the caller's job, otherwise the two overlap; `--delete-blocks` does it in non-dry-run mode. Turn the compactor off first: if it touches the same block, the result may only cause overlap. The procedure is irreversible after the delete delay, so back up blocks first.

**Verify.** Inspect the change log and the new block's `meta.json`, which has modified stats and a `thanos.rewrite` section with the deletion requests.

## Checked

2026-11-08. Read the Bucket Rewrite section of the raw Thanos tools page (docs/components/tools.md, lines 898-1013), including the --help text: dry-run default, --no-dry-run, change.log, downsampled-block limit, --delete-blocks, compactor warning. Removed the claim that the original is marked for deletion automatically (the help text says it is the caller's responsibility) and the numSeries check (not stated).

Method: documentation only; no commands were run.
