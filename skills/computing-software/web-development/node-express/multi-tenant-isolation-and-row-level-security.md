---
id: computing-software.web-development.node-express.multi-tenant-isolation-and-row-level-security
name: multi-tenant-isolation-and-row-level-security
category: computing-software
field: web-development
product: node-express
tags: [multi-tenant-authorization, row-level-security, tenant-isolation, postgres-rls, saas, authorization]
level: advanced
status: docs-checked
description: "Isolating tenants in SaaS apps: tenant_id scoping in queries, Postgres row-level security with SET LOCAL, pooler pitfalls, caches, jobs, storage and cross-tenant tests."
sources:
  - https://www.postgresql.org/docs/current/ddl-rowsecurity.html
  - https://www.postgresql.org/docs/current/functions-admin.html
  - https://www.pgbouncer.org/config.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-tenant isolation and row-level security

Cross-tenant data leaks are the worst SaaS incident class. Defence in depth: app scoping + database enforcement.

## 1. Tenant context
- Derive the tenant from the authenticated session/token, never from a request parameter alone. Subdomain or path tenant hints must be checked against the user's memberships.
- Put it in request context (AsyncLocalStorage, Django thread-local/contextvar, Rails `Current.tenant`) and make every repository/ORM query use it (default scopes, query builder wrappers).

## 2. Postgres RLS as the backstop
```sql
ALTER TABLE invoices ENABLE ROW LEVEL SECURITY;
ALTER TABLE invoices FORCE ROW LEVEL SECURITY;         -- applies to the table owner too
CREATE POLICY tenant_isolation ON invoices
  USING (tenant_id = current_setting('app.tenant_id')::uuid)
  WITH CHECK (tenant_id = current_setting('app.tenant_id')::uuid);
```
Per request, inside a transaction:
```sql
BEGIN; SET LOCAL app.tenant_id = '6f1c...'; SELECT ... ; COMMIT;
```
- App connects as a non-owner, non-superuser role without `BYPASSRLS`; migrations use a separate owner role.
- With PgBouncer `pool_mode = transaction` the server connection is released after each transaction and reused by other clients, so a session-level `SET` can carry over: use `SET LOCAL` inside the transaction (or `set_config('app.tenant_id', $1, true)`; the third argument is `is_local`).
- If the setting is missing `current_setting` errors; `current_setting('app.tenant_id', true)` (the `missing_ok` argument) returns NULL instead, and a NULL tenant matches no rows.
- Index `tenant_id` first in composite indexes; RLS predicates must be indexable.

## 3. Everything else that holds data
- Caches: prefix keys with tenant (`t:{id}:...`); never cache by URL alone.
- Background jobs: carry `tenant_id` in the payload and set context in the worker.
- Object storage: per-tenant prefixes and signed URLs scoped to them.
- Search indexes, analytics exports, logs: filter by tenant at query time.
- Unique constraints include `tenant_id` (`UNIQUE (tenant_id, email)`).

## 4. Test it
Fixtures with two tenants; for every endpoint, user from tenant B requesting tenant A's ids gets 404. A DB-level test asserts that with `app.tenant_id` set to B, selecting A's rows returns nothing.

## Verify
- [ ] Automated cross-tenant suite in CI; RLS enabled and forced on every tenant table (query `pg_class.relrowsecurity`).

## Checked

2026-10-25 against the PostgreSQL documentation source (postgres/postgres master), the PgBouncer config docs and the OWASP Multi-Tenant Security cheat sheet. Confirmed: FORCE ROW LEVEL SECURITY subjects the table owner to policies; superusers and BYPASSRLS roles always bypass RLS; set_config third argument is is_local; current_setting takes an optional missing_ok argument; pg_class has the relrowsecurity column; PgBouncer transaction pool_mode releases the server connection after each transaction; the OWASP cheat sheet documents shared-table row-level security with PostgreSQL.

Method: documentation only; no commands were run.
