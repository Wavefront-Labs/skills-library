---
id: computing-software.database-administration.oracle-database.initialization-parameter-files
name: initialization-parameter-files
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, oracle-instance, spfile, pfile, init-parameters, alter-system-scope, create-pfile-from-spfile, v-spparameter]
level: practitioner
status: docs-checked
description: "Manage Oracle initialization parameters with the spfile: SCOPE rules, RESET, exporting to a pfile, re-creating an spfile, and comparing memory with the spfile."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/creating-and-configuring-an-oracle-database.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Initialization parameter files (spfile and pfile)

## Search order at STARTUP
The instance reads an SPFILE from the platform-specific default location: first `spfile<ORACLE_SID>.ora`, then
`spfile.ora` (which lets all RAC instances share one server parameter file). If no SPFILE is found it searches for a
text initialization parameter file. `STARTUP PFILE = <path>` overrides this with a named text file.

The SPFILE is a binary file created from a text parameter file with `CREATE SPFILE`; it cannot be edited with a text
editor. Use `ALTER SYSTEM` (or export, edit, re-create) instead.

## Changing parameters
```sql
ALTER SYSTEM SET open_cursors = 1000 SCOPE = BOTH;    -- memory + spfile (dynamic parameters only)
ALTER SYSTEM SET processes = 1500 SCOPE = SPFILE;     -- static parameter: next restart
ALTER SYSTEM SET open_cursors = 800 SCOPE = MEMORY;   -- until restart (dynamic only)
ALTER SYSTEM RESET <parameter_name> SCOPE = SPFILE;   -- remove from the spfile
```
- `SCOPE = SPFILE`: spfile only; effective at next startup, persistent; the only scope allowed for static parameters.
- `SCOPE = MEMORY`: current instance only, immediate, lost on restart; not allowed for static parameters.
- `SCOPE = BOTH`: memory and spfile; immediate and persistent; not allowed for static parameters.
- Default is `BOTH` if the instance started from an SPFILE and `MEMORY` if it started from a text file. Specifying
  `SPFILE` or `BOTH` without an SPFILE is an error.
- `DEFERRED` (dynamic parameters) makes the change apply to future sessions only.
- `COMMENT = '<text>'` stores a comment with the change.
- `ALTER SYSTEM RESET` returns a parameter to its default or startup value. In a non-CDB or CDB root, `SCOPE=SPFILE`
  removes it from the spfile so the default applies at next startup. After `SCOPE=BOTH`, `SCOPE=MEMORY` resets to the
  default value. In a PDB the value is inherited from the root.

## Backups and recovery from a bad change
```sql
CREATE PFILE = '<ADMIN_DIR>/init_backup.ora' FROM SPFILE;     -- before every change; comments are preserved
CREATE PFILE = '<ADMIN_DIR>/init_mem.ora' FROM MEMORY;        -- current running values
CREATE SPFILE FROM PFILE = '<ADMIN_DIR>/init_backup.ora';     -- rebuild after editing the text file
```
These statements need SYSDBA, SYSOPER or SYSBACKUP, and the exported file is created on the database server. The
database does not have to be started for `CREATE SPFILE`; if the instance runs from an SPFILE, re-creating that same
file is an error. `CREATE SPFILE FROM MEMORY` is also available.

Recovery from a bad change: start with `STARTUP PFILE = <edited text file>`, then `CREATE SPFILE FROM PFILE`.

## Views
`V$SPPARAMETER` shows the current contents of the SPFILE; its `ISSPECIFIED` column is FALSE for all rows if no SPFILE
is in use. Compare it with `V$PARAMETER` (running values) to find memory-only or spfile-only changes.

## Verify
- [ ] A dated pfile export exists from before the latest change.
- [ ] No unintended differences between `V$PARAMETER` and `V$SPPARAMETER`.

## Checked
Date: 2026-11-09. Confirmed against the Oracle 19c Database Administrator's Guide chapter "Creating and Configuring an
Oracle Database" (read by targeted search of the fetched page, not line by line) and the startup chapter for the
fallback to a text file: SPFILE search order, SCOPE semantics and defaults, DEFERRED, RESET behaviour, CREATE PFILE and
CREATE SPFILE rules and privileges, `V$SPPARAMETER`. Removed (not confirmed): SPFILE paths, RAC/ASM `srvctl` and
`init<SID>.ora` pointer notes, `SID =` clause, `ISSYS_MODIFIABLE` values, the mismatch query, RMAN
`RESTORE SPFILE`, alert-log history claim, hidden-parameter and PDB_SPFILE$ remarks, the reference-manual source
(it returned a stub).
Method: documentation only; no commands were run.
