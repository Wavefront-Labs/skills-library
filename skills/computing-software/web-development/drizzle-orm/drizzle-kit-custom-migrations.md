---
id: computing-software.web-development.drizzle-orm.drizzle-kit-custom-migrations
name: drizzle-kit-custom-migrations
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, drizzle-kit, custom-migration, data-seeding, raw-sql]
level: advanced
status: docs-checked
description: "Create empty custom migrations for unsupported DDL or data seeding with generate --custom, and apply them with drizzle-kit migrate."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/kit-custom-migrations.mdx
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/drizzle-kit-generate.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: ship hand-written SQL inside the Drizzle migration chain.

```sh
drizzle-kit generate --custom --name=seed-users
```

This generates an empty migration file in a timestamped folder next to your generated ones (the docs show `20242409135510_seed-users`). Write your SQL in it, then run it with the `drizzle-kit migrate` command.

Use it for:
- DDL alterations currently not supported by Drizzle Kit.
- Data seeding (the docs example is a few `INSERT INTO "users" ("name") VALUES(...)` statements).

Extended example from the docs: schema at `./src/schema.ts`, output folder `./migrations`, config in a `configs` folder:

```sh
npx drizzle-kit generate --config=./configs/drizzle.config.ts --name=seed-users --custom
```

Limitation stated in the docs: running custom JavaScript and TypeScript migration or seeding scripts is announced for an upcoming release (a GitHub discussion tracks it), so for now write SQL.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (kit-custom-migrations.mdx, drizzle-kit-generate.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
