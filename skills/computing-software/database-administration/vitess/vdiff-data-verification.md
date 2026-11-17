---
id: computing-software.database-administration.vitess.vdiff-data-verification
name: vdiff-data-verification
category: computing-software
field: database-administration
product: vitess
tags: [vdiff, data-verification, vreplication, primary-key, resume, update-table-stats]
level: practitioner
status: docs-checked
description: "Verify MoveTables or Reshard data with VDiff: create, show, resume, stop and delete actions, primary key requirements, collation caveat and progress estimates."
sources:
  - https://vitess.io/docs/25.0/reference/vreplication/vdiff/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VDiff compares every table of a workflow row by row between source and target keyspaces and reports missing, extra and unmatched rows. Run it before `SwitchTraffic` and `complete`.

Actions (all via `vtctldclient VDiff --target-keyspace <ks> --workflow <wf> <action>`):
- `create`: schedules a VDiff on each target shard's primary and returns a UUID (generated if not given).
- `show <uuid|last|all>`: summary with State, RowsCompared, HasMismatch, StartedAt, CompletedAt; add `--format=json` for more, including Progress with Percentage and ETA. `ShardSummaries` (State, LastError, and per-table TableStates with RowsCompared, MatchingRows, MismatchedRows, ExtraRowsSource, ExtraRowsTarget, HasMismatch) appear only with `--verbose` or on mismatch.
- `resume <uuid>`: continues a completed VDiff from the last primary key processed, enabling approximate rolling diffs (after the copy phase and again before SwitchTraffic).
- `stop <uuid>`: pauses, for example for off-hours; stopping a completed one is a no-op.
- `delete <uuid|all>`: idempotent; deleting a workflow deletes its VDiff data.

Cautions: tables without a primary key use a primary key equivalent (non-NULL unique index); with neither, every start or resume needs a full table scan and filesort, so define a PK. Results of `resume` are not guaranteed when source and target collations differ for a table. Progress uses approximate `information_schema` row counts that can be off by 50-60 percent; `create --update-table-stats` runs `ANALYZE TABLE` first to improve it.

## Checked

2026-11-08. Re-read the full VDiff page (v25.0). All actions, output fields, warnings and the progress-estimate note confirmed on the VDiff reference page.

Method: documentation only; no commands were run.
