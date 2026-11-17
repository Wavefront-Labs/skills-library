---
id: computing-software.systems-network-administration.rclone.rclone-bisync-conflicts-compare-and-recovery
name: rclone-bisync-conflicts-compare-and-recovery
category: computing-software
field: systems-network-administration
product: rclone
tags: [bisync, conflict-resolve, compare, resilient, recover, filters-file, backup-dir]
level: advanced
status: docs-checked
description: "Tune bisync comparison, conflict resolution, error recovery, backup directories and the filters-file hash check."
sources: ["https://rclone.org/bisync/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
## Comparison

`--compare` takes a comma list of `size`, `modtime`, `checksum` (default `size,modtime`). Checksums on backends where hashes are slow can be skipped with `--no-slow-hash`, limited to sync calls with `--slow-hash-sync-only`, or computed by downloading with `--download-hash` (slow, uses data). `--ignore-listing-checksum` stops using checksums in listings.

## Conflicts

`--conflict-resolve` picks a winner automatically: `none` (default), `path1`, `path2`, `newer`, `older`, `larger`, `smaller`. `--conflict-loser` decides what happens to the loser: `num` (numbered, default), `pathname`, or `delete`. When there is no winner both files are renamed. `--conflict-suffix` sets the suffix, or two comma-separated suffixes for Path1 and Path2.

## Error handling and recovery

After a serious problem bisync goes into a safe state and later runs fail until you run `--resync`. `--resilient` lets future runs retry after less serious errors, with `--retries` and `--retries-sleep`. `--recover` recovers from interruptions without a full resync. `--no-cleanup` retains working files for troubleshooting.

## Backups and filters

`--backup-dir1` and `--backup-dir2` keep overwritten or deleted files; each must be a non-overlapping path on the same remote as its side. With `--filters-file`, bisync stores an MD5 of the file in a `.md5` file beside it; if the filters change, the next run aborts with a critical error and demands `--resync`, because newly excluded files would otherwise look deleted and be removed for real. `--check-sync` controls the final listing comparison (`true`, `false`, `only`).

## Gotchas from the docs

Bisync uses `--fast-list` by default where supported; add `--disable ListR` to avoid it. Google Docs have unknown size, so use `--drive-skip-gdocs`.

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off). Removed or corrected claims the pages did not confirm.

Method: documentation only; no commands were run.
