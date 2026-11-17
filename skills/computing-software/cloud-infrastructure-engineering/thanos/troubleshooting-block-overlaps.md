---
id: computing-software.cloud-infrastructure-engineering.thanos.troubleshooting-block-overlaps
name: troubleshooting-block-overlaps
category: computing-software
field: cloud-infrastructure-engineering
product: thanos
tags: [thanos-troubleshooting, overlapping-blocks, compactor-halt, ulid]
level: advanced
status: docs-checked
description: "Diagnose and resolve overlapping blocks in a Thanos bucket that halt the compactor."
sources: ["https://thanos.io/tip/operating/troubleshooting.md/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Troubleshooting block overlaps

Overlap means blocks with exactly the same external labels covering the same or overlapping time. Thanos is designed never to produce it, so there is no automatic repair.

**Effects.** Readers such as the Store Gateway handle it (overlapping samples are deduplicated). The compactor stops all activity: it halts or crashes with a metric and an error log, because it cannot compact or downsample.

**Reasons**
- Sidecar, ruler or receive older than 0.13.0 (transient upload errors).
- Same or missing external labels across several block producers.
- More than one compactor on a single stream, even briefly.
- Blocks uploaded manually.
- Eventually consistent block storage.

**Solutions**
- Upgrade sidecar, ruler and receive to 0.13.0 or later.
- If urgent, remove the overlap, or better, back up the block elsewhere (renaming the ULID to a non-ULID name hides it).
- Find who uploaded it: search sidecar and ruler logs for the ULID, check object storage access logs, and inspect `meta.json` to see the source.
- Fix the misconfiguration; if everything looks correct, open an issue.

**Verify.** `thanos tools bucket verify --issues=overlapped_blocks` (verify only, no repair) reports no overlap, and `thanos_compact_halted` returns to 0 once the compactor resumes.

## Checked

2026-11-08. Read in full the raw Thanos troubleshooting page (docs/operating/troubleshooting.md, Overlaps section) for the definition, effects, reasons and solutions; read the tools bucket verify section (docs/components/tools.md) for the overlapped_blocks issue and the Compactor page Halting section for thanos_compact_halted. Changed the Verify line to name the documented issue flag.

Method: documentation only; no commands were run.
