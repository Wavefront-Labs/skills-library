---
id: computing-software.web-development.drizzle-orm.drizzle-kit-choose-migration-flow
name: drizzle-kit-choose-migration-flow
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, drizzle-kit, migrations, database-first, codebase-first]
level: practitioner
status: docs-checked
description: "Pick among Drizzle's six migration flows: pull, push, generate+migrate, runtime migrate(), generate or export with external tools."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/migrations.mdx
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/kit-overview.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose the migration workflow that fits the team before writing config.

Drizzle works with database-first (the database is the source of truth) and codebase-first (the TypeScript schema is). The migrations page lists six options:

1. Database first, pull only: you manage the schema yourself with external migration tools or direct SQL, and `drizzle-kit pull` saves the current database schema as a TypeScript schema file.
2. Push (code first, no SQL migration files): `drizzle-kit push` pulls the current database schema, generates alterations from the diff and applies them. The docs call it the best approach for rapid prototyping and say dozens of teams and solo developers use it as the primary migrations flow in production.
3. Generate + migrate: `drizzle-kit generate` reads previous migration folders, diffs the schema, prompts for renames if needed and writes a migration folder (`snapshot.json` and `migration.sql`); `drizzle-kit migrate` fetches the migration history from the database, picks previously unapplied migrations and applies them.
4. Generate + runtime migrate: apply generated migrations when the app runs, with `migrate(db)` imported from the driver's migrator (for example `drizzle-orm/node-postgres/migrator`). The docs say this is widely used for monoliths (zero-downtime deployment, rolling back DDL changes if something fails) and in serverless deployments with migrations running in a custom resource once during deployment.
5. Generate + external tool: Drizzle generates the SQL; you apply it directly or via tools such as Bytebase, Liquibase or Atlas.
6. Export + Atlas: `drizzle-kit export` prints the SQL representation of the schema to the console for Atlas or another external SQL migration tool.

Options 2 to 6 are codebase first (the TypeScript schema is the source of truth); option 1 is database first.

The Drizzle Kit CLI commands are: generate, migrate, push, pull, check, up, studio, export. Drizzle Kit is configured through `drizzle.config.ts` or CLI params (at least the SQL dialect and schema path are required), and `--config` selects another config file when you have several database stages or databases.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (migrations.mdx, kit-overview.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
