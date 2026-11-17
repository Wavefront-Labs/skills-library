---
id: computing-software.database-administration.sql.default-privileges-and-roles
name: default-privileges-and-roles
category: computing-software
field: database-administration
product: sql
tags: [sql, default-privileges-and-roles]
level: practitioner
status: docs-checked
description: "Grant via group roles and ALTER DEFAULT PRIVILEGES in PostgreSQL."
sources: ["https://www.postgresql.org/docs/current/sql-alterdefaultprivileges.html", "https://www.postgresql.org/docs/current/ddl-priv.html", "https://www.postgresql.org/docs/current/sql-grant.html", "https://www.postgresql.org/docs/current/sql-createrole.html", "https://www.postgresql.org/docs/current/ddl-schemas.html", "https://www.postgresql.org/docs/current/functions-info.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Roles default privileges and group roles

- `CREATE ROLE app_ro NOLOGIN; GRANT USAGE ON SCHEMA s TO app_ro; GRANT SELECT ON ALL TABLES IN SCHEMA s TO app_ro; GRANT app_ro TO alice;` A role without `LOGIN` is useful for managing privileges and is not a user in the usual sense; `NOLOGIN` is the `CREATE ROLE` default.
- Future tables: `ALTER DEFAULT PRIVILEGES IN SCHEMA s GRANT SELECT ON TABLES TO app_ro;` It does not affect existing objects. It applies to objects later created by the target role (`FOR ROLE r`, else the role that ran it), and is not inherited from roles the creator is a member of.
- Revoke PUBLIC defaults: `REVOKE ALL ON DATABASE d FROM PUBLIC;` (PUBLIC has `CONNECT` and `TEMPORARY` on a database by default). Before PostgreSQL 15, or in a database upgraded from an earlier version, also run `REVOKE CREATE ON SCHEMA public FROM PUBLIC`.
- Self-check: `\dp` (and `\ddp` for default privileges) or `has_table_privilege('alice','s.t','SELECT')`.

## Checked

Date: 2026-11-07. Read the whole ALTER DEFAULT PRIVILEGES page; read Table 5.2 and the PUBLIC passages of the Privileges page (ddl-priv, remainder located by search); searched GRANT (ALL TABLES IN SCHEMA, ON DATABASE, GRANT role TO role), CREATE ROLE (NOLOGIN text), the Schemas page (the "PostgreSQL 15 and later" passage) and the has_table_privilege examples on System Information Functions. Confirmed: target-role and no-inheritance rule, existing objects unaffected, \ddp, database PUBLIC default Tc, the version-15 schema change. Corrected: "on PostgreSQL 14 and older" now says before 15 or upgraded databases, per the page. Added the no-inheritance rule, \ddp and the NOLOGIN default from the pages.
Method: documentation only; no commands were run.
