---
id: computing-software.database-administration.postgresql.alter-default-privileges
name: alter-default-privileges
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, database-roles, role-privileges, alter-default-privileges, grant, schema-privileges, read-only-user, permission-denied]
level: practitioner
status: verified
description: "Make grants apply to tables created in future with ALTER DEFAULT PRIVILEGES, and avoid the classic trap where they only apply to objects made by one role."
sources:
  - https://www.postgresql.org/docs/current/sql-alterdefaultprivileges.html
  - https://www.postgresql.org/docs/current/ddl-priv.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ALTER DEFAULT PRIVILEGES

**Goal:** a read-only role that keeps working after the next migration adds tables.

## The problem
`GRANT SELECT ON ALL TABLES IN SCHEMA app TO app_read;` covers tables that exist
**now**. The next `CREATE TABLE` produces `permission denied for table x` for
the reporting user.

## The fix: default privileges, per creating role
```sql
-- Existing objects
GRANT USAGE ON SCHEMA app TO app_read;
GRANT SELECT ON ALL TABLES IN SCHEMA app TO app_read;
GRANT SELECT ON ALL SEQUENCES IN SCHEMA app TO app_read;

-- Future objects created BY app_owner in schema app
ALTER DEFAULT PRIVILEGES FOR ROLE app_owner IN SCHEMA app
  GRANT SELECT ON TABLES TO app_read;
ALTER DEFAULT PRIVILEGES FOR ROLE app_owner IN SCHEMA app
  GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO app_write;
ALTER DEFAULT PRIVILEGES FOR ROLE app_owner IN SCHEMA app
  GRANT USAGE, SELECT ON SEQUENCES TO app_write;
ALTER DEFAULT PRIVILEGES FOR ROLE app_owner
  REVOKE EXECUTE ON FUNCTIONS FROM PUBLIC;
```

## The trap
Default privileges attach to the **role that creates the object** (`FOR ROLE`,
defaulting to the role running the ALTER). If a human or CI user creates the
table instead of `app_owner`, none of the defaults fire. Either:
- always create objects as the owner role (`SET ROLE app_owner;` at the start of
  migrations), or
- add a default-privileges entry for each creating role.
You must be a member of the target role to `ALTER DEFAULT PRIVILEGES FOR ROLE` it.

## Shortcut for read-only everything (PG14+)
`GRANT pg_read_all_data TO reporting;` reads every table in every schema,
present and future, without default privileges (bypasses grants, not RLS).

## Gotchas
- Defaults are per database; run them in each database.
- Schema `USAGE` is still needed; default privileges on tables do not grant it.
- `DROP ROLE` fails while it has default-privilege entries; `DROP OWNED BY` clears them.

## Verify
```sql
\ddp                      -- psql: list default privileges
SELECT has_table_privilege('app_read', 'app.new_table', 'SELECT');
```
Create a test table as `app_owner` and query it as `app_read`.

## Checked
- PostgreSQL 17.6 with roles `app_owner`, `app_read`, `app_write`: a grant on existing tables misses the next table; defaults fire for tables created by `app_owner` but not for a superuser-created table; `ALTER DEFAULT PRIVILEGES FOR ROLE app_owner` by a non-member fails with `permission denied to change default privileges` and works after `GRANT app_owner`; `\ddp` output matches; `pg_read_all_data` reads a table with no grant but still returns zero rows under forced RLS; `DROP ROLE` lists the default-privilege entries and succeeds after `DROP OWNED BY`.
