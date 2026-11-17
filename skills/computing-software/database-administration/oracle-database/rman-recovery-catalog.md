---
id: computing-software.database-administration.oracle-database.rman-recovery-catalog
name: rman-recovery-catalog
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, rman, recovery-catalog, create-catalog, register-database, resync-catalog, virtual-private-catalog, stored-scripts, control-file-record-keep-time, upgrade-catalog]
level: advanced
status: docs-checked
description: "Set up an RMAN recovery catalog: create the owner and catalog, register databases, resync, use stored scripts and virtual private catalogs, and upgrade it."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/bradv/managing-recovery-catalog.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/rcmrf/CREATE-CATALOG.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RMAN recovery catalog

**Why:** the control file is lost with the database. A catalog in a separate database keeps RMAN
metadata outside it and enables stored scripts and central reporting across many databases.

## Create
Catalog database: small, separate host from the protected databases, itself backed up
(control file + autobackup, or exported).
```sql
-- in the catalog DB
CREATE TABLESPACE rcat DATAFILE SIZE 2G AUTOEXTEND ON;
CREATE USER rco IDENTIFIED BY "<pw>" DEFAULT TABLESPACE rcat QUOTA UNLIMITED ON rcat;
GRANT RECOVERY_CATALOG_OWNER TO rco;
```
```
rman catalog rco@RCATDB
RMAN> CREATE CATALOG;
```

## Register databases
```
rman target / catalog rco@RCATDB
RMAN> REGISTER DATABASE;
RMAN> REPORT SCHEMA;            -- works now from catalog
RMAN> LIST INCARNATION;
```

## Resync
RMAN resyncs automatically when connected to the catalog during backups. Backups run
without the catalog (catalog down) are recorded in the control file and picked up by:
```
RMAN> RESYNC CATALOG;
```

## Stored scripts
```
RMAN> CREATE GLOBAL SCRIPT l0_backup {
  BACKUP INCREMENTAL LEVEL 0 DATABASE PLUS ARCHIVELOG DELETE INPUT;
  DELETE NOPROMPT OBSOLETE;
}
RMAN> RUN { EXECUTE GLOBAL SCRIPT l0_backup; }
RMAN> LIST GLOBAL SCRIPT NAMES;
```

## Virtual private catalog (separation of duties)
Give a team access only to its databases' metadata:
```
RMAN> GRANT CATALOG FOR DATABASE sales TO vpc_sales;   -- as catalog owner
```

## Upgrade and maintenance
The catalog schema version must be >= the newest RMAN client using it:
```
rman catalog rco@RCATDB
RMAN> UPGRADE CATALOG;
RMAN> UPGRADE CATALOG;   -- must be entered twice to confirm
```
The docs also point to the `dbmsrmansys.sql` script (granting additional privileges to the catalog owner)
for catalogs created or upgraded from certain versions; read the upgrade section before upgrading.

## Verify
- [ ] Every production DB registered (`LIST INCARNATION`, `REPORT SCHEMA` work from the catalog).
- [ ] Catalog database backed up and on separate infrastructure.
- [ ] Catalog version >= the highest RMAN client version.

## Checked
2026-11-01. Confirmed against the Oracle 19c Backup and Recovery User's Guide (Managing the Recovery Catalog) and
the CREATE CATALOG reference: RECOVERY_CATALOG_OWNER, CREATE CATALOG, dbmsrmansys.sql, GRANT CATALOG FOR DATABASE,
UPGRADE CATALOG entered twice, CREATE GLOBAL SCRIPT. Removed as unconfirmed: the 7-day control-file default,
the 14-31 day advice, Data Guard registration detail, VPD remark, catalog reporting views and the Enterprise
Edition note.
Method: documentation only; no commands were run.
