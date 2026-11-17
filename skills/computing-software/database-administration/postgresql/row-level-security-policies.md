---
id: computing-software.database-administration.postgresql.row-level-security-policies
name: row-level-security-policies
category: computing-software
field: database-administration
product: postgresql
tags: [database-administration, postgresql, postgres, database-roles, role-privileges, row-level-security, rls, create-policy, multi-tenant, bypassrls, force-row-level-security]
level: advanced
status: verified
description: "Enforce per-tenant or per-user row visibility in PostgreSQL with row-level security policies, without the owner-bypass, leaky-function and index pitfalls."
sources:
  - https://www.postgresql.org/docs/current/ddl-rowsecurity.html
  - https://www.postgresql.org/docs/current/sql-createpolicy.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Row-level security

**Goal:** a query from tenant A can never return tenant B's rows, even if the
application forgets a WHERE clause.

## Setup for a multi-tenant table
```sql
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE invoices FORCE ROW LEVEL SECURITY;    -- apply to the table owner too

CREATE POLICY tenant_isolation ON invoices
  USING (tenant_id = nullif(current_setting('app.tenant_id', true), '')::bigint)
  WITH CHECK (tenant_id = nullif(current_setting('app.tenant_id', true), '')::bigint);
```
App per request/transaction:
```sql
BEGIN;
SET LOCAL app.tenant_id = '42';   -- LOCAL: resets at COMMIT; safe with transaction pooling
SELECT * FROM invoices;           -- only tenant 42
COMMIT;
```

## Semantics to know
- RLS enabled with no policy = default deny (zero rows), not allow.
- `USING` filters rows read/updated/deleted; `WITH CHECK` validates new rows on
  INSERT/UPDATE. Omitting WITH CHECK reuses USING.
- Multiple permissive policies are OR-ed; `AS RESTRICTIVE` policies are AND-ed
  on top (e.g. "and not soft-deleted").
- Policies can be per command (`FOR SELECT`) and per role (`TO app_rw`).
- Superusers and roles with `BYPASSRLS` skip policies; table owners skip unless
  `FORCE ROW LEVEL SECURITY`.

## Gotchas
- `current_setting('app.tenant_id')` raises if unset. `current_setting('app.tenant_id', true)` returns NULL
  only until the setting has been used once in that session; after a `SET LOCAL` ends, the session
  returns an empty string and `''::bigint` raises `invalid input syntax for type bigint: ""`. Write the policy as
  `tenant_id = nullif(current_setting('app.tenant_id', true), '')::bigint` to get zero rows in both cases.
- Session-level `SET` with a transaction-mode pooler leaks tenant context to the
  next client: always `SET LOCAL` or `set_config(..., true)`.
- Performance: the policy predicate is added to every query; index
  `(tenant_id, ...)` on every RLS table. Non-LEAKPROOF functions in user
  predicates are evaluated after the policy, which can block index use.
- `pg_dump` sets `row_security = off`, so by a role that cannot bypass RLS it fails with
  `query would be affected by row-level security policy for table "invoices"` instead of dumping a subset;
  `--enable-row-security` dumps only the visible rows (a partial backup), so use a BYPASSRLS or owner backup role.
- Foreign-key and unique checks are not filtered by RLS; existence of other
  tenants' keys can leak through constraint errors.

## Verify
```sql
SELECT relname, relrowsecurity, relforcerowsecurity FROM pg_class WHERE relname='invoices';
SELECT * FROM pg_policies WHERE tablename='invoices';
```
Test as the app role: with `app.tenant_id` unset, `SELECT count(*)` = 0; with 42
it equals the tenant's count; `INSERT ... tenant_id=43` fails with
`new row violates row-level security policy`.

## Checked
PostgreSQL 17.6: enabling RLS with no policy gave the app role 0 rows; the tenant policy returned 10 of 30 rows after `SET LOCAL app.tenant_id = '42'` and `INSERT ... tenant_id=43` failed with `new row violates row-level security policy for table "invoices"`; after the transaction `current_setting('app.tenant_id', true)` was an empty string and the old policy errored (`invalid input syntax for type bigint: ""`), which is why the policy above uses `nullif`; superuser saw 30 rows even with FORCE, the owner saw 30 without FORCE and 10 with it; a restrictive policy ANDed with a permissive one (10 rows to 3); `pg_dump` as a non-bypass role failed as quoted and `--enable-row-security` dumped the 3 visible rows; `relrowsecurity`/`relforcerowsecurity` and `pg_policies` queries work. Docs (ddl-rowsecurity): default-deny, leakproof ordering, referential-integrity checks bypass RLS. The `nullif` policy text was run: 10 rows with the setting at 42, 0 rows after the transaction ended.
