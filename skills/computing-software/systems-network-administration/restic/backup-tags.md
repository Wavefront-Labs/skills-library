---
id: computing-software.systems-network-administration.restic.backup-tags
name: backup-tags
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, tags, tag, snapshots, filtering, retention]
level: practitioner
status: docs-checked
description: "Label restic snapshots with --tag, filter by tag in find, forget and copy, and change tags on existing snapshots."
sources:
  - https://restic.readthedocs.io/en/stable/040_backup.html
  - https://restic.readthedocs.io/en/stable/060_forget.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tags

Add tags when you create a snapshot:

```
restic -r /srv/restic-repo backup --tag nightly --tag db /path/to/data
```

Tags let you separate kinds of backup that share a host and paths, then apply different retention.

## Filtering

Several commands take `--tag`, including `find`, `forget`, `copy` and `rewrite` (check `restic help <command>` for the rest). The documented rules, shown for `forget`, `copy` and `find`, are:

- A comma-separated list means AND: `--tag foo,bar` needs both tags.
- Repeating the flag means OR: `--tag foo --tag bar` matches either.
- An empty tag `''` matches untagged snapshots.

## Retention by tag

```
restic forget --tag nightly --keep-daily 7
restic forget --keep-tag keep-forever --keep-daily 7
```

`--tag` restricts which snapshots the policy considers; `--keep-tag` protects snapshots from removal.

## Change tags later

The `tag` command modifies tags on existing snapshots (see `restic help tag` for its options). Its JSON output reports an old and a new snapshot ID, so a retagged snapshot gets a new ID.

## Checked

Checked 2026-11-08 against the restic Backing up (040_backup), Removing backup snapshots (060_forget), Working with repositories (045_working_with_repos) and Scripting (075_scripting) pages, all read in full. Confirmed: --tag on backup, AND within a comma list and OR across repeated flags for forget and copy, empty tag for untagged snapshots, --keep-tag, tag command, find accepting --tag, and old_snapshot_id/new_snapshot_id in the tag JSON output. Removed: the claim that snapshots and restore accept --tag and the repository original field, which the pages do not state.

Method: documentation only; no commands were run.
