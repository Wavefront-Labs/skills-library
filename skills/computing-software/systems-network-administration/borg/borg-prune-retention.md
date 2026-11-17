---
id: computing-software.systems-network-administration.borg.borg-prune-retention
name: borg-prune-retention
category: computing-software
field: systems-network-administration
product: borg
tags: [borg, borg-prune, retention, keep-daily, keep-weekly, keep-monthly, keep-within, gfs, glob-archives, compact]
level: practitioner
status: docs-checked
description: "Apply a Borg retention policy with borg prune keep-daily, weekly, monthly, yearly and keep-within rules, dry-run first, then compact to actually free space."
sources: ["https://borgbackup.readthedocs.io/en/stable/usage/prune.html", "https://borgbackup.readthedocs.io/en/stable/usage/compact.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Borg prune

`borg prune` deletes every archive that no retention rule keeps. It frees no disk space until `borg compact` runs. Always dry-run first:

```
borg prune -v --list --dry-run --keep-daily=7 --keep-weekly=4 /path/to/repo
borg prune -v --list --keep-within=10d --keep-weekly=4 --keep-monthly=-1 /path/to/repo
borg compact /path/to/repo
```

Rules apply from secondly to yearly (`--keep-last/secondly`, `minutely`, `-H hourly`, `-d daily`, `-w weekly`, `-m monthly`, `--keep-13weekly`, `--keep-3monthly`, `-y yearly`). An archive kept by an earlier rule does not count toward later ones. A negative count means unlimited. Weeks run Monday to Sunday using each backup's local start time. `--keep-within` takes a number plus H, d, w, m or y (`1m` is 31 days), and those archives do not count toward other rules. Since 1.2.0 the oldest archive is kept when a rule cannot meet its target.

With a shared repository, restrict each run to one data set: `--glob-archives '{hostname}-*'` (note `foo*` also matches `foobar`). Checkpoint archives do not count toward limits and old ones are removed, except the latest archive if it is a checkpoint. `--stats` and `--dry-run` are mutually exclusive. `borg compact --threshold` (default 10 percent) sets how much a segment must save to be rewritten.

## Checked

2026-11-03. Confirmed against the Borg 1.4.5 documentation (usage/prune and usage/compact): keep options and short flags, rule order, keep-within units, checkpoint handling, 1.2.0 oldest-archive rule, compact threshold default. Removed: nothing.

Method: documentation only; no commands were run.
