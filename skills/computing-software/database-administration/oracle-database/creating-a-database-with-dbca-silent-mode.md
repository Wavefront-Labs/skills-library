---
id: computing-software.database-administration.oracle-database.creating-a-database-with-dbca-silent-mode
name: creating-a-database-with-dbca-silent-mode
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, dbca, silent-mode, response-file, create-database, cdb, character-set]
level: practitioner
status: docs-checked
description: "Create Oracle databases repeatably with DBCA in silent mode (command-line flags or response file): CDB/PDB, character set, memory, storage, and post-create checks."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/creating-and-configuring-an-oracle-database.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/26/multi/dbca-command.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/riwin/dbca-commands-for-noninteractive-silent-configuration-of-rac.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Creating a database with DBCA silent mode

## Command line
```bash
dbca -silent -createDatabase \
  -templateName General_Purpose.dbc \
  -gdbName ORCL -sid ORCL \
  -createAsContainerDatabase true -numberOfPDBs 1 -pdbName PDB1 -pdbAdminPassword "<SECRET>" \
  -sysPassword "<SECRET>" -systemPassword "<SECRET>" \
  -characterSet AL32UTF8 -nationalCharacterSet AL16UTF16 \
  -storageType FS -datafileDestination /u02/oradata -useOMF true \
  -recoveryAreaDestination /u03/fra -recoveryAreaSize 204800 -enableArchive true \
  -memoryMgmtType AUTO_SGA -totalMemory 16384 \
  -redoLogFileSize 1024 \
  -emConfiguration NONE \
  -initParams "processes=1000"
```
Units: `-totalMemory`, `-redoLogFileSize` and `-recoveryAreaSize` are in MB. `-gdbName` must be `database_name.domain_name`; `-sid` defaults to the database name; `-useOMF`, `-enableArchive` and `-enableForceLogging` default to false; `-numberOfPDBs` defaults to 0. `-memoryMgmtType AUTO` on a host with more than 4 GB is not recommended: use `AUTO_SGA`. Specify `-recoveryAreaDestination NONE` to disable the fast recovery area.
ASM: `-storageType ASM -diskGroupName +DATA` (the Oracle RAC guide's example). RAC: `-databaseConfigType RAC -nodelist node1,node2`.
Prefer a response file (`-responseFile`) or the password prompts (the RAC guide shows `-sysPassword` with no value prompting) so secrets do not land in shell history.

## Response file
`-createDatabase` takes either `-responseFile` or the pair `-gdbName` and `-templateName` (an existing template name, or a full path to a template elsewhere). Set the parameters in a response file, then `dbca -silent -createDatabase -responseFile <RSP_DIR>/orcl.rsp`. The Oracle RAC guide's example uses the template `General_Purpose.dbc`; list the templates installed in your home before choosing.

## Choices you cannot easily change later
- **Character set**: Oracle recommends AL32UTF8 (the DBCA and OUI default since 12.2); DBCA's default configuration allows only recommended character sets, so a non-recommended set needs advanced mode or `CREATE DATABASE`.
- CDB vs non-CDB: `-createAsContainerDatabase false` is not supported by DBCA starting with Oracle Database 20.3 (it is accepted in 19c); always create a CDB for new work.

## Logs and failure
Read the DBCA log output for the failing step (log location: see the DBCA documentation for your release), fix the cause and retry; clean up any partial files and `/etc/oratab` entries first.

## After creation
```sql
SELECT name, cdb, log_mode, force_logging, flashback_on FROM v$database;
SELECT * FROM nls_database_parameters WHERE parameter LIKE '%CHARACTERSET';
SHOW PDBS
```
Then: multiplex control files and redo, set force logging if Data Guard is planned (or pass `-enableForceLogging true`), and configure RMAN.

## Verify
Database open, character set AL32UTF8, archivelog on, PDB open, listener shows the services.

## Checked
Date 2026-10-22. Oracle AI Database 26ai Multitenant Administrator's Guide (DBCA Silent Mode Commands, first 100,000
characters), 19c Administrator's Guide (creating a database; character set text) and 19c RAC installation guide (silent
example). Confirmed: the -createDatabase options kept in the example, units (MB), defaults, `-gdbName` format, AUTO_SGA
advice, `-recoveryAreaDestination NONE`, `-responseFile` or `-gdbName`+`-templateName`, AL32UTF8 recommendation and
12.2 default, non-CDB creation unsupported from 20.3. Removed (not found in the pages read): `-ignorePreReqs`,
`-recoveryGroupName`, `-generateScripts`, `-deleteDatabase`, template names other than General_Purpose.dbc, the
dbca.rsp path, the cfgtoollogs log path, DMU/block-size remarks, `audit_trail`/`db_block_checksum` init parameters.
`-initParams` is documented with an escape-character option; only a single parameter is shown. The 19c dbca-command-reference
URL returned 404 and was replaced; the DBCA syntax section of the 19c Administrator's Guide (2.14) was not read.
Method: documentation only; no commands were run.
