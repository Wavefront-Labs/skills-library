---
id: computing-software.web-development.prisma.migrate-seeding
name: migrate-seeding
category: computing-software
field: web-development
product: prisma
tags: [prisma-migrate-seeding, prisma, db-seed, migrations-seed-config, seed-user-arguments]
level: practitioner
status: docs-checked
description: "Seed data with prisma db seed and migrations.seed in prisma.config.ts, a driver-adapter seed.ts, raw SQL seeds, shell seeds and custom arguments after --."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/workflows/seeding.mdx", "https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/understanding-prisma-migrate/limitations-and-known-issues.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Seeding with prisma db seed

Set the command in `prisma.config.ts` under `migrations.seed`; `prisma db seed` runs whatever string you give:

```ts
export default defineConfig({
  schema: "prisma/schema.prisma",
  migrations: { path: "prisma/migrations", seed: "tsx prisma/seed.ts" },
  datasource: { url: env("DATABASE_URL") },
});
```

In v7 seeding only happens when you run `npx prisma db seed`; automatic seeding during `migrate dev` or `migrate reset` was removed. Another docs page still says a reset triggers a seed script found in the config, so test your own setup.

In `seed.ts`, `PrismaClient` needs a driver adapter in v7. The doc example builds `new Pool({ connectionString })` from `pg`, wraps it with `new PrismaPg(pool)` from `@prisma/adapter-pg`, passes `{ adapter }` to `PrismaClient` imported from your generated client path, uses `upsert` with `update: {}` so reruns are safe, and calls `prisma.$disconnect()` and `pool.end()` in both success and error paths. Dev dependencies listed: `typescript`, `tsx`, `@types/node`, `@prisma/adapter-pg`, `pg`, `@types/pg`, `dotenv`. For plain JavaScript run `node prisma/seed.js`.

Raw SQL: use `prisma.$executeRaw` with tagged template SQL such as `INSERT ... ON CONFLICT DO NOTHING`, chained after `main()`. Non-JS seeds: a `seed.sh` can call a Go program or `psql file.sql`.

Custom arguments: parse them with `node:util` `parseArgs` and pass them after the delimiter, `npx prisma db seed -- --environment development`.

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
