---
id: computing-software.database-administration.yugabytedb.rbac-roles-and-grants
name: rbac-roles-and-grants
category: computing-software
field: database-administration
product: yugabytedb
tags: [rbac, roles, grant, revoke, yb-db-admin, yb-extension, yb-fdw, role-hierarchy, privileges]
level: practitioner
status: docs-checked
description: "Manage YSQL roles and privileges: users versus roles, role hierarchies, built-in roles such as yb_db_admin and yb_extension, and privilege grant patterns."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/secure/authorization/rbac-model.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/secure/authorization/create-roles.md", "https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/secure/authorization/ysql-grant-permissions.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# RBAC: roles and grants

In YSQL a role can be a user or a group. A role with `LOGIN` is a user, so all users are roles but not all roles are users. Roles can be granted to other roles to build a hierarchy, and roles inherit the privileges of the roles granted to them. As in PostgreSQL, role attributes (SUPERUSER, INHERIT, CREATEROLE, CREATEDB, REPLICATION, BYPASSRLS) are not inherited, even if the membership grant has INHERIT; you must `SET ROLE` to a role that has the attribute. Privileges can be granted at any level of the database hierarchy (ALL DATABASES > DATABASE > TABLE) and are inherited downwards; the privilege set is ALTER, AUTHORIZE, CREATE, DROP, MODIFY and SELECT, and ALTER on the base table is needed to create or drop its indexes.

Built-in roles:
- `postgres` and `yugabyte`: superusers (`postgres` is created during database creation; `yugabyte` is used during creation, by Yugabyte support for maintenance, and for backups with ysql_dump). `\duS` shows all roles, including the built-in ones.
- `yb_db_admin`: lets non-superusers create tablespaces and perform other privileged operations
- `yb_extension`: lets non-superusers create PostgreSQL extensions, all of those bundled with YugabyteDB (grant it to a role, `SET ROLE` to it, then `CREATE EXTENSION`)
- `yb_fdw`: lets non-superusers create, alter and drop foreign data wrappers

Patterns:
```
CREATE ROLE engineering;
CREATE ROLE john LOGIN PASSWORD 'secret';
GRANT engineering TO john;
CREATE ROLE developer; GRANT engineering TO developer;
```
Grant read to the group and write privileges to subgroups, as the page's tutorial does: `GRANT SELECT ON integration_tests TO engineering; GRANT USAGE ON SCHEMA public TO engineering;`, then `GRANT INSERT, UPDATE, DELETE, TRUNCATE ON TABLE integration_tests TO developer;`. Roles that inherit `engineering` get its read access. `ALTER TABLE integration_tests OWNER TO qa` gives a role full privileges on a table, and `ALTER USER db_admin WITH SUPERUSER` (superuser only) gives all privileges, reversed with `NOSUPERUSER`. Granting or revoking a role requires the AUTHORIZE privilege on the role being granted or revoked; `REVOKE engineering FROM john` removes the membership. Check table privileges with `\z`.

Inspect with `\du` in ysqlsh or `SELECT rolname, rolcanlogin, rolsuper FROM pg_roles;`.

Identifiers fold to lowercase: `CREATE ROLE Alice` creates `alice`; quote the name (`CREATE ROLE "Alice"`) for a case-sensitive role.

## Checked

2026-11-04. Confirmed against the RBAC model page (users versus roles, hierarchy, inheritance, attribute non-inheritance and SET ROLE, built-in roles and their descriptions, yb_extension example, resources and privileges), the Create roles page (CREATE ROLE, LOGIN PASSWORD, GRANT, AUTHORIZE, hierarchy, pg_roles query, \du, REVOKE, DROP ROLE, lowercase folding) and the Grant permissions tutorial (GRANT SELECT/USAGE, GRANT INSERT, UPDATE, DELETE, TRUNCATE, OWNER TO, SUPERUSER). Replaced the `GRANT SELECT ON ALL TABLES IN SCHEMA public` example, which the pages do not use, with the tutorial's grants.

Method: documentation only; no commands were run.
