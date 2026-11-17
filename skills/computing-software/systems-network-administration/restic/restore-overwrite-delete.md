---
id: computing-software.systems-network-administration.restic.restore-overwrite-delete
name: restore-overwrite-delete
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, restore, overwrite, delete, in-place, dry-run]
level: advanced
status: docs-checked
description: "Restore in place safely with restic restore --overwrite modes and --delete, previewing every change with --dry-run and -vv first."
sources:
  - https://restic.readthedocs.io/en/stable/050_restore.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# In-place restores

Restoring over the live directory can overwrite or delete data, so control it with explicit options.

## Overwrite behaviour

`--overwrite` takes:

- `always` (default): verifies existing file content and restores only mismatching parts; updates metadata of all files
- `if-changed`: like `always`, but treats files with matching size and mtime as up to date; if they differ, the full content is verified
- `if-newer`: overwrite only if the snapshot's file has a newer mtime
- `never`: never overwrite existing files

## Delete extra files

`--delete` removes files in the target that are not in the snapshot. When used with `--target`, it requires `--include` or `--exclude`, so you cannot wipe a whole directory by accident.

## Preview first

```
restic restore latest --target /path/to/data --overwrite if-changed --delete --include /path/to/data/project --dry-run -vv
```

`--dry-run` with `--verbose=2` shows each file as `unchanged`, `updated` or `restored` (and deletions). The docs warn to run `--dry-run -vv` before using `--delete`.

Dry runs skip content comparison when you use `--overwrite never` or a non-existent target, since there is nothing to compare, so they run faster.

## Safer pattern

An interrupted in-place restore can leave files partially restored, so the docs advise taking a current backup before restoring a different snapshot. `--delete` with `--include` or `--exclude` only deletes files matched by those patterns, and it also allows overwriting a non-empty directory when the snapshot has a file of the same name.

## Checked

2026-11-03. Confirmed in the restic docs page Restoring from backup (Restoring in-place, Deleting files not in snapshot, Dry runs): the four `--overwrite` modes and their meaning, `--delete` rules and the `--dry-run -vv` warning, the unchanged/updated/restored labels, the checks skipped with `--overwrite never` or a missing target. Removed: the restore-to-fresh-directory advice (not in the docs).

Method: documentation only; no commands were run.
