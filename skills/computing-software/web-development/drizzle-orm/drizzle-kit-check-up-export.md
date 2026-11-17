---
id: computing-software.web-development.drizzle-orm.drizzle-kit-check-up-export
name: drizzle-kit-check-up-export
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, drizzle-kit, check, up, export]
level: practitioner
status: docs-checked
description: "Use the utility commands: check for migration collisions in teams, up to upgrade old snapshots, and export to print schema DDL for external tools."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/drizzle-kit-check.mdx
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/drizzle-kit-up.mdx
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/drizzle-kit-export.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: maintain a healthy migrations folder.

drizzle-kit check: checks the consistency of your generated SQL migrations history, useful when several developers change the schema on different branches. Needs `dialect` (config file or CLI); optional `out` (default `./drizzle`) and `config` (default `drizzle.config.ts`). `--ignore-conflicts` makes it skip the commutativity checks; the docs say needing it probably means drizzle-kit checked the migrations wrongly, and ask you to report it.

```sh
npx drizzle-kit check --dialect=postgresql --out=./migrations-folder
```

drizzle-kit up: upgrades drizzle schema snapshots to a newer version; required whenever breaking changes are made to the JSON snapshots and the internal version is upgraded. Needs `dialect`; optional `out` and `config`.

```sh
npx drizzle-kit up --dialect=postgresql
```

drizzle-kit export: reads the schema file(s), composes a JSON snapshot, and prints the SQL DDL to the console, so external tools such as Atlas can handle the migrations.

```sh
npx drizzle-kit export --dialect=postgresql --schema=./src/schema.ts --sql
```

Needs `dialect` and `schema` (a glob of path(s) or folder(s)); optional `config`. The CLI-only `--sql` option generates the SQL representation; by default Drizzle Kit outputs SQL, and other formats may come in future.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (drizzle-kit-check.mdx, drizzle-kit-up.mdx, drizzle-kit-export.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
