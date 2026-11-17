---
id: computing-software.database-administration.oracle-database.unified-auditing
name: unified-auditing
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, oracle-security, unified-auditing, audit-policy, unified-audit-trail, dbms-audit-mgmt, ora-secureconfig, pure-unified-auditing, compliance]
level: advanced
status: draft
description: "Configure Oracle unified auditing: create and enable audit policies, query UNIFIED_AUDIT_TRAIL, and purge or archive the trail with DBMS_AUDIT_MGMT."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/dbseg/introduction-to-auditing.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/dbseg/administering-the-audit-trail.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Unified auditing

**Goal:** one audit trail (`UNIFIED_AUDIT_TRAIL`) recording privileged activity,
logins and sensitive data access, with a retention process so it does not fill SYSAUX.

## Mixed vs pure mode
By default (12c-19c) the database runs in **mixed mode**: unified policies work and
the traditional `AUDIT_TRAIL` audit also works. Pure unified auditing (relink with
`make -f ins_rdbms.mk uniaud_on ioracle`, the only mode in 23ai) disables traditional
auditing. Check: `SELECT value FROM v$option WHERE parameter = 'Unified Auditing';`
(TRUE = pure). Even in mixed mode, prefer unified policies and turn off old-style
`AUDIT` statements to avoid double trails.

## Defaults
`ORA_SECURECONFIG` (enabled by default; DDL on users/roles, ALTER SYSTEM, privilege
grants...) and `ORA_LOGON_FAILURES` (19c+). Mandatory audit (always on): `SYSDBA`
actions on startup/shutdown, audit configuration changes.
```sql
SELECT policy_name, enabled_option, entity_name, success, failure FROM audit_unified_enabled_policies;
```

## Create policies
```sql
CREATE AUDIT POLICY pol_priv_users
  PRIVILEGES CREATE USER, ALTER USER, DROP USER, GRANT ANY PRIVILEGE, GRANT ANY ROLE
  ACTIONS ALTER SYSTEM;
AUDIT POLICY pol_priv_users;

CREATE AUDIT POLICY pol_payroll_access
  ACTIONS SELECT ON hr.payroll, UPDATE ON hr.payroll, DELETE ON hr.payroll
  WHEN q'[SYS_CONTEXT('USERENV','SESSION_USER') NOT IN ('HR_BATCH')]' EVALUATE PER SESSION;
AUDIT POLICY pol_payroll_access;

CREATE AUDIT POLICY pol_dba_all ACTIONS ALL;
AUDIT POLICY pol_dba_all BY sys, system;           -- everything privileged users do
AUDIT POLICY ORA_LOGON_FAILURES WHENEVER NOT SUCCESSFUL;
```
`BY` / `EXCEPT` target users; `BY USERS WITH GRANTED ROLES dba` (12.2+) follows role
membership. In a CDB, create in root with `CONTAINER = ALL` for common policies.
Auditing `SELECT` on hot tables or `ACTIONS ALL` for app users generates huge volume: be narrow.

## Query
```sql
SELECT event_timestamp, dbusername, os_username, userhost, client_program_name,
       action_name, object_schema, object_name, return_code, sql_text, unified_audit_policies
FROM unified_audit_trail
WHERE event_timestamp > SYSTIMESTAMP - INTERVAL '1' DAY
ORDER BY event_timestamp DESC;
```
`return_code <> 0` = failed (e.g. 1017 bad password, 1031 insufficient privileges).
Records written to OS spillover files when the DB is not writable (read-only standby,
closed) are loaded with `DBMS_AUDIT_MGMT.LOAD_UNIFIED_AUDIT_FILES`.

## Retention and purge
The trail lives in `AUDSYS.AUD$UNIFIED` (partitioned, SYSAUX by default).
```sql
BEGIN
  DBMS_AUDIT_MGMT.SET_AUDIT_TRAIL_LOCATION(DBMS_AUDIT_MGMT.AUDIT_TRAIL_UNIFIED, 'AUDIT_TBS');
  DBMS_AUDIT_MGMT.SET_LAST_ARCHIVE_TIMESTAMP(DBMS_AUDIT_MGMT.AUDIT_TRAIL_UNIFIED, SYSTIMESTAMP - INTERVAL '90' DAY);
  DBMS_AUDIT_MGMT.CREATE_PURGE_JOB(
     audit_trail_type => DBMS_AUDIT_MGMT.AUDIT_TRAIL_UNIFIED, audit_trail_purge_interval => 24,
     audit_trail_purge_name => 'PURGE_UNIFIED', use_last_arch_timestamp => TRUE);
END;
/
```
Advance the last-archive timestamp daily (a scheduler job) after shipping records to
a SIEM, otherwise the purge job deletes nothing. `DBMS_AUDIT_MGMT.ALTER_PARTITION_INTERVAL`
sets partition granularity so purges drop partitions.

## Verify
- [ ] Enabled policies cover privileged users, user/role changes and logon failures.
- [ ] Trail is shipped off-database and purged; SYSAUX/audit tablespace growth flat.
- [ ] A test failed login appears with return_code 1017.
