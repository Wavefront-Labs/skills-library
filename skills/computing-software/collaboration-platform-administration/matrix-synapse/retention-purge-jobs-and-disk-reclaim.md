---
id: computing-software.collaboration-platform-administration.matrix-synapse.retention-purge-jobs-and-disk-reclaim
name: retention-purge-jobs-and-disk-reclaim
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, retention, purge-jobs, longest-max-lifetime, shortest-max-lifetime, vacuum-full, disk-space]
level: advanced
status: docs-checked
description: "Schedule Synapse retention purge_jobs by room max_lifetime band, avoid heavy jobs, ensure every policy is covered, and reclaim disk afterwards with VACUUM FULL on PostgreSQL."
sources:
  - https://element-hq.github.io/synapse/latest/message_retention_policies.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Purge jobs run in the background to delete expired events, and only run when retention is enabled. Without configuration Synapse uses default jobs described in the config manual. For finer control, set `purge_jobs` inside the `retention` section. Each job selects rooms by their policy's `max_lifetime` using `shortest_max_lifetime` and `longest_max_lifetime`, and runs every `interval`:

```yaml
purge_jobs:
  - longest_max_lifetime: 3d
    interval: 12h
  - shortest_max_lifetime: 3d
    longest_max_lifetime: 1w
    interval: 1d
  - shortest_max_lifetime: 1w
    interval: 2d
```

This runs twice a day for rooms with `max_lifetime` up to 3 days, daily for 3 days to a week, and every 2 days beyond a week. The docs say the example shows more jobs than needed; in practice the last two could become one daily job for anything over 3 days.

Design rules from the page:

- A purge job can be heavy if it targets many rooms, so prefer jobs with a low interval that cover a limited set of rooms.
- Include one job with no minimum and one with no maximum, so every policy (including the default and lifetime-limit-adjusted values) is handled.
- A job running daily means an expired event can stay in the database up to a day, but Synapse hides it from local users from the moment it expires.

Disk space: purging deletes rows but the database may not return space to the operating system straight away, though new data is written into the freed space. To reclaim it, run `VACUUM FULL;` on PostgreSQL (or `VACUUM;` on SQLite) against Synapse's database; see the PostgreSQL VACUUM documentation.

Policy values themselves (default policy, lifetime limits, `m.room.retention`) are covered in the default policy skill.

## Checked

2026-11-04. Confirmed against the Synapse Message retention policies page: purge_jobs example and rules, hiding of expired events, disk space note with VACUUM FULL and VACUUM. Removed an unsourced locking and backup remark.
Method: documentation only; no commands were run.
