---
id: computing-software.database-administration.oracle-database.password-file-and-administrative-privileges
name: password-file-and-administrative-privileges
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, orapwd, password-file, sysdba, sysbackup, sysdg, syskm, remote-login-passwordfile]
level: practitioner
status: docs-checked
description: "Manage the Oracle password file with orapwd, grant separation-of-duty admin privileges (SYSBACKUP, SYSDG, SYSKM), and keep it in sync across RAC and Data Guard."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/admin/getting-started-with-database-administration.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/dbseg/configuring-privilege-and-role-authorization.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Password file and administrative privileges

## Why
`SYSDBA` and the other administrative privileges authenticate outside the database (it may be
down). Locally, OS group membership (`dba`, `backupdba`, `dgdba`, `kmdba`) does it; remotely, the
**password file** does (`remote_login_passwordfile = EXCLUSIVE`).

## Create / recreate
```bash
orapwd file=$ORACLE_HOME/dbs/orapwORCL format=12.2 force=y
# prompts for the SYS password
# ASM / RAC: store in the disk group
orapwd file='+DATA/ORCL/orapworcl' dbuniquename=ORCL format=12.2
srvctl modify database -db ORCL -pwfile +DATA/ORCL/orapworcl
```
Default location: `$ORACLE_HOME/dbs/orapw<SID>` (Linux).

## Separation of duty
| Privilege | For |
|---|---|
| SYSDBA | everything; connects as SYS |
| SYSOPER | startup/shutdown/backup without data access |
| SYSBACKUP | RMAN backup/recovery (`rman target '"bkpuser@ORCL AS SYSBACKUP"'`) |
| SYSDG | Data Guard broker operations |
| SYSKM | TDE keystore management |
| SYSRAC | clusterware agents |
```sql
CREATE USER c##bkp IDENTIFIED BY "<SECRET>" CONTAINER = ALL;
GRANT SYSBACKUP TO c##bkp CONTAINER = ALL;
SELECT username, sysdba, sysoper, sysbackup, sysdg, syskm, account_status FROM v$pwfile_users;
```
Granting writes the user into the password file automatically.

## Changing the SYS password
`ALTER USER sys IDENTIFIED BY "<NEW>";` updates the password file. In Data Guard and RAC
check that every database and instance accepts the new password with a remote `AS SYSDBA` login from another host.

## Gotchas
- Check `v$pwfile_users` after any recreate or restore of the password file.

## Verify
`v$pwfile_users` lists the expected accounts, and remote `AS SYSBACKUP` RMAN connection works on every instance.

## Checked

2026-10-28. Confirmed against the cited Oracle documentation: orapwd FILE= FORMAT=12.2 [FORCE] [ASM] [DBUNIQUENAME], administrative privileges SYSDBA/SYSOPER/SYSBACKUP/SYSDG/SYSKM/SYSRAC, V$PWFILE_USERS (Administrator Guide and SQL*Plus guide).

Removed or corrected: password-complexity note, regrant-after-recreate claim, 12.2 standby propagation claim and the ORA-01017/ORA-01994/ORA-16191, redo_transport_user and unified-auditing gotchas (not found in the cited pages).

Method: documentation only; no commands were run.
