---
id: computing-software.database-administration.oracle-database.data-guard-archive-gap-resolution
name: data-guard-archive-gap-resolution
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, data-guard, archive-gap, fal-server, incremental-from-scn, standby-recovery]
level: advanced
status: draft
description: "Detect and close Oracle Data Guard archive log gaps: automatic FAL resolution, manually registering missing logs, and rolling a standby forward with an incremental from SCN."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sbydb/log-apply-services.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sbydb/managing-physical-standby-databases.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sbydb/redo-transport-services.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Data Guard archive gap resolution

## Detect
On the standby:
```sql
SELECT thread#, low_sequence#, high_sequence# FROM v$archive_gap;
SELECT process, status, thread#, sequence# FROM v$managed_standby;        -- 19c; 21c+: v$dataguard_process
SELECT name, value, time_computed FROM v$dataguard_stats WHERE name IN ('transport lag','apply lag');
```
Alert log: `FAL[client]: Failed to request gap sequence` or `Fetching gap sequence in thread 1, gap sequence 5121-5130`.
Broker: `DGMGRL> SHOW DATABASE standby` -> `ORA-16766` / transport/apply lag warnings.

## Automatic resolution (FAL)
The standby requests missing logs from `FAL_SERVER` (primary, and other standbys):
```sql
ALTER SYSTEM SET fal_server = 'PRIM_TNS','STBY2_TNS' SCOPE=BOTH;   -- on each standby
```
With the broker this is set automatically. Most gaps from network outages close themselves
once connectivity returns, as long as the primary still has the logs.

## Manual: logs exist somewhere
Copy the missing archives (from primary disk or restored from backup) to the standby and register:
```bash
# on primary: restore if already deleted
RMAN> RESTORE ARCHIVELOG FROM SEQUENCE 5121 UNTIL SEQUENCE 5130 THREAD 1;
```
```sql
-- on standby
ALTER DATABASE REGISTER PHYSICAL LOGFILE '/u03/arch/1_5121_1123456789.arc';
-- or catalog a directory in RMAN on the standby:
-- RMAN> CATALOG START WITH '/u03/arch/gap/' NOPROMPT;
```
Managed recovery picks them up.

## Logs are gone: roll forward with an incremental (12c+ simplified)
On the standby (mounted, recovery stopped):
```
RMAN> RECOVER STANDBY DATABASE FROM SERVICE prim_tns;   -- 18c+: fetches incremental + controlfile
```
12c method: on standby `SELECT current_scn FROM v$database;`, on primary
`BACKUP INCREMENTAL FROM SCN <scn> DATABASE FORMAT '/tmp/stby_%U';` plus a standby controlfile,
then catalog and `RECOVER DATABASE NOREDO` on the standby, restore the controlfile, and restart
recovery. Datafiles added on the primary after that SCN must be restored separately.

## Prevent
- Archive deletion policy on the primary that respects the standby:
  `CONFIGURE ARCHIVELOG DELETION POLICY TO APPLIED ON ALL STANDBY BACKED UP 1 TIMES TO DISK;`
- Monitor transport lag; alert before the primary's retention window is exceeded.
- Size standby redo logs correctly so real-time apply keeps working.

## Verify
`v$archive_gap` returns no rows, `apply lag` is seconds, and `DGMGRL> SHOW CONFIGURATION`
reports `SUCCESS`.
