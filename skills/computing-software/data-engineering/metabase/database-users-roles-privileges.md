---
id: computing-software.data-engineering.metabase.database-users-roles-privileges
name: database-users-roles-privileges
category: computing-software
field: data-engineering
product: metabase
tags: [database-privileges, read-only-user, pg-read-all-data, writable-connection, roles]
level: practitioner
status: docs-checked
description: "Give Metabase a least-privilege database user: read-only grants, roles, Postgres pg_read_all_data, and separate writable connections for transforms, uploads and persistence."
sources:
  - https://www.metabase.com/docs/latest/databases/users-roles-privileges
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Recommended setup: create a dedicated `metabase` user with read-only access, limited to the schemas and tables used for analysis. Metabase needs `CONNECT` on the database and `SELECT` on the relevant schemas or tables. Bundle privileges into roles (for example an `analytics` role) so they are easier to manage and reuse.

Postgres grant options: `pg_read_all_data` (Postgres 14+), or `SELECT` at database, schema or table level. Optionally add `TEMPORARY` for temp tables or `EXECUTE` for stored procedures and functions.

Write access: actions, editable tables, uploads, transforms and model persistence each need separate write roles. Use a separate writable connection and grant write roles only to that connection's user.

Gotchas:
- Granting all privileges is suitable only for local development or testing; avoid it in production.
- Any user with a role inherits all of that role's privileges.
- Model persistence needs `CREATE` on the database unless you add the schema manually first.
- Transforms may need `CREATE SCHEMA` (or `CREATE DATABASE` for ClickHouse).

The page recommends a separate writable connection for any operation needing write access, granting the write role only to that connection's user. Role names it uses: `metabase_transforms`, `metabase_uploads`, `metabase_model_persistence` and (for actions and editable tables) `metabase_writer`. For multi-tenant SQL access it suggests one database connection and user per customer.

## Checked

Method: 2026-11-08 read the cited page in full as raw markdown from the Metabase docs repository. Replaced an unsupported security rationale with the page's own recommendations. Otherwise unchanged.
