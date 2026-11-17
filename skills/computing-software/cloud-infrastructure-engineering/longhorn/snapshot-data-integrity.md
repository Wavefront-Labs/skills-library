---
id: computing-software.cloud-infrastructure-engineering.longhorn.snapshot-data-integrity
name: snapshot-data-integrity
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [data-integrity, snapshot-data-integrity, fast-check, bit-rot, cronjob]
level: advanced
status: docs-checked
description: "Detect snapshot corruption in Longhorn with snapshot-data-integrity (disabled, enabled, fast-check), the cron schedule, immediate check and per-volume override."
sources:
  - https://longhorn.io/docs/1.13.0/advanced-resources/data-integrity/snapshot-data-integrity-check/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: find silent snapshot corruption and trigger rebuilds.

Global settings:
- `snapshot-data-integrity`:
  - `disabled`: no hashing or checking
  - `enabled`: periodic hashing and checking; can detect filesystem-unaware corruption such as bit rot, at a performance cost during checks
  - `fast-check`: hashes only files that are unhashed or whose modification time changed; cannot detect filesystem-unaware corruption but has less impact
- `snapshot-data-integrity-immediate-check-after-snapshot-creation`: whether to hash and check right after a snapshot is created; can be disabled to reduce impact
- `snapshot-data-integrity-cronjob`: a unix-cron schedule for when checks run

The page states no defaults.

Per volume: `Volume.Spec.SnapshotDataIntegrity` takes `ignored` (default, use the global setting), `disabled`, `enabled` or `fast-check`.

Behaviour: when a snapshot disk file in one replica is corrupted, Longhorn automatically starts rebuilding that replica. Hashing and checking reduce read IOPS, bandwidth and latency.

Recommendations: schedule checks for off-peak hours with the cronjob setting, and disable the immediate-check setting.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/advanced-resources/data-integrity/snapshot-data-integrity-check/

Removed: the closing line about fast-replica-rebuild-enabled requirements (not on this page).

Method: documentation only; no commands were run.
