---
id: computing-software.database-administration.supabase.rls-policies
name: rls-policies
category: computing-software
field: database-administration
product: supabase
tags: [rls, row-level-security, policies, auth-uid, security-invoker]
level: practitioner
status: docs-checked
description: "Write safe Supabase Row Level Security policies: grants, per-operation policies, auth.uid() caching, view and security definer traps, and testing."
sources:
  - https://supabase.com/docs/guides/database/postgres/row-level-security
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: expose tables through the Data API without leaking rows.

Enable RLS on every table in an exposed schema, then add policies. Once RLS is on, the API returns no data with a publishable key until a policy exists.

```sql
alter table public.reports enable row level security;
revoke all on table public.reports from anon, authenticated;
grant select, insert, update, delete on table public.reports to authenticated;
```

Grants are checked before policies: a missing grant fails with `42501` before any policy runs. New tables in `public` receive all privileges for `anon`, `authenticated` and `service_role` on projects that grant by default.

Rules:
- One policy per operation (`select`, `insert`, `update`, `delete`); a `for all` policy hides which operation it covers.
- Always name the role with `to`.
- Without `with check`, the `using` expression controls both row visibility and new rows.
- An `UPDATE` needs a matching `SELECT` policy.
- `auth.uid()` is `null` for unauthenticated requests, so `auth.uid() = user_id` fails silently; add `auth.uid() IS NOT NULL`.

Performance: wrap helpers as `(select auth.uid())` so Postgres caches the result per statement, and lead a btree index with each column the policy filters on.

Traps:
- Views bypass RLS; on Postgres 15 and later set `security_invoker = true`.
- `security definer` functions need `set search_path = ''` and schema-qualified names, and must not live in an exposed schema.
- Policies reading each other's tables raise `42P17` (infinite recursion); break the cycle with a security definer function.
- `raw_user_meta_data` is user-editable; use `raw_app_meta_data` for authorization.
- A JWT stays stale until refreshed.

Test with `supabase test db`. A `using` denial raises no error and matches zero rows, so assert with `is_empty`; prove allowed writes with `returning`, not `lives_ok`.

## Checked

Confirmed against the page: enable RLS and revoke/grant sequence, 42501 on missing grant, default grants on existing projects, per-operation policies, to clause, using vs with check, UPDATE needing a SELECT policy, auth.uid() null behaviour, select-wrapping, btree leading column indexing, security_invoker on Postgres 15+, security definer search_path guidance, 42P17 recursion, user vs app metadata, JWT staleness, supabase test db and is_empty/returning testing advice. Nothing removed.

Method: docs-checked 2026-11-09 against the Supabase docs source for guides/database/postgres/row-level-security (apps/docs/content on GitHub master), read in full.
