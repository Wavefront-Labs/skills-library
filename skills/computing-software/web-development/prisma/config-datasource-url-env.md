---
id: computing-software.web-development.prisma.config-datasource-url-env
name: config-datasource-url-env
category: computing-software
field: web-development
product: prisma
tags: [prisma-config-datasource-url, prisma, env-helper-throws, process-env-optional, shadow-database-url]
level: practitioner
status: docs-checked
description: "Set datasource.url and shadowDatabaseUrl in prisma.config.ts, and avoid env() throwing on prisma generate when DATABASE_URL is missing."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/reference/prisma-config-reference.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# datasource.url and environment variables

`datasource.url` is required and uses the database's own URL syntax. `datasource.shadowDatabaseUrl` (optional) points Migrate at a separate, possibly cloud-hosted, shadow database.

`env()` from `prisma/config` throws when the variable is missing, typed via `env<Env>("DATABASE_URL")`. Every CLI command loads the config file, but only some commands need the URL (`prisma db *`, `prisma migrate *`, `prisma generate --sql`). So with `env("DATABASE_URL")` and no variable set, even plain `prisma generate` fails:

```
Error: PrismaConfigEnvError: Missing required environment variable: DATABASE_URL
```

Typical in CI that only runs `generate` for type checking. Fix: skip `env()` and read the variable directly:

```ts
datasource: { url: process.env.DATABASE_URL! }, // or ?? '' as a fallback
```

Rule from the docs: use `env()` to enforce a variable exists; use `process.env` when it may be optional depending on the command.

Removed in v7: `datasource.directUrl` (use `url`), plus `adapter`, `engine` and `studio` (see `prisma-config-removed-options`).

The generated client does not read `.env` at runtime (see `prisma-client-generator-setup`), so load variables yourself, for example `dotenv` or an env-file flag, in application code.

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
