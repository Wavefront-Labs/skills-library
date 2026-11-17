---
id: computing-software.database-administration.oracle-database.data-pump-remapping-schemas-and-tablespaces
name: data-pump-remapping-schemas-and-tablespaces
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, data-pump, impdp, remap-schema, remap-tablespace, remap-table, remap-data, transform, network-link, sqlfile, table-exists-action, schema-refresh]
level: practitioner
status: docs-checked
description: "Refresh or copy Oracle schemas with impdp REMAP_SCHEMA, REMAP_TABLESPACE, TRANSFORM and NETWORK_LINK, preview DDL with SQLFILE, and avoid import traps."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/sutil/datapump-import-utility.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data Pump: remapping schemas and tablespaces

Typical job: refresh `APP_TEST` in a test PDB from `APP` in production, landing in
different tablespaces, without the production storage clauses.

## Parameter file
```
# imp_refresh.par
DIRECTORY=DP_DIR
DUMPFILE=app_%U.dmp
LOGFILE=imp_app_test.log
SCHEMAS=APP
REMAP_SCHEMA=APP:APP_TEST
REMAP_TABLESPACE=APP_DATA:TEST_DATA,APP_IDX:TEST_IDX
TRANSFORM=SEGMENT_ATTRIBUTES:N      # omit physical/storage attributes, tablespaces and logging (default Y)
TRANSFORM=OID:N                     # assign new OIDs to object tables and types instead of reusing the exported ones
TRANSFORM=DISABLE_ARCHIVE_LOGGING:Y # TABLE and INDEX logging disabled during load, restored after; no effect under FORCE LOGGING
TABLE_EXISTS_ACTION=REPLACE         # SKIP | APPEND | TRUNCATE | REPLACE
EXCLUDE=STATISTICS                  # gather fresh stats after import instead
PARALLEL=8
LOGTIME=ALL
METRICS=YES
```
`impdp system@testpdb parfile=imp_refresh.par`. Oracle recommends parameter files for parameters whose
values need quotation marks.

## Other remaps
```
REMAP_TABLE=APP.ORDERS:ORDERS_OLD          # rename a table on import (schema.old_table[.partition]:new_table)
REMAP_DATAFILE='/u01/old/x.dbf':'/u02/new/x.dbf'   # source_datafile:target_datafile
REMAP_DATA=APP.CUSTOMERS.EMAIL:APP.MASK_PKG.MASK_EMAIL   # [schema.]table.column:[schema.]pkg.function, e.g. masking PII
REMAP_DIRECTORY=source_directory_string:target_directory_string
```
`REMAP_DATA` does not support user-defined types, LONG, REF, VARRAY, nested tables, BFILE or XMLType columns.

## Preview first
```
impdp system@testpdb DIRECTORY=DP_DIR DUMPFILE=app_%U.dmp SQLFILE=app_ddl.sql REMAP_SCHEMA=APP:APP_TEST
```
`SQLFILE` writes the DDL that the import would run, instead of importing: check tablespaces and object
references before the real run.

## No dump file: NETWORK_LINK
```
impdp system@testpdb NETWORK_LINK=PROD_LINK SCHEMAS=APP REMAP_SCHEMA=APP:APP_TEST \
  EXCLUDE=STATISTICS PARALLEL=4
```
Reads straight from the source over a database link; there are no dump files. The link must exist already
(`CREATE DATABASE LINK`). If the importing user has `DATAPUMP_IMP_FULL_DATABASE` on the target, that user also
needs `DATAPUMP_EXP_FULL_DATABASE` on the source. `FLASHBACK_TIME` and `FLASHBACK_SCN` (mutually exclusive) are
only allowed with `NETWORK_LINK`. Source and target may differ by no more than two major versions. Private
connected-user and current-user links are not supported, evolved types are not supported, and an unencrypted link
sends all data as clear text.

## Traps
- A schema-mode import by a user with `DATAPUMP_IMP_FULL_DATABASE` first imports the user definitions (if the user
  does not exist), including system and role grants and password history; an unprivileged user gets objects only.
  Otherwise pre-create the target user.
- `TABLE_EXISTS_ACTION=SKIP` and `REPLACE` are not valid with `CONTENT=DATA_ONLY`. `REPLACE` drops the table and
  recreates it and its dependent objects (unless excluded); `SKIP`, `APPEND` and `TRUNCATE` leave indexes, grants,
  triggers and constraints untouched. `TRUNCATE` and `REPLACE` need the table not to be a target of referential
  constraints. `APPEND` always loads into new space.
- Code that hard-codes the old schema name is not rewritten by `REMAP_SCHEMA`; search the `SQLFILE` output for it.
- Monitor and control: `impdp system attach=<job_name>` then `STATUS`, `PARALLEL=n`, `STOP_JOB`, `START_JOB`;
  `DBA_DATAPUMP_JOBS` lists jobs.

## Verify
- [ ] Log ends "successfully completed" or every error line is explained.
- [ ] Object counts by type match source; no INVALID objects after recompilation.
- [ ] No references to the old schema name remain in code.

## Checked
2026-11-09. Read the 19c Utilities guide, Data Pump Import chapter (parameters `NETWORK_LINK`, `SCHEMAS`,
`TABLE_EXISTS_ACTION`, `SQLFILE`, `REMAP_*`, `TRANSFORM` options and interactive commands); placeholder names in the
examples are illustrative. Removed as not stated there: the "12c+" and "19c" version tags, the `FLASHBACK_TIME=SYSTIMESTAMP`
example, the LONG-over-network-link note, the ORA-02304 note, the sequence behaviour, the grants-to-other-users note,
the source password hash detail, `UTL_RECOMP` and the dictionary queries.
Method: documentation only; no commands were run.
