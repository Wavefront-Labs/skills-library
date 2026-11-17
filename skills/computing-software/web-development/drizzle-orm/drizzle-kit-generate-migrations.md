---
id: computing-software.web-development.drizzle-orm.drizzle-kit-generate-migrations
name: drizzle-kit-generate-migrations
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, drizzle-kit, generate, migration-sql, snapshot-json]
level: practitioner
status: docs-checked
description: "Run drizzle-kit generate: how snapshots and diffs work, naming with --name, empty --custom migrations, --ignore-conflicts and CLI-only config."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/drizzle-kit-generate.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: produce correct SQL migration files from a schema change.

What it does: reads your schema, composes a JSON snapshot, compares it with the latest snapshot in the migrations folder, writes `migration.sql` and `snapshot.json` into a new timestamped folder. It prompts you when it cannot tell a rename from a drop plus add.

```sh
npx drizzle-kit generate
npx drizzle-kit generate --name=init
npx drizzle-kit generate --custom --name=seed-users
npx drizzle-kit generate --config=./configs/drizzle.config.ts
```

Needs `dialect` and `schema` (file, folder or glob). Options: `out` (default `./drizzle`), `breakpoints` (default true), `driver`, `config`.

Folder layout: `drizzle/20242409125510_init/{migration.sql,snapshot.json}`.

`--custom` creates an empty migration for DDL Drizzle Kit cannot express or for data seeding (see `drizzle-kit-custom-migrations`).

`--ignore-conflicts` skips the commutativity conflict check; the docs say you probably hit a bug if you need it, and ask you to report it.

Apply the output with `drizzle-kit migrate`, drizzle-orm's `migrate()`, external tools like Bytebase, or by running the migrations yourself directly on the database.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (drizzle-kit-generate.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
