---
id: computing-software.systems-network-administration.incus.snapshot-schedule
name: snapshot-schedule
category: computing-software
field: systems-network-administration
product: incus
tags: [incus, snapshots-schedule, snapshots-expiry, snapshots-pattern, cron, automation]
level: practitioner
status: docs-checked
description: "Schedule automatic Incus snapshots with snapshots.schedule (alias or cron syntax, at most once per minute) plus snapshots.expiry, snapshots.pattern and snapshots.schedule.stopped."
sources:
  - https://raw.githubusercontent.com/lxc/incus/main/doc/howto/instances_backup.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scheduled snapshots

```
incus config set <instance> snapshots.schedule=@daily
incus config set <instance> snapshots.schedule="0 6 * * *"
```

- Schedules run at most once per minute.
- The page recommends setting these alongside the schedule:
  - `snapshots.expiry`: automatic expiry of old snapshots.
  - `snapshots.pattern`: naming pattern for the snapshots.
  - `snapshots.schedule.stopped`: whether to snapshot instances that are not running.

## Checked

2026-11-04: confirmed against the Incus instance backup how-to (schedule alias and cron examples, at most once per minute, expiry, pattern and stopped-instance options). Nothing removed.

Method: documentation only; no commands were run.
