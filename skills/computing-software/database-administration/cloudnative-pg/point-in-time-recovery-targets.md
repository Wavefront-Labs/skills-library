---
id: computing-software.database-administration.cloudnative-pg.point-in-time-recovery-targets
name: point-in-time-recovery-targets
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [pitr, recovery-target, targettime, targetlsn, targetname, targetxid, backupid, exclusive]
level: advanced
status: docs-checked
description: "Perform PITR in CloudNativePG: choose one recoveryTarget (targetTime, targetXID, targetName, targetLSN, targetImmediate), when backupID is mandatory, exclusive and timezones."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/recovery.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
PITR needs a valid WAL archive. Add a single target under `bootstrap.recovery.recoveryTarget`; the operator generates the PostgreSQL parameters.

```yaml
  bootstrap:
    recovery:
      source: origin
      recoveryTarget:
        targetTime: "2023-08-11 11:14:21.00000+02"
```

Targets (choose only one): `targetTime` (RFC 3339 or PostgreSQL timestamp), `targetXID` (committed before, optionally including, the xid; xids are assigned at start, so completion order can differ), `targetName` (restore point from `pg_create_restore_point()`), `targetLSN`, and `targetImmediate` (stop as soon as consistent, i.e. the end of the base backup).

Pitfalls:

- Timestamps without a zone are read as **UTC**; always write `2023-07-06T08:00:39Z` or `...+02:00`.
- Recovery stops at the first transaction after the target time; if none exists after it, recovery **fails**.
- Without `backupID`, for `targetTime` or `targetLSN` the operator picks the closest backup completed before the target, otherwise the last available backup. For `targetName`, `targetXID` and `targetImmediate` you **must** give `backupID`.

```yaml
      recoveryTarget:
        backupID: 20220616T142236
        targetName: "maintenance-activity"
        exclusive: true
```

Targets are inclusive by default; `exclusive: true` stops right before. `targetTLI` forces a timeline.

With a volume snapshot as base, you must ensure the snapshot's backup end time is before the target timestamp. If a tablespace was added or removed since the last base backup, WAL replay fails; you need a newer base backup.

## Checked

2026-11-04. Target semantics, backup selection rules, UTC default and the failure condition for time targets confirmed on the Recovery page, section Point in time recovery.

Method: documentation only; no commands were run.
