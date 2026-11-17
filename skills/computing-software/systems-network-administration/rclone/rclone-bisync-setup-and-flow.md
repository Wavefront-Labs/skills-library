---
id: computing-software.systems-network-administration.rclone.rclone-bisync-setup-and-flow
name: rclone-bisync-setup-and-flow
category: computing-software
field: systems-network-administration
product: rclone
tags: [bisync, resync, bidirectional-sync, check-access, lock-file, cron]
level: advanced
status: docs-checked
description: "Set up and run rclone bisync: the required first resync, listing flow, change rules, safety checks and exit codes."
sources: ["https://rclone.org/bisync/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Bisync is an advanced command; read the Limitations section before using it. It keeps listings of both paths from the previous run, finds new, newer, older and deleted files on each side, and propagates them. State lives in a working directory (the `rclone/bisync` folder under the user cache directory); it must be writable.

## First run

Run once with `--resync`, ideally with `--dry-run` first, then run again without `--resync`. Leaving `--resync` on later runs defeats the safety design.

```console
rclone bisync remote1:path1 remote2:path2 --create-empty-src-dirs --compare size,modtime,checksum --slow-hash-sync-only --resilient -MvP --drive-skip-gdocs --fix-case --resync --dry-run
```

Resync copies Path2-only files to Path1 and then Path1 to Path2, roughly `rclone copy Path2 Path1 --ignore-existing` then `rclone copy Path1 Path2`. By default Path1 wins when both differ; `--resync-mode` can prefer path2, newer, older, larger or smaller. Both base directories must exist. On later runs an empty listing on either side aborts with "Cannot sync to an empty directory", guarding against a failed listing being read as mass deletion.

## Change rules

New or newer on one side is copied to the other; unchanged on one side and deleted on the other is deleted; changed on both sides is a conflict handled by `--conflict-resolve`, `--conflict-loser` and `--conflict-suffix`, which by default renames both copies `.conflict1`, `.conflict2`.

## Safety

- `--check-access` requires matching `RCLONE_TEST` files (or `--check-filename`) on both sides; create them first with `rclone touch`, because `--resync --check-access` will not create them.
- `--max-delete PERCENT` (default 50) aborts on excessive deletes; `--force` bypasses it.
- A lock file named for the path pair blocks overlapping runs, so cron is safe; `--max-lock` (minimum 2m) expires stale locks, and after a crash you can delete the lock file by hand.

Exit codes: 0 success, 1 retryable failure, 2 usage error, 7 critical abort needing `--resync`.

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off).

Method: documentation only; no commands were run.
