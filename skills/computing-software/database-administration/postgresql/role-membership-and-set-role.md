---
id: computing-software.database-administration.postgresql.role-membership-and-set-role
name: role-membership-and-set-role
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, database-roles, role-privileges, role-membership, set-role, inherit, group-roles, grant-role, least-privilege]
level: practitioner
status: verified
description: "Design PostgreSQL group roles and membership with INHERIT, SET and ADMIN options so apps get least privilege and humans escalate explicitly with SET ROLE."
sources:
  - https://www.postgresql.org/docs/current/role-membership.html
  - https://www.postgresql.org/docs/current/sql-grant.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Role membership and SET ROLE

**Goal:** privileges are granted to a few group roles; login roles get them by
membership; powerful roles need a deliberate `SET ROLE`.

## Standard layout
```sql
CREATE ROLE app_read  NOLOGIN;
CREATE ROLE app_write NOLOGIN;
CREATE ROLE app_owner NOLOGIN;             -- owns schema objects; nobody logs in as it
GRANT app_read TO app_write;               -- write implies read

CREATE ROLE svc_api  LOGIN PASSWORD NULL;  -- password set via \password
GRANT app_write TO svc_api;
CREATE ROLE alice LOGIN;
GRANT app_read TO alice;
GRANT app_owner TO alice WITH INHERIT FALSE;   -- PG16+: must SET ROLE to use it
```

## INHERIT vs SET (PG16 grant options)
- `INHERIT TRUE` (default): member uses the role's privileges automatically.
- `INHERIT FALSE`: privileges only after `SET ROLE app_owner;` — good for
  migration/DDL rights so day-to-day sessions cannot drop tables by accident.
- `SET FALSE`: member may inherit but not `SET ROLE` to it (stops creating
  objects owned by that role); checked: such a member got `permission denied to set role` while `pg_has_role(..., 'USAGE')` stayed true.
- `ADMIN OPTION`: may grant the role to others. PG16 removed the old
  CREATEROLE-can-do-anything behaviour; CREATEROLE users now get ADMIN on roles
  they create only.
Pre-16, `NOINHERIT` was a property of the member role, not per grant.

## DDL ownership pattern
Run migrations as `SET ROLE app_owner;` so every object is owned by the group
role, not by whichever human ran the migration. Objects owned by a person break
when that person leaves (`DROP ROLE` fails: `role cannot be dropped because
some objects depend on it`). Fix with
`REASSIGN OWNED BY alice TO app_owner; DROP OWNED BY alice; DROP ROLE alice;`
(run in every database).

## Gotchas
- `SET ROLE` is undone by `RESET ROLE`; inside SECURITY DEFINER functions
  `current_user` is the owner, `session_user` the login (checked: `postgres:svc_api`).
- `SET ROLE` is checked against the session user's own memberships, so a superuser can `SET ROLE` to anything; test `INHERIT FALSE` and `SET FALSE` by logging in as the member.
- Membership cycles are rejected; deep chains are legal but hard to audit.
- `pg_hba.conf` role matching uses `+groupname` for membership.

## Verify
```sql
SELECT r.rolname AS role, m.rolname AS member, a.inherit_option, a.set_option, a.admin_option
FROM pg_auth_members a JOIN pg_roles r ON r.oid=a.roleid JOIN pg_roles m ON m.oid=a.member
ORDER BY 1,2;                                   -- PG16+ columns
SELECT pg_has_role('alice','app_owner','USAGE');  -- false if INHERIT FALSE
```
psql `\du` gives a quick view.

## Checked
PostgreSQL 17.6: the layout script runs; `pg_auth_members` shows `inherit_option = f` for the `WITH INHERIT FALSE` grant and `t` for the others; `pg_has_role('alice','app_owner2','USAGE')` is false while `'MEMBER'` and `'SET'` are true; a cycle (`GRANT app_write TO app_read` after the reverse) fails with `role "app_write" is a member of role "app_read"`; `DROP ROLE` of an object owner fails with `role "alice" cannot be dropped because some objects depend on it` and succeeds after `REASSIGN OWNED BY` + `DROP OWNED BY`. Inherit/SET/ADMIN option semantics and the CREATEROLE change are from the PG16 release notes and role docs; `+groupname` in pg_hba: auth-pg-hba-conf docs ("match any of the roles that are directly or indirectly members of this role").
