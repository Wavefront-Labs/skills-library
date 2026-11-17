---
id: computing-software.systems-network-administration.restic.forget-keep-policy
name: forget-keep-policy
category: computing-software
field: systems-network-administration
product: restic
tags: [restic, forget, retention, keep-daily, keep-within, policy, prune]
level: practitioner
status: docs-checked
description: "Apply a restic retention policy with forget --keep-last, --keep-daily and --keep-within options, preview with --dry-run, and add --prune."
sources:
  - https://restic.readthedocs.io/en/stable/060_forget.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Retention with forget

Remove a single snapshot with `restic forget <ID>`. For a policy:

```
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 12 --dry-run
restic forget --keep-daily 7 --keep-weekly 4 --keep-monthly 12 --prune
```

`--dry-run` prints what would be removed without removing anything. Removing snapshots takes two steps, forget and
then prune; `--prune` runs prune automatically if any snapshots were actually removed. Snapshot data stays in the
repository until prune runs.

## Options

- `--keep-last n`: keep the n most recent snapshots
- `--keep-hourly`, `--keep-daily`, `--keep-weekly`, `--keep-monthly`, `--keep-yearly n`: for the last `n` periods that have one or more snapshots, keep only the most recent snapshot of each
- `--keep-within duration`, e.g. `2y5m7d3h` (years, months, days, hours), keeps all snapshots within that duration of the latest snapshot
- `--keep-within-hourly|daily|weekly|monthly|yearly duration`: keep the hourly, daily, ... snapshots made within the duration of the latest snapshot (`1w` is not a recognised duration; use `7d`)
- `--keep-tag`: keep snapshots matching at least one tag list
- `unlimited` is read as "keep all" for the calendar options

## How rules combine

A snapshot is kept if it matches any one `--keep-*` option (the results are ORed). Calendar options work on natural
boundaries (weeks run Monday 00:00 to Sunday 23:59), not time relative to when forget runs. Duration options ignore
snapshots with a timestamp in the future, so those are not removed. `--keep-last 0` is an empty policy and restic
refuses to act on it. If there are not enough snapshots for a duration option, the oldest snapshot is also kept and
marked as oldest in the output.

Use `--dry-run` after changing a policy. Prune locks the repository so backups cannot complete meanwhile, and it is
advisable to run `restic check` afterwards.

## Checked
Compared with the "Removing backup snapshots" page: all `--keep-*` options and their meanings, the duration format,
natural time boundaries, `unlimited`, future timestamps, oldest-kept note, empty-policy refusal, `--dry-run` and
`--prune`. Reworded: the `--prune` and "oldest kept" notes to match the page.
Nothing was removed.
Method: docs-only read of cited pages, 2026-11-08
