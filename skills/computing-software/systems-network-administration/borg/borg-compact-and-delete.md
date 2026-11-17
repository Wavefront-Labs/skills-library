---
id: computing-software.systems-network-administration.borg.borg-compact-and-delete
name: borg-compact-and-delete
category: computing-software
field: systems-network-administration
product: borg
tags: [borg, borg-compact, borg-delete, free-space, threshold, cleanup-commits, segments]
level: practitioner
status: docs-checked
description: "Free repository space after deleting Borg archives: borg delete options, whole-repository deletion confirmation, and borg compact threshold and cleanup-commits."
sources: ["https://borgbackup.readthedocs.io/en/stable/usage/delete.html", "https://borgbackup.readthedocs.io/en/stable/usage/compact.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Borg delete and compact

`borg delete REPO::ARCHIVE` removes one archive; `borg delete REPO` removes the whole repository after you type `YES` (or set `BORG_DELETE_I_KNOW_WHAT_I_AM_DOING=YES`), along with its security info and local cache. Deleting archives does not free disk space; only `borg compact` does.

```
borg delete /path/to/repo::Monday
borg delete --glob-archives '{hostname}-*' /path/to/repo
borg delete --list --dry-run -a '*-May-*' /path/to/repo   # preview
borg compact /path/to/repo
```

Delete options: `-n/--dry-run`, `--list`, `-s/--stats` (the "Deleted data" deduplicated size is the shrink), `--quick-stats`, `--cache-only` (drop just the local cache), `--keep-security-info`, `--force` (corrupted archives; `--force --force` if needed), archive filters `-a`, `--sort-by`, `--first N`, `--last N`. Stats and dry-run cannot be combined.

`borg compact` rewrites segments; it needs no key and can run on the server. Run it regularly, not after every command. `--threshold PERCENT` (default 10): 0 compacts anything that saves space (slowest), 1 is nearly as good and much faster, 100 compacts nothing. `-n` dry-run, `--progress` helps on many segments. After upgrading the server from 1.1 to 1.2+, run `borg compact --cleanup-commits` once per repository to remove the 17-byte commit-only segments.

## Checked

2026-11-03. Confirmed against the Borg 1.4.5 documentation (usage/delete and usage/compact): delete options, whole-repo delete behaviour, compact --threshold default 10 and --cleanup-commits, BORG_DELETE_I_KNOW_WHAT_I_AM_DOING (General page). Removed: nothing.

Method: documentation only; no commands were run.
