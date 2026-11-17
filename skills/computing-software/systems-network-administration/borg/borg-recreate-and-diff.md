---
id: computing-software.systems-network-administration.borg.borg-recreate-and-diff
name: borg-recreate-and-diff
category: computing-software
field: systems-network-administration
product: borg
tags: [borg, borg-recreate, borg-diff, recompress, rechunk, json-lines, sort-by, archive-comparison]
level: advanced
status: docs-checked
description: "Rewrite existing Borg archives with borg recreate (recompress, rechunk, drop paths, comments) and compare two archives with borg diff."
sources: ["https://borgbackup.readthedocs.io/en/stable/usage/recreate.html", "https://borgbackup.readthedocs.io/en/stable/usage/diff.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Borg recreate and diff

`borg recreate` rebuilds archives in place. The docs warn it can lose data if used wrongly: run `--dry-run --verbose --list` first. Exclude options and PATHs behave like `create` but match only items already in the archive, using relative paths. Space is freed only after `borg compact`.

```
borg recreate /path/to/repo --exclude home/user/Pictures/private
borg recreate /path/to/repo::archive --recompress --compression zlib,9
borg recreate /path/to/repo --chunker-params default --progress
borg recreate --comment "new comment" /path/to/repo::archive
```

`--recompress` modes: `if-different` (default when the flag is given), `always` (change level only), `never` (same as omitting). `--target NAME` writes a new archive and keeps the original (single archive only). While running, a temporary `<ARCHIVE>.recreate` exists. Rechunking or recompressing can need at least the deduplicated size of the archives as extra space. Rechunking drops `chunks_healthy`, so earlier `check --repair` healing is no longer possible.

`borg diff REPO::ARCHIVE1 ARCHIVE2` compares two archives of one repository: content bytes added/removed, mode/user/group changes, added and removed items. For Borg 1.1+ archives with equal chunker params it compares chunk IDs only (fast); for older ones pass `--same-chunker-params` if you know they match. `--content-only`, `--json-lines`, `--sort-by` fields such as `path`, `size_diff` (prefix `>` for descending), `-e/--exclude`.

## Checked

2026-11-03. Confirmed against the Borg 1.4.5 documentation (usage/recreate and usage/diff): recreate options, --recompress modes, --target, .recreate archive, chunks_healthy note, diff comparison, sort fields. Removed: nothing.

Method: documentation only; no commands were run.
