---
id: computing-software.database-administration.oracle-database.rman-encryption-compression-and-multisection-backups
name: rman-encryption-compression-and-multisection-backups
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, rman, rman-encryption, section-size, backup-compression, multisection-backup, parallelism, transparent-encryption]
level: advanced
status: docs-checked
description: "Speed up and secure RMAN backups: channel parallelism, multisection SECTION SIZE for bigfiles, compression algorithms, and transparent/password/dual encryption."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/configuring-rman-client-advanced.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/backing-up-database-advanced.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/tuning-rman-performance.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RMAN encryption, compression and multisection backups

## Parallelism and multisection
```
RMAN> CONFIGURE DEVICE TYPE DISK PARALLELISM 8 BACKUP TYPE TO COMPRESSED BACKUPSET;
RMAN> BACKUP SECTION SIZE 32G DATABASE PLUS ARCHIVELOG;
```
One channel normally backs up one datafile, so one very large datafile ties up one channel.
`SECTION SIZE` splits large files into sections processed in parallel by all channels.

## Compression
```
RMAN> CONFIGURE COMPRESSION ALGORITHM 'BASIC';     -- default algorithm, a standard feature
```
Other algorithms belong to the Advanced Compression option; see the CONFIGURE reference for valid names.

## Encryption
| Mode | Setup | Restore needs |
|---|---|---|
| Transparent | TDE keystore open; `CONFIGURE ENCRYPTION FOR DATABASE ON;` | the keystore (keep it backed up separately) |
| Password | `SET ENCRYPTION ON IDENTIFIED BY '<SECRET>' ONLY;` per session | the password: `SET DECRYPTION IDENTIFIED BY '<SECRET>';` |
| Dual | `SET ENCRYPTION ON IDENTIFIED BY '<SECRET>';` with keystore open | either |
```
RMAN> CONFIGURE ENCRYPTION ALGORITHM '<name from V$RMAN_ENCRYPTION_ALGORITHMS>';
RMAN> SET ENCRYPTION ON IDENTIFIED BY '<SECRET>' ONLY;
RMAN> BACKUP DATABASE;
```
Password mode suits backups shipped to another site without the keystore. Losing the password or
keystore = backups are useless; store them in a vault and test restores on another host.

## Measure
```sql
SELECT * FROM v$rman_backup_job_details ORDER BY start_time DESC;
```
Synchronous vs asynchronous IO waits during backup: `v$backup_async_io` (look for files with high `long_waits`).

## Gotchas
- More channels than the backup target can absorb just adds contention; scale until throughput stops rising.
- `SECTION SIZE` larger than the file is ignored; very small sections add overhead. Aim for sections about file size / channels.

## Verify
Backup duration down vs baseline, backup pieces reported as encrypted, and a restore test in a separate environment using only vault-stored secrets succeeds.

## Checked

2026-10-28. Confirmed against the cited Oracle documentation: SECTION SIZE multisection backups, CONFIGURE COMPRESSION ALGORITHM (default algorithm standard, others Advanced Compression), CONFIGURE ENCRYPTION ALGORITHM values from V$RMAN_ENCRYPTION_ALGORITHMS, SET ENCRYPTION ON IDENTIFIED BY ... ONLY, V$BACKUP_ASYNC_IO LONG_WAITS (Backup and Recovery User Guide and Reference).

Removed or corrected: algorithm-name-to-codec mapping and per-algorithm licence list, TDE recompression note, 4 TB example and 12c/restore parallelism remarks, AES256 literal, Advanced Security licence remark, backup-piece check query, v$rman_backup_job_details column list and the archived-log compression remark (not found in the cited pages).

Method: documentation only; no commands were run.
