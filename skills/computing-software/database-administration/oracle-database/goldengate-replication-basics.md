---
id: computing-software.database-administration.oracle-database.goldengate-replication-basics
name: goldengate-replication-basics
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, goldengate, extract, replicat, trail-files, supplemental-logging, zero-downtime-migration, logical-replication]
level: advanced
status: draft
description: "Set up Oracle GoldenGate replication between Oracle databases: database prerequisites, integrated Extract and Replicat, initial load, lag monitoring and common abends."
sources:
  - https://docs.oracle.com/en/middleware/goldengate/core/21.3/oracle-db/index.html
  - https://docs.oracle.com/en/middleware/goldengate/core/21.3/admin/index.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/refrn/ENABLE_GOLDENGATE_REPLICATION.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Oracle GoldenGate replication basics

GoldenGate captures committed changes from the redo (Extract), writes them to trail files,
ships them (Distribution/Receiver service or Data Pump extract), and applies them as SQL on the
target (Replicat). Uses: zero-downtime migrations and upgrades, active-active, feeding other platforms.
Separately licensed (or included in some cloud services).

## Database prerequisites (source)
```sql
ALTER SYSTEM SET enable_goldengate_replication = TRUE SCOPE = BOTH;
ALTER DATABASE FORCE LOGGING;
ALTER DATABASE ADD SUPPLEMENTAL LOG DATA;            -- minimal, at CDB root
-- archivelog mode required
CREATE USER c##ggadmin IDENTIFIED BY "<SECRET>" CONTAINER = ALL;
EXEC DBMS_GOLDENGATE_AUTH.GRANT_ADMIN_PRIVILEGE('c##ggadmin', container => 'ALL');
ALTER SYSTEM SET streams_pool_size = 2G SCOPE = BOTH;   -- integrated extract/replicat use it
```
Table-level supplemental logging (keys) from GGSCI / adminclient:
`ADD SCHEMATRANDATA pdb1.sales ALLCOLS` (or `ADD TRANDATA` per table). Tables without a PK/UK use all columns as the key: add keys.

## Configure (Microservices adminclient or GGSCI; classic syntax shown)
```
-- extract params (ext1.prm)
EXTRACT ext1
USERIDALIAS ggsrc DOMAIN OracleGoldenGate
EXTTRAIL ./dirdat/ea
SOURCECATALOG pdb1
DDL INCLUDE MAPPED
TABLE sales.*;

-- replicat params (rep1.prm)
REPLICAT rep1
USERIDALIAS ggtgt DOMAIN OracleGoldenGate
DBOPTIONS INTEGRATEDPARAMS(parallelism 4)
MAP pdb1.sales.*, TARGET sales.*;
```
```
DBLOGIN USERIDALIAS ggsrc
REGISTER EXTRACT ext1 DATABASE CONTAINER (pdb1)
ADD EXTRACT ext1, INTEGRATED TRANLOG, BEGIN NOW
ADD EXTTRAIL ./dirdat/ea, EXTRACT ext1
START EXTRACT ext1
-- target
ADD REPLICAT rep1, INTEGRATED, EXTTRAIL ./dirdat/ea
```

## Initial load (instantiation)
1. Start Extract first (captures from now).
2. Note an SCN: `SELECT current_scn FROM v$database;`
3. Export with `expdp ... FLASHBACK_SCN=<scn>`, import on target.
4. `START REPLICAT rep1, AFTERCSN <scn>` so Replicat applies only changes after the export point.

## Monitor
```
INFO ALL
LAG EXTRACT ext1
STATS REPLICAT rep1, TOTAL, LATEST
VIEW REPORT rep1
```
DB side: `SELECT * FROM v$goldengate_capture;` and `dba_apply_error` for integrated replicat errors.

## Common abends
| Symptom | Fix |
|---|---|
| OGG-01028 / missing archived log | Extract needs logs back to its recovery checkpoint; keep archive logs (RMAN deletion policy aware of GG) |
| OGG-01296 / ORA-01403 no data found on update | target out of sync; investigate row, `REPERROR` handling, resync table |
| ORA-00001 on insert | duplicate from overlapping initial load; was AFTERCSN used? |
| Lag growing | Replicat too slow: parallelism, missing indexes on target keys |

## Verify
`LAG` near zero under normal load, and Veridata or row-count/hash comparisons match on key tables.
