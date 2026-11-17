---
id: computing-software.web-development.drizzle-orm.drizzle-kit-config-file
name: drizzle-kit-config-file
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, drizzle-kit, drizzle-config, dbcredentials, tablesfilter]
level: practitioner
status: docs-checked
description: "Configure drizzle.config.ts: dialect, schema, out, driver, dbCredentials, migrations table, introspect casing, filters, entities, verbose and breakpoints."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/drizzle-config-file.mdx
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/kit-overview.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: a complete, correct drizzle-kit config.

The overview page says at least the SQL `dialect` and `schema` path must be provided; the `dbCredentials` option applies to push, pull, migrate and studio.

```ts
import { defineConfig } from "drizzle-kit";
export default defineConfig({
  dialect: "postgresql",
  schema: "./src/db/schema",          // file, folder or glob
  out: "./drizzle",                    // migrations folder, default ./drizzle
  dbCredentials: { url: process.env.DATABASE_URL! },
  migrations: { table: "__drizzle_migrations", schema: "drizzle" }, // defaults
  introspect: { casing: "camel" },     // pull only: camel (default) or preserve
  tablesFilter: ["users", "project1_*"],
  schemaFilter: ["public"],
  extensionsFilters: ["postgis"],
  entities: { roles: { provider: "supabase", exclude: ["admin"] } },
  verbose: true,
  breakpoints: true,
});
```

Notes from the docs:
- `driver` is only needed for exception drivers, which the PostgreSQL page lists as `aws-data-api` and `pglite`; otherwise drizzle-kit picks an available driver from the project based on `dialect`.
- `tablesFilter` and `schemaFilter` take glob-based names (for example `"user*"`, `"tenant_*"`); `tablesFilter`, `schemaFilter` and `extensionsFilters` apply to push and pull. `extensionsFilters` lists installed extensions (such as `postgis`) whose tables drizzle-kit should ignore.
- `breakpoints` (default `true`) embeds `--> statement-breakpoint` in generated SQL, needed for databases that cannot run multiple DDL statements in one transaction (MySQL and SQLite). `verbose` prints all SQL statements during push (default `false`).
- `entities.roles` is off by default; set `true`, or `include`/`exclude` lists, or `provider: "neon" | "supabase"` to skip provider-managed roles (you may also need `exclude` for newer provider roles).
- Use several config files for dev and prod and pass `--config`, for example `drizzle-kit generate --config=drizzle-dev.config.ts`.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (drizzle-config-file.mdx, kit-overview.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
