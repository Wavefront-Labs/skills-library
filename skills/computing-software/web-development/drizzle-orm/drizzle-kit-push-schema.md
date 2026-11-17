---
id: computing-software.web-development.drizzle-orm.drizzle-kit-push-schema
name: drizzle-kit-push-schema
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, drizzle-kit, push, schema-diff, prototyping]
level: practitioner
status: docs-checked
description: "Use drizzle-kit push to sync a schema straight to the database, preview with --explain, review with --verbose, and filter tables and schemas."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/drizzle-kit-push.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: iterate quickly without SQL files, with safeguards.

`push` reads your schema into a JSON snapshot, introspects the database, generates SQL from the differences and applies it, skipping SQL file generation.

```sh
npx drizzle-kit push
npx drizzle-kit push --explain      # dry run: print planned SQL, do not apply
npx drizzle-kit push --verbose      # print every statement before executing
npx drizzle-kit push --force        # auto-accept data-loss statements
```

Needs `dialect`, `schema` (file(s) or folder(s), glob) and a connection (`url`, or `host`, `port`, `user`, `password`, `database`). Drivers are not bundled; kit picks one installed in your project, and exceptions such as `aws-data-api` and `pglite` need an explicit `driver`.

Scope it with `tablesFilter` (glob, for example `'user*'`, default `"*"`), `schemaFilter` (default `["*"]`), `extensionsFilters` (for example `postgis`). By default push manages all tables and schemas.

The docs say it is the best approach for rapid prototyping, used by dozens of teams as a primary production migrations flow, and pairs well with blue/green deployment and serverless databases like Neon, PlanetScale and Turso.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (drizzle-kit-push.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
