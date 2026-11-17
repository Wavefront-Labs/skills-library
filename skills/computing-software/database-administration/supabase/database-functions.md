---
id: computing-software.database-administration.supabase.database-functions
name: database-functions
category: computing-software
field: database-administration
product: supabase
tags: [functions, security-definer, search-path, execute-privilege, plpgsql]
level: practitioner
status: docs-checked
description: "Write Supabase Postgres functions safely: invoker vs definer, pinned search_path, and revoking execute from public and anon."
sources:
  - https://supabase.com/docs/guides/database/functions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: ship database functions that callers cannot abuse.

Rules:
- Overloaded functions are not supported; give every function a unique name.
- Use `create or replace` when the function may not exist, and `returns void` when nothing is returned.
- A function returns the result of its final query, which may be an `insert`, `update` or `delete` with `returning`.
- Set-returning functions accept filters, e.g. `select * from get_planets() where id = 1;`.

Invoker vs definer: prefer `security invoker` (the default). A `security definer` function runs with its creator's privileges, so it can return rows the caller cannot read, and it must set `search_path`. With `search_path = ''`, schema-qualify every relation, such as `from public.table`. Functions created in the Dashboard or by a migration are owned by `postgres`, which bypasses RLS.

Who may call: any role can call a function by default, including `anon`. Pinning `search_path` does not change that, and an execute grant does not limit the rows a permitted role receives, so check ownership in the body. Narrow execution:

```sql
revoke execute on function public.hello_world from public;
revoke execute on function public.hello_world from anon;
revoke execute on all functions in schema public from public;
revoke execute on all functions in schema public from anon, authenticated;
alter default privileges revoke execute on functions from public;
alter default privileges in schema public revoke execute on functions from anon, authenticated;
grant execute on function public.hello_world to authenticated;
```

Omit `in schema` on the first default-privileges statement: a revoke limited to one schema has no effect on a global default. Grant `execute` on each new function to its callers, including helpers that RLS policies call.

## Checked

2026-11-04: Read the Database functions guide in full and compared every rule and SQL statement. All confirmed; nothing removed.
Method: documentation only; no commands were run.
