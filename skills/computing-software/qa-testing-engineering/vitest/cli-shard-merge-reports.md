---
id: computing-software.qa-testing-engineering.vitest.cli-shard-merge-reports
name: cli-shard-merge-reports
category: computing-software
field: qa-testing-engineering
product: vitest
tags: [shard, merge-reports, blob-reporter-shard, vitest-blob-label]
level: practitioner
status: docs-checked
description: "Split a Vitest run across CI machines with --shard=index/count and combine blob reports afterwards with --merge-reports and any other reporter."
sources:
  - https://raw.githubusercontent.com/vitest-dev/vitest/main/docs/guide/cli.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`--shard=<index>/<count>` divides all tests into `count` equal parts and runs only part `index`:

```sh
vitest run --shard=1/3
vitest run --shard=2/3
vitest run --shard=3/3
```

It cannot be combined with `--watch`, which is on by default in development.

If `--reporter=blob` is used without an output file, the default path includes the shard config and the blob label (from `VITEST_BLOB_LABEL` or the blob reporter `label` option), which avoids collisions with other Vitest processes.

`--merge-reports` merges every blob report in a folder (`.vitest/blob/` by default) and accepts any reporter except `blob`:

```sh
vitest --merge-reports --reporter=junit
```

## Checked

2026-11-04. Confirmed against guide/cli.md, sections shard and merge-reports. Removed a closing line about a typical CI job layout, which the page does not state.

Method: documentation only; no commands were run.
