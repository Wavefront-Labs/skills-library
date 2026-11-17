---
id: computing-software.database-administration.postgresql.dropping-roles-reassign-owned
name: dropping-roles-reassign-owned
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, database-roles, reassign-owned, drop-owned, drop-role, offboarding, role-privileges]
level: practitioner
status: verified
description: "Remove a departing user's role cleanly: REASSIGN OWNED and DROP OWNED in every database, then DROP ROLE, avoiding 'role cannot be dropped because some objects depend on it'."
sources:
  - https://www.postgresql.org/docs/current/role-removal.html
  - https://www.postgresql.org/docs/current/sql-reassign-owned.html
  - https://www.postgresql.org/docs/current/sql-drop-owned.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dropping roles: REASSIGN OWNED and DROP OWNED

## Why DROP ROLE fails
```
ERROR:  role "alice" cannot be dropped because some objects depend on it
DETAIL:  owner of table reports.q3
         privileges for schema app
         owner of default privileges on new relations belonging to role alice in schema app
         3 objects in database analytics
```
A role can own objects, hold grants, and have default-privilege entries in **every
database** of the cluster. All must go first.

## Procedure
```sql
-- 0. Stop new logins and kill sessions
ALTER ROLE alice NOLOGIN;
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE usename = 'alice';

-- 1. In EACH database (\c db1, \c db2, ... including postgres):
REASSIGN OWNED BY alice TO app_owner;   -- transfers ownership of objects in this db
DROP OWNED BY alice;                    -- revokes alice's grants + default privileges here
                                        -- (and drops anything still owned by alice)

-- 2. Once, anywhere:
DROP ROLE alice;
```
Loop over databases from the shell:
```bash
for db in $(psql -Atc "select datname from pg_database where datallowconn"); do
  psql -d "$db" -v ON_ERROR_STOP=1 -c 'REASSIGN OWNED BY alice TO app_owner; DROP OWNED BY alice;'
done
psql -c 'DROP ROLE alice;'
```

## Gotchas
- Order matters: run `REASSIGN OWNED` **before** `DROP OWNED`, or `DROP OWNED` deletes the
  objects alice owns (tables included).
- Databases themselves and tablespaces are cluster-wide objects: `REASSIGN OWNED` handles
  them, but if a database is owned by alice and you cannot connect to it
  (`datallowconn = false`), use `ALTER DATABASE x OWNER TO ...` directly.
- You need privileges on both roles (superuser, or membership in both with PG16 rules).
- `REASSIGN OWNED BY postgres` is refused for system objects; never reassign from the
  bootstrap superuser.
- Find what a role owns before acting:
  ```sql
  SELECT n.nspname, c.relname, c.relkind FROM pg_class c
  JOIN pg_namespace n ON n.oid = c.relnamespace
  WHERE c.relowner = 'alice'::regrole;
  ```
- Jobs (pg_cron entries run as alice), PgBouncer userlists and `pg_hba.conf` lines naming
  the user need cleanup outside SQL.

## Verify
`SELECT 1 FROM pg_roles WHERE rolname = 'alice';` returns no row, and applications using
objects formerly owned by alice still work (ownership moved, grants to other roles intact).

## Checked
- PostgreSQL 17.6: `DROP ROLE` fails with the quoted DETAIL kinds (owner of schema, privileges, owner of default privileges); `REASSIGN OWNED` then `DROP OWNED` then `DROP ROLE` succeeds and moves tables and schemas; `DROP OWNED` alone removes tables the role owns; `REASSIGN OWNED BY postgres` is refused ("required by the database system"); a non-superuser needs privileges of both roles (`Only roles with privileges of role ... may reassign objects`); `REASSIGN OWNED` also moved a database owner; `pg_class.relowner` query lists owned objects. A schema owned by the role that contains other roles' tables makes a bare `DROP OWNED` fail with a dependency error.
