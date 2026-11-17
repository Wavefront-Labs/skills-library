---
id: computing-software.systems-network-administration.restic.rewrite-snapshots
name: rewrite-snapshots
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, rewrite, exclude, include, new-host, new-time, repair]
level: advanced
status: docs-checked
description: "Remove files from existing restic snapshots or change their host and timestamp with restic rewrite, with dry runs first."
sources:
  - https://restic.readthedocs.io/en/stable/045_working_with_repos.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rewriting snapshots

`rewrite` removes unwanted files from existing snapshots (or changes snapshot metadata) by saving new snapshots,
instead of deleting the snapshots and re-running backups.

```
restic rewrite --exclude /path/to/secret.txt --dry-run <snapshotID>
```

Without snapshot IDs it processes all snapshots; you can also restrict it to a subset using the same filters as
`copy` (`--host`, `--path`, `--tag`).

## Filters

- `--exclude`, `--exclude-file`, `--iexclude`, `--iexclude-file` behave as for `backup`.
- `--include`, `--include-file`, `--iinclude`, `--iinclude-file` reduce snapshots to the files you want, e.g.
  `--iinclude "*.jpg" --iinclude "*.png"`.

## Metadata options

- `--new-host <name>` changes the recorded hostname.
- `--new-time "<timestamp>"` changes the backup time, e.g. `--new-time "1999-01-01 11:11:11"`.
- `--snapshot-summary` attaches summary data (only TotalFilesProcessed and TotalBytesProcessed) to snapshots that
  lack it.

## Replace or keep originals

By default rewrite keeps the original snapshots and creates new ones for each modified snapshot, tagged `rewrite`.
`--forget` removes the originals immediately and adds no tag to the new snapshots.

## Workflow

1. Run with `--dry-run`, which simulates the rewrite and prints the actions it would perform without modifying the
   repository.
2. Run for real, optionally with `--forget`.
3. Run `restic prune`. `--forget` removes only the snapshots, not the data, so unreferenced data remains until prune
   runs.

If rewrite fails with `cannot encode tree at "[...]" without losing information` (a snapshot made by a newer restic
or third-party tool), convert the snapshot with `restic repair snapshots <snapshotID>`.

## Checked
Compared with the "Working with repositories" page, sections "Removing files from snapshots" and "Modifying metadata
of snapshots": filter options, include variants, `--new-host`, `--new-time`, `--snapshot-summary`, the `rewrite` tag,
`--forget`, `--dry-run`, prune requirement and the repair note. Removed: the claim that repair snapshots is for
snapshots "damaged by missing data" and the `restic snapshots` confirmation step (not on the page).
Method: docs-only read of cited pages, 2026-11-08
