---
id: computing-software.database-administration.oracle-database.time-zone-file-dst-upgrades
name: time-zone-file-dst-upgrades
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle-patching, timezone-file-upgrade, dst, timestamp-with-time-zone, dbms-dst, autoupgrade]
level: advanced
status: docs-checked
description: "Upgrade the Oracle time zone file (DST rules) so TIMESTAMP WITH TIME ZONE data stays correct: check versions, run DBMS_DST prepare/upgrade, or let AutoUpgrade do it."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/nlspg/datetime-data-types-and-time-zone-support.html#GUID-B0ED6B4F-6E42-4D6F-A1FA-7A25FBD8A72D
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/arpls/DBMS_DST.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time zone file (DST) upgrades

Oracle stores region-based `TIMESTAMP WITH TIME ZONE` (TSTZ) values using a time zone file
version (`timezlrg_NN.dat`). When governments change DST rules, a newer file is shipped. Data stored under old rules must be
converted when you move the database to the new version.

## Check versions
```sql
SELECT * FROM v$timezone_file;                                -- version the database uses
SELECT property_name, property_value FROM database_properties
WHERE property_name LIKE 'DST_%';                             -- DST upgrade state
```

## Upgrade with DBMS_DST (outline)
1. **Prepare** (database open, finds affected data, no changes):
   ```sql
   EXEC DBMS_DST.BEGIN_PREPARE(43);
   EXEC DBMS_DST.FIND_AFFECTED_TABLES;
   SELECT * FROM sys.dst$affected_tables;
   SELECT * FROM sys.dst$error_table;
   EXEC DBMS_DST.END_PREPARE;
   ```
2. **Upgrade** (follow the DBMS_DST and upgrade guide for the required restart sequence and CDB handling):
   ```sql
   EXEC DBMS_DST.BEGIN_UPGRADE(43);
   DECLARE n NUMBER; BEGIN DBMS_DST.UPGRADE_DATABASE(n, parallel => TRUE, error_on_overlap_time => FALSE, error_on_nonexisting_time => FALSE); DBMS_OUTPUT.PUT_LINE('failures: '||n); END;
   /
   EXEC DBMS_DST.END_UPGRADE(:n);
   ```
Oracle also ships check and apply scripts under `rdbms/admin` in the Oracle home; see the
upgrade guide for the current names. In a CDB, run in root and each PDB.

## AutoUpgrade
AutoUpgrade can perform the time zone upgrade as a post-upgrade fixup; for big TSTZ tables
consider doing it in a separate window (see the AutoUpgrade config file reference for the switch).

## When it matters
- Columns of type `TIMESTAMP WITH TIME ZONE` with region names.

## Gotchas
- Large affected tables make the upgrade long (it updates rows); plan time from the prepare report.

## Checked
2026-11-01. Confirmed on the 19c DBMS_DST reference: BEGIN_PREPARE, FIND_AFFECTED_TABLES, END_PREPARE, BEGIN_UPGRADE, UPGRADE_DATABASE, END_UPGRADE. Removed: GET_LATEST_TIMEZONE_VERSION and its version gate, utltz script names, catcon.pl, timezone_upg switch, RU 19.18 claim, ORA-01805, scheduler/AQ examples, file path.
Method: documentation only; no commands were run.

## Verify
`SELECT * FROM v$timezone_file;` shows the new version, the `DST_%` database properties show no upgrade in progress, and
`sys.dst$error_table` is empty.
