---
id: computing-software.web-development.drizzle-orm.drizzle-row-level-security
name: drizzle-row-level-security
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, rls, pgpolicy, pgrole, withrls]
level: advanced
status: docs-checked
description: "Enable PostgreSQL row-level security in Drizzle with withRLS, pgRole, pgPolicy options, link() to provider tables, and Neon or Supabase helpers."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/rls.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: define roles and policies in the schema.

Enable RLS without policies using `pgTable.withRLS('users', {...})`. Quoting the PostgreSQL docs, the page says that with no policy a default-deny policy is used: no rows are visible or can be modified. Operations on the whole table, such as TRUNCATE and REFERENCES, are not subject to row security. If you add a policy to a table, RLS is enabled automatically.

Roles (the page says more options will be added in a future release):

```ts
export const admin = pgRole('admin', { createRole: true, createDb: true, inherit: true });
export const existingAdmin = pgRole('admin').existing();   // drizzle-kit does not see it or include it in migrations
```

Policies are defined in the table's third argument (a callback returning an array):

```ts
pgPolicy('policy', { as: 'permissive', to: admin, for: 'delete', using: sql``, withCheck: sql`` })
```

Options: `as` is `permissive` or `restrictive`; `to` is `public`, `current_role`, `current_user`, `session_user`, any other role name as a string, or a `pgRole` object; `for` is `all`, `select`, `insert`, `update` or `delete`; `using` fills the `USING` part and `withCheck` the `WITH CHECK` part of the policy creation statement.

Policies on existing tables you do not define (such as provider tables) use `.link(table)`:

```ts
import { authenticatedRole, realtimeMessages } from "drizzle-orm/supabase";
pgPolicy("authenticated role insert policy", { for: "insert", to: authenticatedRole, using: sql`` }).link(realtimeMessages);
```

Provider helpers: `drizzle-orm/neon` exports `crudPolicy({ role, read, modify })`, the existing roles `authenticatedRole` and `anonymousRole`, and `authUid`; `drizzle-orm/supabase` exports existing roles `anonRole`, `authenticatedRole`, `serviceRole`, `postgresRole`, `supabaseAuthAdminRole`, plus tables and helpers such as `authUsers`, `realtimeMessages`, `authUid`. For views, set `.with({ securityInvoker: true })` in the view's WITH options.

drizzle-kit does not manage roles by default; enable it in `drizzle.config.ts` with `entities: { roles: true }`, or `roles: { exclude: ['admin'] }`, `roles: { include: ['admin'] }`, or `roles: { provider: 'neon' }` / `'supabase'` (optionally with `exclude`) to skip provider-defined roles (see `drizzle-kit-config-file`).

## Checked

Date: 2026-11-07

Confirmed against `pg/rls.mdx` in the drizzle-orm-docs repo (cloned from main, read in full, all 513 lines including the Neon equivalence example, Supabase sections and the `createDrizzle` wrapper): Enable RLS, Roles, Policies and options table, `.link()`, the Migrations section with `entities.roles`, RLS on views, and the Neon and Supabase helper exports.

Removed: the invented Verify step. Added the `entities.roles` variants from the page. Not summarised: the `createDrizzle` Supabase wrapper example.

Method: documentation only; no commands were run.
