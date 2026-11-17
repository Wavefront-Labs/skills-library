---
id: computing-software.systems-network-administration.backup-and-recovery.restic-snapshots-find-and-diff
name: restic-snapshots-find-and-diff
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [restic-snapshots, restic-diff, restic, restic-find, restic-ls, backup-browsing]
level: practitioner
status: docs-checked
description: "List, filter, search and compare restic snapshots: snapshots filters and grouping, ls, find across snapshots, diff between snapshots, stats, and JSON output for scripts."
sources:
  - https://restic.readthedocs.io/en/stable/045_working_with_repos.html
  - https://restic.readthedocs.io/en/stable/manual_rest.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Working with restic snapshots

**Goal:** answer "which backup has the file I need, and what changed?" quickly.

## List and filter
```sh
restic snapshots                                  # all
restic snapshots --host web01 --tag daily --path /etc
restic snapshots --latest 3 --group-by host,paths # last 3 per host and path set
restic snapshots --compact                        # compact table output; --json for scripts
```
Filters (`--host`, `--tag`, `--path`) work the same on `forget`, `restore`, `ls`, `find`, `copy`, `stats`, and `latest` resolves within the filter: `restic restore latest --host web01 --path /etc`.

## Browse one snapshot
```sh
restic ls latest /etc/nginx                 # list contents
restic ls --long 4f2a1c9b /var/www | head
restic dump latest /etc/fstab               # print a single file to stdout
restic dump latest /etc > etc.tar           # dump a directory as tar
```

## Find across snapshots
```sh
restic find '*.conf' --path /etc            # pattern match, shows each snapshot containing it
restic find --snapshot 4f2a1c9b nginx.conf
restic find --newest 2026-10-01 --oldest 2026-09-25 'report*.xlsx'
restic find --blob <id>                     # also --tree <id> or --pack <id>; with --show-pack-id (troubleshooting)
```

## Diff
```sh
restic diff 4f2a1c9b 8d0e33aa               # + added, - removed, M content modified, T type change, U metadata updated, ? bitrot
restic diff --metadata 4f2a1c9b 8d0e33aa    # print changes in metadata
```
The final summary shows added and removed bytes; use it to explain sudden repository growth. `snapshotID:subfolder` limits the comparison to a subtree.

## Size
`restic stats latest` (default mode restore-size), `restic stats --mode raw-data` (data actually stored); modes are restore-size, files-by-contents, blobs-per-file and raw-data.

## Gotchas
- `--path` selects snapshots whose recorded paths include the given absolute path (all given paths must be included); a snapshot of `/` is not matched by `--path /etc`.
- `find` sorts snapshots youngest to oldest by default (`--reverse` flips it); narrow it with `--host`, `--path`, `--snapshot` or dates.
- Metadata comparison will likely not work for backups created with `--ignore-inode` or `--ignore-ctime`.

## Verify
For a known recent change, `restic diff` between the two latest snapshots shows it, and `restic dump` returns the expected old version.

## Checked

2026-10-26. Documentation checked: restic/restic doc/ sources on master (last commit 2026-10-18; latest release v0.19.1) and the generated man pages in doc/man. Confirmed: snapshots flags (--latest, --group-by, --compact), shared --host/--path/--tag filters, ls --long, dump tar default, find flags (--snapshot, --newest, --oldest, --blob, --tree, --pack, --show-pack-id, default sort), diff status letters and --metadata, stats modes (man pages, 045_working_with_repos). Removed the jq pipeline and unconfirmed speed claims.

Method: documentation only; no commands were run.
