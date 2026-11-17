---
id: computing-software.systems-network-administration.rclone.rclone-sync-safety-flags
name: rclone-sync-safety-flags
category: computing-software
field: systems-network-administration
product: rclone
tags: [sync, dry-run, backup-dir, max-delete, delete-before, track-renames, immutable]
level: practitioner
status: docs-checked
description: "Flags that make rclone sync and copy safer: dry-run, interactive, backup-dir, suffix, max-delete, delete timing and rename tracking."
sources: ["https://rclone.org/docs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`sync` makes the destination match the source and can delete files, so rehearse first.

```console
rclone sync -i /path/to/src remote:dst
rclone sync --dry-run /path/to/src remote:dst -vv
```

`-i/--interactive` asks before each action; `-n/--dry-run` prints what would change. Test filters with `rclone ls` or a dry run.

## Keep what would be overwritten

`--backup-dir remote:dir` moves files that would be overwritten or deleted into that directory, which must be on the same remote and not overlap the destination. Add `--suffix .bak` to rename them, and `--suffix-keep-extension` keeps the extension last.

## Limit blast radius

`--max-delete N` stops the run if more than N files would be deleted; `--max-delete-size` limits by bytes. `--max-transfer`, `--max-duration` and `--cutoff-mode HARD|SOFT|CAUTIOUS` bound transfer volume and runtime. `--immutable` errors if a source file differs from an existing destination file instead of overwriting. `--ignore-existing` skips files already on the destination.

## Delete timing

`--delete-before` deletes extraneous destination files first (two passes). `--delete-during` deletes while transferring and is the fastest with the least memory. `--delete-after` is the default: deletions are collected during the copy pass and run only after it succeeds, which is the safest, and if there were earlier errors you see "not deleting files as there were IO errors". Deleting after holds the list in memory.

## Rename tracking

By default a locally renamed file is deleted and re-uploaded on the remote. `--track-renames` matches source-only and destination-only objects and renames server-side. It needs a destination with server-side copy or move, a compatible hash for the default `hash` strategy, is incompatible with `--no-traverse` and `--delete-before` (it selects delete-after), and uses extra memory. `--track-renames-strategy` takes `modtime`, `hash`, `leaf` and `size` (always on); `modtime` or `leaf` make it usable with encrypted destinations, where `hash` is not supported.

Comparison options: `--size-only`, `-c/--checksum`, `-I/--ignore-times`, `-u/--update` and `--modify-window`.

## Checked

2026-11-04: flags, defaults, option names and behaviour confirmed against the rclone.org documentation pages cited in sources (and the matching docs source on GitHub where the rendered page was cut off).

Method: documentation only; no commands were run.
