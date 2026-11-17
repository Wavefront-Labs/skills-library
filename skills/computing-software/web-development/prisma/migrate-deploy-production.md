---
id: computing-software.web-development.prisma.migrate-deploy-production
name: migrate-deploy-production
category: computing-software
field: web-development
product: prisma
tags: [prisma-migrate-deploy-production, prisma, migrate-deploy, advisory-lock, prisma-schema-disable-advisory-lock]
level: practitioner
status: docs-checked
description: "Apply migrations in staging and production with migrate deploy from CI, what it does not check, and the 10 second advisory lock with its disable variable."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-migrate/workflows/development-and-production.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# migrate deploy in production

```
npx prisma migrate deploy
```

Use it in testing and production, as part of an automated CI/CD pipeline; the docs do not recommend running it locally against a production database. It compares applied migrations with the history, warns if any applied migration was modified (output lists the migration names), and applies pending migrations.

What it does not do:

- warn if an applied migration is missing from the history
- detect drift, such as a production hotfix that differs from the history end state
- reset the database or generate artifacts like Prisma Client
- use a shadow database


Advisory locking: `migrate deploy`, `migrate dev` and `migrate resolve` take an advisory lock so two runs cannot overlap, for instance when two pull requests merge in quick succession. The timeout is 10 seconds and not configurable. It uses the default advisory locking mechanism of the underlying provider (PostgreSQL, MySQL, Microsoft SQL Server). If a command times out, run it again. Since 5.3.0 you can disable locking with the `PRISMA_SCHEMA_DISABLE_ADVISORY_LOCK` environment variable.

If a deploy fails partway, see `prisma-migrate-failed-migration-recovery`. If you applied a manual production fix, see `prisma-migrate-hotfix-resolve`.

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
