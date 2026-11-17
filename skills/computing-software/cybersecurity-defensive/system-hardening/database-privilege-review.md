---
id: computing-software.cybersecurity-defensive.system-hardening.database-privilege-review
name: database-privilege-review
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [database-privilege-review, access-review, least-privilege, postgresql, sql-server, mysql, entitlement-review]
level: practitioner
status: draft
description: "Run a periodic database privilege review: extract users, roles and grants per engine, find excessive privileges and orphans, certify with owners, and remove what is unused."
sources: ["https://www.cisecurity.org/controls/cis-controls-list", "https://www.postgresql.org/docs/current/ddl-priv.html", "https://learn.microsoft.com/en-us/sql/relational-databases/security/authentication-access/getting-started-with-database-engine-permissions", "https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Database privilege review

Privileges accumulate: emergency grants never revoked, leavers' accounts, apps running as owner. A quarterly or
semi-annual review (CIS Control 5/6, PCI DSS 7.2.4, SOX ITGC) brings them back to least privilege.

## 1. Extract
**PostgreSQL**
```sql
SELECT rolname, rolsuper, rolcreaterole, rolcreatedb, rolcanlogin, rolbypassrls, rolvaliduntil FROM pg_roles;
SELECT r.rolname AS member, g.rolname AS role FROM pg_auth_members m JOIN pg_roles r ON r.oid=m.member JOIN pg_roles g ON g.oid=m.roleid;
SELECT grantee, table_schema, table_name, privilege_type FROM information_schema.role_table_grants WHERE grantee NOT IN ('postgres','PUBLIC');
```
**SQL Server**
```sql
SELECT sp.name, sp.type_desc, sp.is_disabled, r.name AS server_role
FROM sys.server_principals sp LEFT JOIN sys.server_role_members rm ON sp.principal_id = rm.member_principal_id
LEFT JOIN sys.server_principals r ON r.principal_id = rm.role_principal_id;
-- per database: sys.database_principals, sys.database_role_members, sys.database_permissions
EXEC sp_change_users_login 'Report';   -- legacy orphan check; or join database_principals to server_principals by SID
```
**MySQL**: `SELECT user, host, account_locked, password_last_changed FROM mysql.user;` and `SHOW GRANTS FOR ...`
per account. **Oracle**: `DBA_USERS`, `DBA_ROLE_PRIVS`, `DBA_SYS_PRIVS`, `DBA_TAB_PRIVS`.

## 2. Flag
- Superuser / sysadmin / DBA role members beyond the named DBA team.
- Application accounts with DDL, owner or admin rights (should be DML on their schema).
- Accounts of leavers (join to HR/IdP), shared/generic human accounts, accounts unused for 90 days (last login:
  PostgreSQL via `log_connections` in logs, SQL Server login audit or `sys.dm_exec_sessions` history, MySQL
  audit plugin).
- Grants to PUBLIC; `WITH GRANT OPTION`/`WITH ADMIN OPTION`; `BYPASSRLS`; `ALL PRIVILEGES`.
- Orphaned database users (no matching login).
- Direct grants to individuals instead of roles.

## 3. Certify
Send each data owner a list of who has what on their database (role-level, human-readable), require
approve/revoke decisions by a deadline, and record the evidence. Use the IGA tool if one exists.

## 4. Remediate
Revoke unapproved access, convert direct grants to roles, lock unused accounts before dropping (safer rollback),
rotate credentials of shared accounts, and fix app accounts to least privilege with app teams.

## 5. Prevent drift
Grants managed as code (Terraform providers for PostgreSQL/MySQL/SQL Server, Liquibase/Flyway migrations),
database audit alerts on GRANT/ALTER ROLE, just-in-time elevation for DBAs via PAM.

## Verify
Review report signed by owners, revoked items confirmed in a fresh extract, and the number of superuser accounts
equals the documented DBA list.
