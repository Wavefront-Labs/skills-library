---
id: computing-software.database-administration.postgresql.schemas-and-search-path
name: schemas-and-search-path
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, managing-databases, search-path, schemas, public-schema, cve-2018-1058, security-definer, schema-qualification]
level: practitioner
status: verified
description: "Organise PostgreSQL objects into schemas, set search_path per role or database, and close the public-schema and SECURITY DEFINER search_path hijack holes."
sources:
  - https://www.postgresql.org/docs/current/ddl-schemas.html
  - https://www.postgresql.org/docs/current/sql-createfunction.html#SQL-CREATEFUNCTION-SECURITY
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Schemas and search_path

**Goal:** unqualified names resolve to the objects you intend, and no user can
plant a function that hijacks someone else's query.

## Basics
`search_path` is the list of schemas searched for unqualified names; default
`"$user", public`. The first schema that exists is where `CREATE` puts new objects.
```sql
CREATE SCHEMA app AUTHORIZATION app_owner;
ALTER ROLE svc_api IN DATABASE appdb SET search_path = app, public;
ALTER DATABASE appdb SET search_path = app;   -- default for everyone
SHOW search_path;
```
`pg_catalog` is always searched (implicitly before the path unless listed). The session's temporary schema `pg_temp` is searched first unless listed, but only for relation and type names, never for functions or operators (docs: runtime-config-client).

## Lock down public
Before PG15, every role could `CREATE` in `public`, so a low-privilege user could
create objects there that shadow or intercept calls (CVE-2018-1058). PG15 removed `CREATE` for PUBLIC on `public` and made `pg_database_owner` its owner for new databases only; upgraded clusters and restored dumps keep the old settings (PG15 release notes). In
every database created on older versions:
```sql
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
ALTER SCHEMA public OWNER TO pg_database_owner;   -- PG15 default
```

## SECURITY DEFINER functions
They run as the owner, so a caller-controlled search_path is an escalation path.
Always pin it:
```sql
CREATE FUNCTION app.reset_pw(...) RETURNS void
LANGUAGE plpgsql SECURITY DEFINER
SET search_path = pg_catalog, app, pg_temp      -- pg_temp LAST
AS $$ ... $$;
```

## Gotchas
- Extensions install into the first existing schema of search_path at CREATE EXTENSION
  time (`pg_trgm` landed in `app` with `search_path = app`); pin with `CREATE EXTENSION x SCHEMA ext;`.
- `pg_dump` output sets `search_path = ''` and schema-qualifies everything;
  functions relying on an unqualified search_path can break on restore (index
  expressions, check constraints). Schema-qualify inside function bodies or SET search_path on them.
- Precedence checked on 17.6: `ALTER ROLE r IN DATABASE d SET` beats `ALTER ROLE r SET`, which beats `ALTER DATABASE d SET`. Clear with `ALTER ROLE r [IN DATABASE d] RESET search_path`; changes apply to new sessions only.

## Verify
```sql
SELECT has_schema_privilege('public', 'public', 'CREATE');   -- false
SELECT proname, proconfig FROM pg_proc WHERE prosecdef;       -- every row has search_path=
SELECT * FROM pg_db_role_setting;                             -- per-role/db overrides
```

## Checked
PostgreSQL 17.6: default `search_path` is `"$user", public`; a new database has `public` owned by `pg_database_owner` and `has_schema_privilege('public','public','CREATE')` is false; the role/database precedence order and `RESET` behaviour as above; `CREATE EXTENSION` target schema as above; `pg_proc.proconfig` shows `search_path=pg_catalog, app, pg_temp` for a function created with `SET search_path`; `pg_dump -s` output begins `SELECT pg_catalog.set_config('search_path', '', false);` and the function carried `SET search_path TO 'pg_catalog', 'app', 'pg_temp'`. Docs: ddl-schemas, runtime-config-client, PG15 release notes, the CVE-2018-1058 security page.
