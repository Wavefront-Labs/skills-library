---
id: computing-software.database-administration.oracle-database.system-and-object-privileges-and-roles
name: system-and-object-privileges-and-roles
category: computing-software
field: database-administration
product: oracle-database
tags: [database-administration, oracle-database, oracle, oracle-security, oracle-users, system-privileges, object-privileges, roles, with-admin-option, with-grant-option, privilege-analysis, schema-only-account, least-privilege]
level: practitioner
status: draft
description: "Grant Oracle system and object privileges through roles with least privilege, use schema-only accounts and schema privileges, and find unused grants with privilege analysis."
sources:
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/dbseg/configuring-privilege-and-role-authorization.html
  - https://docs.oracle.com/en/database/oracle/oracle-database/19/dbseg/performing-privilege-analysis-find-privilege-use.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# System and object privileges and roles

## Privilege types
- **System privileges** (`CREATE SESSION`, `CREATE TABLE`, `SELECT ANY TABLE`,
  `ALTER SYSTEM`...): granted `WITH ADMIN OPTION` lets the grantee grant/revoke them;
  revoking from the grantor does **not** cascade.
- **Object privileges** (`SELECT`, `INSERT`, `UPDATE(col)`, `EXECUTE`, `READ`): granted
  `WITH GRANT OPTION`; revoking **does** cascade to downstream grants.
- `READ` (12c) is `SELECT` without the ability to `SELECT ... FOR UPDATE` lock rows; prefer it for readers.
- **Schema privileges** (23ai): `GRANT SELECT ANY TABLE ON SCHEMA hr TO reporting;`
  covers current and future tables in one schema without `ANY` across the database.

## Role pattern
```sql
CREATE ROLE app_read;
CREATE ROLE app_write;
GRANT READ ON hr.employees TO app_read;
GRANT INSERT, UPDATE, DELETE ON hr.employees TO app_write;
GRANT app_read TO app_write;
GRANT CREATE SESSION, app_write TO hr_app;
ALTER USER hr_app DEFAULT ROLE ALL;
```
Before 23ai, generate object grants per table with a PL/SQL loop or after each
deployment; `ANY` privileges are the shortcut to avoid.

## Things that bite
- **Roles are disabled inside definer's-rights PL/SQL** (procedures, views owned by
  the user): the owner needs direct object grants to compile code that references
  another schema. "Works in SQL*Plus, ORA-00942 in the procedure" = this.
- `ANY` privileges, `GRANT ANY PRIVILEGE`, `EXEMPT ACCESS POLICY`, `BECOME USER`,
  `CREATE ANY DIRECTORY`, `ALTER USER`, `DBA` role are effectively full control; keep them
  to named DBA accounts.
- Granting to `PUBLIC` grants to everyone. Revoke `EXECUTE` on `UTL_FILE`, `UTL_HTTP`,
  `UTL_TCP`, `UTL_SMTP`, `DBMS_JAVA` from PUBLIC per CIS benchmark, after checking dependents.

## Schema-only accounts (18c+)
Application owner with no password, so nobody logs in as the owner; deploy via proxy:
```sql
CREATE USER hr NO AUTHENTICATION;
ALTER USER hr GRANT CONNECT THROUGH deploy_user;
-- connect: sqlplus deploy_user[hr]/<deploy_pw>@pdb1
```

## Who has what
```sql
SELECT grantee, privilege, admin_option FROM dba_sys_privs WHERE grantee = 'HR_APP';
SELECT grantee, owner, table_name, privilege, grantable FROM dba_tab_privs WHERE grantee = 'APP_WRITE';
SELECT grantee, granted_role FROM dba_role_privs WHERE granted_role = 'DBA';
SELECT * FROM session_privs;  SELECT * FROM session_roles;   -- as the user
```

## Privilege analysis (DBMS_PRIVILEGE_CAPTURE, free since 2018 in EE)
```sql
BEGIN
  DBMS_PRIVILEGE_CAPTURE.CREATE_CAPTURE(name => 'app_cap', type => DBMS_PRIVILEGE_CAPTURE.G_CONTEXT,
     condition => q'[SYS_CONTEXT('USERENV','SESSION_USER') = 'HR_APP']');
  DBMS_PRIVILEGE_CAPTURE.ENABLE_CAPTURE('app_cap');
END;
/
-- run a full business cycle, then
EXEC DBMS_PRIVILEGE_CAPTURE.DISABLE_CAPTURE('app_cap');
EXEC DBMS_PRIVILEGE_CAPTURE.GENERATE_RESULT('app_cap');
SELECT * FROM dba_unused_privs WHERE capture = 'app_cap';
```
Revoke what is unused, keeping evidence of the capture window.

## Verify
- [ ] No application account holds `DBA` or `ANY` system privileges.
- [ ] Owners of PL/SQL have direct grants for cross-schema references.
- [ ] Privilege capture reviewed and unused grants revoked.
