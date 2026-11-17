---
id: computing-software.systems-network-administration.restic.skip-unchanged-and-dry-run
name: skip-unchanged-and-dry-run
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, dry-run, skip-if-unchanged, backup, preview]
level: practitioner
status: docs-checked
description: "Preview a restic backup with --dry-run and avoid creating empty snapshots with --skip-if-unchanged."
sources:
  - https://restic.readthedocs.io/en/stable/040_backup.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dry runs and skipping unchanged snapshots

## Preview

```
restic -r /srv/restic-repo backup --dry-run --verbose=2 /path/to/data
```

`--dry-run` (`-n`) reports what would be done without writing to the repository. Combined with `--verbose` (twice,
or `--verbose=2`) it lists per-file changes such as "modified ... (9.110 KiB added)" and ends with the total that
would be added to the repository.

## Skip a snapshot when nothing changed

By default restic always creates a new snapshot even if nothing changed compared to the parent snapshot. To omit the
new snapshot in that case, add `--skip-if-unchanged`:

```
restic backup --skip-if-unchanged /path/to/data
```

With absolute paths as the source, changes to the metadata of the parent folders also count as a change: a backup of
/data/work creates a new snapshot if the metadata of /, /data or /data/work changes. To avoid that, run restic
from the corresponding folder and use relative paths, as in `cd /data/work && restic backup . --skip-if-unchanged`.
Switching between absolute and relative paths stops change detection from recognising unmodified files.

## Checked
Compared with the "Backing up" page, sections "Dry runs" and "Skip creating snapshots if unchanged": `--dry-run`/`-n`,
verbose listing, `--skip-if-unchanged` and the absolute-path caveat. Removed: the claims about testing exclude
patterns, retention counting, `--no-scan` and exit code 3 (not on the cited page).
Method: docs-only read of cited pages, 2026-11-08
