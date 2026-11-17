---
id: computing-software.database-administration.sql.sql-privileges-grant-and-revoke
name: sql-privileges-grant-and-revoke
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-privileges, grant-revoke, roles, least-privilege, row-level-security]
level: practitioner
status: docs-checked
description: "Apply least privilege in PostgreSQL with roles, GRANT and REVOKE, default privileges, the public schema and row-level security."
sources: ["https://www.postgresql.org/docs/current/ddl-priv.html", "https://www.postgresql.org/docs/current/sql-grant.html", "https://www.postgresql.org/docs/current/sql-alterdefaultprivileges.html", "https://www.postgresql.org/docs/current/ddl-schemas.html", "https://www.postgresql.org/docs/current/ddl-rowsecurity.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Privileges (PostgreSQL)

- A new object belongs to the role that created it; initially only the owner (or a superuser) can use it. Create group roles for functions (for example `app_read`, `app_write`, `migrator`) and grant roles to login users (`GRANT admins TO joe;`). Privileges are the sum of those granted directly, via roles the user is a member of, and to `PUBLIC`. The application should not connect as the table owner or a superuser.
- Grant narrowly: `GRANT SELECT, INSERT, UPDATE ON orders TO app_write;`. Avoid `GRANT ALL PRIVILEGES` to application roles. Owners and superusers can always grant; `WITH GRANT OPTION` lets a recipient grant onward, and revoking it removes the chain.
- Column-level privileges: `GRANT SELECT (col1), UPDATE (col1) ON mytable TO miriam_rw;`.
- `ALTER DEFAULT PRIVILEGES IN SCHEMA s GRANT SELECT ON TABLES TO app_read;` sets privileges for objects created later; it does not change existing objects. It applies to objects created by the role running the command (or named with `FOR ROLE`), not those created by roles it is a member of. For existing tables use `GRANT ... ON ALL TABLES IN SCHEMA s TO role`.
- `PUBLIC` means all roles, including those created later. By default `PUBLIC` holds `CONNECT` and `TEMPORARY` on databases (`Tc`) and `USAGE` on schema `public`; use `REVOKE ... FROM PUBLIC` where that is too broad.
- Schema `public`: in PostgreSQL 15 and later the default does not give everyone `CREATE` on it; in databases upgraded from 14 or earlier, run `REVOKE CREATE ON SCHEMA public FROM PUBLIC;`.
- Row-level security: enable it per table and add policies with `CREATE POLICY`; policies are restricted to a role, or to `PUBLIC` for all users. Superusers and roles with `BYPASSRLS` always bypass it, and table owners bypass it unless the table has `ALTER TABLE ... FORCE ROW LEVEL SECURITY`. Referential-integrity checks bypass row security.
- Inspect grants with psql `\dp` (tables), `\l` (databases), `\dn+` (schemas); revoke with `REVOKE ... FROM role`.
- Rotate credentials and restrict network access; these are operational controls outside SQL.

## Checked

2026-11-08. Confirmed against the PostgreSQL 18 pages "Privileges" (ownership, PUBLIC defaults table, column grants, `\dp`), "GRANT" (PUBLIC, role membership, ALL TABLES IN SCHEMA, ALL PRIVILEGES), "ALTER DEFAULT PRIVILEGES" (future objects only, creating-role rule), "Schemas" (public schema CREATE, PostgreSQL 15 default) and "Row Security Policies" (bypass rules, FORCE, referential integrity). Removed as unconfirmed: SQL Server security policies, Oracle VPD, `information_schema.table_privileges`, and the PostgreSQL 15 wording "default since PostgreSQL 15" as a blanket `PUBLIC` claim (restated precisely above).
Method: documentation only; no commands were run.
