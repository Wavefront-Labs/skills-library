---
id: computing-software.data-engineering.snowflake.backup-sets-and-immutable-backups
name: backup-sets-and-immutable-backups
category: computing-software
field: data-engineering
product: snowflake
tags: [snowflake, snowflake-backups, backup-sets, retention-lock, ransomware-protection]
level: advanced
status: docs-checked
description: "Protect Snowflake data beyond Time Travel with backup policies and backup sets, including retention locks for immutable (WORM) backups and restoring from them."
sources:
  - https://docs.snowflake.com/en/user-guide/backups
  - https://docs.snowflake.com/en/user-guide/data-time-travel
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Backup sets and immutable backups

**Goal:** point-in-time copies of tables, schemas or databases that survive accidental drops beyond Time Travel and, with retention lock, cannot be deleted even by admins (ransomware / regulatory WORM).

## Concepts
- **Backup policy**: schedule and expiry for backups (optionally with retention lock).
- **Backup set**: the collection of backups for one object (table, schema or database).
- Backups are discrete snapshots of the objects you choose; you choose frequency, retention and whether to add a retention lock.

## Typical setup
```sql
CREATE BACKUP POLICY daily_30d
  SCHEDULE = '1440 MINUTE'
  EXPIRE_AFTER_DAYS = 30;

CREATE BACKUP SET finance_db_backups FOR DATABASE finance
  WITH BACKUP POLICY daily_30d;

ALTER BACKUP SET finance_db_backups ADD BACKUP;     -- ad-hoc backup now
SHOW BACKUPS IN BACKUP SET finance_db_backups;
```
Restore a database or schema with `CREATE DATABASE` / `CREATE SCHEMA ... FROM BACKUP SET <set> IDENTIFIER '<backup_id>'` (a new object under a new name; ids from SHOW BACKUPS), then swap or copy what you need. Test a restore before you need one.

## Immutable backups
A backup set created with a **retention lock** prevents anyone, even privileged users, from deleting its backups prematurely; without a lock a backup can be deleted and its expiry changed. Retention lock and legal holds need Business Critical Edition or higher. The docs cite a third-party assessment of the feature against SEC 17a-4(f) and similar rules. Start with short expiries while testing.

## vs Time Travel, Fail-safe, clones, replication
| Mechanism | Covers | Limit |
|---|---|---|
| Time Travel | accidental change/drop | 0 to 90 days on Enterprise or higher (Standard: 0 or 1) |
| Fail-safe | disaster recovery by Snowflake | see the Time Travel and Fail-safe docs; not self-service |
| Zero-copy clone | manual snapshot | can be dropped by owners |
| Replication | region/cloud outage | replicates mistakes too |
| Backups (+lock) | long, policy-driven, tamper-proof | storage cost for changed data |

## Gotchas
- Backups are available on all editions; retention lock and legal holds need Business Critical or higher.
- Retention lock + long expiry on a high-churn table means paying for all changed data for that period.

## Verify
Drop a test table protected by a backup set, restore it from the latest backup, and compare row counts.

## Checked

2026-10-28: reviewed against the Snowflake documentation fetched this batch.

Confirmed: CREATE BACKUP POLICY with SCHEDULE and EXPIRE_AFTER_DAYS, CREATE BACKUP SET ... FOR DATABASE ... WITH BACKUP POLICY, ALTER BACKUP SET ... ADD BACKUP, SHOW BACKUPS IN BACKUP SET, restore via FROM BACKUP SET ... IDENTIFIER, retention lock and legal hold edition requirement, SEC 17a-4(f) assessment, Time Travel range (backups, create-database, create-schema pages).

Removed or corrected: the zero-copy storage claim, 'including ACCOUNTADMIN' and 'irreversible' wording, and the Fail-safe 7-day figure (not on the pages read).

Method: documentation only; no commands were run.
