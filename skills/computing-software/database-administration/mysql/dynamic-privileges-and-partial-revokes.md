---
id: computing-software.database-administration.mysql.dynamic-privileges-and-partial-revokes
name: dynamic-privileges-and-partial-revokes
category: computing-software
field: database-administration
product: mysql
tags: [database-administration, mysql, mysql-security, mysql-accounts, dynamic-privileges, partial-revokes, least-privilege, super-privilege]
level: practitioner
status: verified
description: "Replace MySQL SUPER with specific dynamic privileges, grant at the right level, and use partial_revokes to exclude schemas from global grants."
sources:
  - https://dev.mysql.com/doc/refman/8.4/en/privileges-provided.html
  - https://dev.mysql.com/doc/refman/8.4/en/partial-revokes.html
  - https://dev.mysql.com/doc/refman/8.4/en/grant.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dynamic privileges and partial revokes

## Privilege levels
Global (`*.*`), database (`db.*`), table (`db.t`), column (`SELECT (col) ON db.t`), routine,
proxy. Grant at the narrowest level that works.

## Dynamic privileges replace SUPER
`SUPER` is deprecated (docs; on 9.7.4 `GRANT SUPER` still works but returns warning 1287 "The SUPER privilege identifier is deprecated"). Grant the specific capability instead:
| Need | Dynamic privilege |
|---|---|
| `SET GLOBAL` / `SET PERSIST` | `SYSTEM_VARIABLES_ADMIN` (+ `PERSIST_RO_VARIABLES_ADMIN` for `SET PERSIST_ONLY`, which fails with error 3630 without it, even for a dynamic variable) |
| kill other users' queries | `CONNECTION_ADMIN` (`SYSTEM_VARIABLES_ADMIN` alone gets error 1095 "You are not owner of thread") |
| manage replication | `REPLICATION_SLAVE_ADMIN`, `REPLICATION_APPLIER`, `GROUP_REPLICATION_ADMIN` |
| purge/rotate binlogs | `BINLOG_ADMIN` |
| create views/routines with another DEFINER | `SET_ANY_DEFINER` (8.2+; without it, error 1227) or `SET_USER_ID` (older, deprecated). A definer that holds `SYSTEM_USER` additionally needs `SYSTEM_USER` yourself |
| write when `read_only=ON` | `CONNECTION_ADMIN` (read_only bypass) |
| backup tools | `BACKUP_ADMIN` (`LOCK INSTANCE FOR BACKUP` ran with only this grant), `CLONE_ADMIN` |
| encryption keys | `ENCRYPTION_KEY_ADMIN` |
| bypass `max_connections` reserved slot | `CONNECTION_ADMIN` |
| see all sessions | `PROCESS` (static) |
Check what exists: `SELECT * FROM information_schema.user_privileges WHERE grantee LIKE '%dba%';`
and `SHOW PRIVILEGES;`.

## Typical role design
```sql
CREATE ROLE app_rw, app_ro, ops_dba;
GRANT SELECT, INSERT, UPDATE, DELETE ON shop.* TO app_rw;
GRANT SELECT ON shop.* TO app_ro;
GRANT PROCESS, RELOAD, REPLICATION CLIENT, SYSTEM_VARIABLES_ADMIN, CONNECTION_ADMIN,
      BINLOG_ADMIN ON *.* TO ops_dba;
GRANT app_rw TO 'app'@'10.0.%';
SET DEFAULT ROLE app_rw TO 'app'@'10.0.%';
```

## Partial revokes
With `partial_revokes = ON` you can grant globally but carve out schemas:
```sql
SET PERSIST partial_revokes = ON;
GRANT SELECT, INSERT, UPDATE, DELETE ON *.* TO 'analyst'@'%';
REVOKE INSERT, UPDATE, DELETE ON mysql.* FROM 'analyst'@'%';
REVOKE SELECT ON hr.* FROM 'analyst'@'%';
SHOW GRANTS FOR 'analyst'@'%';   -- shows GRANT ... ON *.* and the REVOKE restrictions
```
Restrictions are stored in `mysql.user.User_attributes`, e.g. `{"Restrictions": [{"Database": "mysql", "Privileges": ["INSERT", "UPDATE", "DELETE"]}, ...]}`. Turning `partial_revokes` off later
fails with error 3896 while any restriction exists. The `REVOKE` on a schema that does not exist yet (`hr` above) is accepted.

## Gotchas
- Wildcards in database names (`shop\_%`) are interpreted as patterns in grants; with
  partial_revokes ON, `%` and `_` in REVOKE ... ON db.* are literal (checked: after `REVOKE SELECT ON shop_a.*`, schema `shopxa` stayed readable). Escape consistently. Note the `mysql` client treated `\_` in a statement as an unknown client command in the test run, so send such statements through a driver instead of the mysql client script.
- `GRANT ALL ON *.*` includes `GRANT OPTION` only if you add `WITH GRANT OPTION`, but it does
  include `SHUTDOWN`, `SUPER`, `FILE` and every dynamic privilege (checked with `SHOW GRANTS`): avoid for apps.
- `FILE` privilege lets a user read files mysqld can read, limited by `secure_file_priv` (`NULL` on the Windows zip with no setting: `LOAD_FILE` then returns NULL; set it to a directory to allow access there only).
- Roles must be active (`SET DEFAULT ROLE` or `activate_all_roles_on_login`).

## Verify
`SHOW GRANTS FOR user USING role;` matches the intended least-privilege set, and an attempted
forbidden action returns error 1142/1227.
