---
id: computing-software.web-development.drizzle-orm.drizzle-kit-pull-introspect
name: drizzle-kit-pull-introspect
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, drizzle-kit, pull, introspection, database-first]
level: practitioner
status: docs-checked
description: "Introspect an existing database into a Drizzle schema with drizzle-kit pull, control camel versus preserve casing, and filter what is pulled."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/drizzle-kit-pull.mdx
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/drizzle-config-file.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: turn an existing database into schema.ts.

`drizzle-kit pull` reads the database DDL and writes a Drizzle schema file into the `out` folder. Use it when another tool or team manages the database, or to adopt Drizzle on an existing project.

```ts
export default defineConfig({
  dialect: "postgresql",
  dbCredentials: { url: "postgresql://user:password@host:port/dbname" },
  introspect: { casing: "camel" },
});
```

```sh
npx drizzle-kit pull
npx drizzle-kit pull --dialect=postgresql --url=postgresql://user:password@host:port/dbname
```

Casing: the CLI option `introspect-casing` sets the strategy for JS keys of columns and tables; values are `preserve` or `camel`.

Filters (glob-based): `tablesFilter` (default `"*"`), `schemaFilter` (default `"*"`), `extensionsFilters` (installed extensions such as `["postgis"]`, default `[]`).

`--init` marks the pulled schema as an applied migration in your database, so later migrations are diffed against the initial one:

```sh
npx drizzle-kit pull --init
```

Needs `dialect` plus a connection `url` or `user`, `password`, `host`, `port`, `database`. Drivers are not bundled; `aws-data-api` and `pglite` need an explicit `driver`. `--config` selects another config file; `out` defaults to `./drizzle`.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (drizzle-kit-pull.mdx, drizzle-config-file.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
