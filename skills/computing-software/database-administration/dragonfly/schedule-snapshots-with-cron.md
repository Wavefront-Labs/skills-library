---
id: computing-software.database-administration.dragonfly.schedule-snapshots-with-cron
name: schedule-snapshots-with-cron
category: computing-software
field: database-administration
product: dragonfly
tags: [snapshot-cron, cron-schedule, save-schedule, backups, dragonfly]
level: practitioner
status: docs-checked
description: "Schedule automatic Dragonfly snapshots with the snapshot_cron flag, why it replaces deprecated save_schedule, and cron examples."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/managing-dragonfly/backups.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Dragonfly writes a backup on shutdown whenever `dbfilename` is not empty. For scheduled backups use `snapshot_cron`, a standard crontab expression (minute, hour, day of month, month, day of week).

- `snapshot_cron` exists since Dragonfly 1.7.1.
- Before 1.7.1 only `save_schedule` was available.
- `save_schedule` (`HH:MM` with globbing such as `*:15`) is deprecated and will be removed. Prefer `snapshot_cron`.

```shell
./dragonfly --logtostderr --dir my-snapshot-dir --snapshot_cron "*/5 * * * *"
```

This creates a snapshot every 5th minute.

| Cron | Meaning |
| --- | --- |
| `*/30 * * * *` | every 30th minute |
| `0 */2 * * *` | minute 0 of every 2nd hour |
| `0 0 * * *` | midnight daily |
| `0 6 * * 1-5` | 06:00 Monday to Friday |

Each snapshot produces a `...-0000.dfs` data file plus a `...-summary.dfs` file with a timestamp in the name (default `dbfilename` is `dump-{timestamp}`).

## Checked

2026-11-04. Confirmed against the Dragonfly Saving Backups page: shutdown backup when `dbfilename` is not empty, `snapshot_cron` since 1.7.1, `save_schedule` deprecated, the example command, cron table rows, file naming in the example listings, default `dump-{timestamp}`. Removed the pruning claim, which the page does not state.

Method: documentation only; no commands were run.
