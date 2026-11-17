---
id: computing-software.database-administration.mysql.accounts-and-roles
name: accounts-and-roles
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mariadb, mysql-security, mysql-accounts, mysql-roles, create-user-mysql, grant, default-roles, activate-all-roles-on-login, least-privilege]
level: practitioner
status: verified
description: "Create MySQL 8 accounts (user@host), grant privileges through roles, set default roles, and audit who can do what without the old wildcard-host traps."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/roles.html
  - https://dev.mysql.com/doc/refman/8.4/en/account-names.html
  - https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MySQL accounts and roles

**Goal:** every application and person has its own account with privileges
coming from a small set of roles.

## Accounts are user@host
`'app'@'10.0.%'` and `'app'@'localhost'` are **different accounts** with
separate passwords and grants. When several match, MySQL picks the most specific
host first; an anonymous `''@'localhost'` can shadow `'app'@'%'` (remove
anonymous users: `SELECT user,host FROM mysql.user WHERE user='';`).
Roles are stored as accounts in `mysql.user` too (`CREATE ROLE app_read` creates `'app_read'@'%'` with `account_locked = Y`).

## Roles (8.0+)
```sql
CREATE ROLE 'app_read', 'app_write', 'app_ddl';
GRANT SELECT ON appdb.* TO 'app_read';
GRANT INSERT, UPDATE, DELETE ON appdb.* TO 'app_write';
GRANT ALTER, CREATE, DROP, INDEX, REFERENCES ON appdb.* TO 'app_ddl';

CREATE USER 'svc_api'@'10.0.%' IDENTIFIED BY '<secret>' PASSWORD EXPIRE NEVER;
GRANT 'app_read', 'app_write' TO 'svc_api'@'10.0.%';
SET DEFAULT ROLE 'app_read', 'app_write' TO 'svc_api'@'10.0.%';   -- otherwise roles are inactive on login!
```
Granted-but-not-default roles must be enabled per session with `SET ROLE ...` (checked on 9.7.4: without a default role `CURRENT_ROLE()` is `NONE` and a SELECT fails with error 1142; `SET ROLE app_write` for a role not granted gives error 3530). `activate_all_roles_on_login` defaults to OFF and `mandatory_roles` to empty.
`activate_all_roles_on_login = ON` makes all granted roles active (simpler,
less least-privilege). `mandatory_roles` grants a role to everyone.

## Audit
```sql
SHOW GRANTS FOR 'svc_api'@'10.0.%' USING 'app_read', 'app_write';
SELECT * FROM mysql.role_edges;
SELECT user, host, account_locked, password_last_changed FROM mysql.user;
SELECT grantee, privilege_type FROM information_schema.user_privileges WHERE privilege_type IN ('SUPER','FILE','PROCESS','SHUTDOWN');
```

## Gotchas
- `GRANT ... TO user IDENTIFIED BY` (create-on-grant) is gone in 8.0; CREATE USER first (a syntax error, error 1064, on 9.7.4).
- `FILE`, `SUPER`, `PROCESS` and `SYSTEM_VARIABLES_ADMIN` are effectively
  admin; 8.0 splits SUPER into dynamic privileges (`REPLICATION_SLAVE_ADMIN`,
  `CONNECTION_ADMIN`, ...): grant those instead.
- Lock rather than drop departing accounts that own definer objects:
  `ALTER USER ... ACCOUNT LOCK;` (views/procedures with a missing DEFINER fail).
- MariaDB role syntax differs in details; check its docs rather than assuming the MySQL statements above carry over (not run here).

## Verify
Log in as the service account, `SELECT CURRENT_ROLE();` shows the expected roles,
and a statement outside its grants fails with error 1142.
