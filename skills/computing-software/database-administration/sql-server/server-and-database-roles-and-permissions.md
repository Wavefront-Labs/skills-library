---
id: computing-software.database-administration.sql-server.server-and-database-roles-and-permissions
name: server-and-database-roles-and-permissions
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, sql-server-security, server-roles, database-roles, grant-deny, revoke, least-privilege, ownership-chaining, schema-permissions, sys-fn-my-permissions]
level: practitioner
status: docs-checked
description: "Design least-privilege SQL Server access with server and database roles, schema-level GRANT, DENY and REVOKE, and audit effective permissions."
sources:
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/authentication-access/server-level-roles
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/authentication-access/database-level-roles
  - https://learn.microsoft.com/en-us/sql/relational-databases/security/permissions-hierarchy-database-engine
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Server and database roles, GRANT / DENY / REVOKE

**Goal:** every principal has exactly the permissions its job needs, granted to roles
(not individuals) at the narrowest securable that works.

## Semantics
- `GRANT` adds a permission; `REVOKE` removes a GRANT **or** a DENY (it is "remove
  the entry", not "deny"); `DENY` blocks and wins over any GRANT, including via roles.
- Exception: DENY does not apply to object owners or members of the `sysadmin` fixed server role.
- A table-level DENY does not take precedence over a column-level GRANT (kept for backward compatibility; avoid relying on it).

## Server level
Fixed roles: `sysadmin`, `securityadmin` (can grant itself almost anything: treat
as sysadmin), `serveradmin`, `dbcreator`, `processadmin`, `setupadmin`,
`bulkadmin`, `diskadmin`, `public`. 2022 adds `##MS_ServerStateReader##`,
`##MS_DefinitionReader##`, `##MS_DatabaseConnector##` and others for granular access.
Prefer granular permissions over fixed roles:
```sql
CREATE SERVER ROLE monitoring;
GRANT VIEW SERVER STATE, VIEW ANY DEFINITION TO monitoring;   -- 2022: VIEW SERVER PERFORMANCE STATE
ALTER SERVER ROLE monitoring ADD MEMBER [CORP\svc-monitor];
```

## Database level
Fixed: `db_owner`, `db_securityadmin`, `db_ddladmin`, `db_datareader`,
`db_datawriter`, `db_denydatareader`, `db_denydatawriter`, `db_backupoperator`.
Pattern: custom roles + schema grants, so new objects are covered automatically.
```sql
CREATE ROLE app_rw;
GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE ON SCHEMA::sales TO app_rw;
DENY DELETE ON OBJECT::sales.audit_log TO app_rw;
ALTER ROLE app_rw ADD MEMBER app_user;
```

## Audit effective permissions
```sql
EXECUTE AS USER = 'app_user';
SELECT * FROM fn_my_permissions('sales.orders', 'OBJECT');
REVERT;
-- members of sysadmin / db_owner
SELECT r.name role, m.name member FROM sys.server_role_members rm
JOIN sys.server_principals r ON r.principal_id = rm.role_principal_id
JOIN sys.server_principals m ON m.principal_id = rm.member_principal_id;
SELECT pr.name, pe.permission_name, pe.state_desc, pe.class_desc, OBJECT_NAME(pe.major_id)
FROM sys.database_permissions pe JOIN sys.database_principals pr ON pr.principal_id = pe.grantee_principal_id;
```

## Gotchas
- Granting to `public` grants to everyone. Check `public` permissions after vendor installs.
- Application accounts in `db_owner` "because it was easier" are the norm; fix them first.

## Checked
2026-11-01: fixed server and database roles, the ##MS_...## roles, DENY precedence and the column-level exception, `public` behaviour, and `fn_my_permissions` checked against the Microsoft Learn pages in sources plus DENY, REVOKE and fn_my_permissions. Removed: ownership chaining and module signing, `IMPERSONATE`/`CONTROL` remark, dbatools mention (not confirmed here).
Method: documentation only; no commands were run.

## Verify
- [ ] `sysadmin` members list is short and reviewed.
- [ ] App logins hold custom roles, not `db_owner`.
- [ ] `public` has no extra grants in user databases.
