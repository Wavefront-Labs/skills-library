---
id: computing-software.database-administration.postgresql.column-level-privileges
name: column-level-privileges
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, column-privileges, grant, privileges, data-protection, least-privilege]
level: practitioner
status: verified
description: "Grant or revoke SELECT/INSERT/UPDATE on specific PostgreSQL columns, understand interaction with table grants, and audit column ACLs."
sources:
  - https://www.postgresql.org/docs/current/sql-grant.html
  - https://www.postgresql.org/docs/current/ddl-priv.html
  - https://www.postgresql.org/docs/current/infoschema-column-privileges.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Column-level privileges

## Grant only some columns
```sql
REVOKE ALL ON customers FROM support;
GRANT SELECT (id, name, email, created_at) ON customers TO support;
GRANT UPDATE (email) ON customers TO support;
GRANT INSERT (name, email) ON customers TO intake;      -- other columns get defaults
```
`SELECT * FROM customers` as support fails with `permission denied for table customers`; selecting granted columns works.

## The rule that bites
A **table-level** grant covers all columns, and revoking a column does not subtract from it:
```sql
GRANT SELECT ON customers TO support;
REVOKE SELECT (ssn) ON customers FROM support;   -- no effect: table grant still allows ssn
```
To hide a column: revoke the table privilege, then grant the allowed columns explicitly. New columns added later are **not** granted automatically (good for sensitive additions, but add them to the grant script).

## Audit
```sql
SELECT grantee, column_name, privilege_type
FROM information_schema.column_privileges
WHERE table_schema = 'public' AND table_name = 'customers' AND grantee <> 'postgres';
```
`\dp customers` in psql shows column ACLs under "Column privileges". Test: `SET ROLE support; SELECT ssn FROM customers;` must error.

## UPDATE/DELETE needs SELECT too
`UPDATE customers SET email = $1 WHERE id = $2` needs `SELECT (id)` as well as `UPDATE (email)`, because the WHERE clause reads id. `RETURNING` needs SELECT on returned columns.

## Alternatives
- A view exposing safe columns (owned by a privileged role) with `GRANT SELECT ON view` — simpler for many consumers, and you can mask (`left(ssn,3)||'***'`).
- Row-level security for row restriction (column grants do not restrict rows).

## Gotchas
- `pg_dump` by a role without full SELECT fails; dump with the owner.
- ORMs selecting all columns break the moment column grants are introduced; list columns explicitly.

## Checked
- PostgreSQL 17.6: `SELECT *` as the column-limited role fails with `permission denied for table customers` while granted columns work; `UPDATE ... WHERE id` works with `SELECT (id)` and `UPDATE (email)`, `RETURNING ssn` is denied; after a table-level `GRANT SELECT`, `REVOKE SELECT (ssn)` changes nothing and `ssn` stays readable; a column added later is not granted; `information_schema.column_privileges` and `\dp` show the column ACLs.
