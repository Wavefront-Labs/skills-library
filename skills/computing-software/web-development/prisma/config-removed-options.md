---
id: computing-software.web-development.prisma.config-removed-options
name: config-removed-options
category: computing-software
field: web-development
product: prisma
tags: [prisma-config-removed-options, prisma, directurl-removed, adapter-removed, studio-config-removed]
level: intro
status: docs-checked
description: "List config options removed in Prisma 7, datasource.directUrl, adapter, engine and studio, and what replaces each."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/reference/prisma-config-reference.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Config options removed in Prisma ORM 7

- `datasource.directUrl`: removed in favour of `url`. (Up to v6.19 it let CLI commands bypass a pooler URL such as pgBouncer.)
- `adapter`: removed. Migrations for driver adapters work automatically in v7 with no extra config. (v6.19 and earlier took a function returning a driver adapter such as `PrismaD1`; D1 was renamed from `PrismaD1HTTP` in 6.11.0.)
- `engine`: removed. (Earlier values were `classic` default and `js`.)
- `studio`: removed, including `studio.adapter`. Run Studio with `npx prisma studio --config ./prisma.config.ts`; it reads the connection from `datasource`.

Related facts on the same page: `datasource.url` is the only datasource key marked required, with default `''`; `shadowDatabaseUrl` also defaults to `''`. The `experimental` block still exists in v7 but now only carries `externalTables` (default `false`).

If old code or tutorials set any of these, delete them. For Prisma 7 the Client side instead needs a driver adapter (see `prisma-client-driver-adapter`).

## Checked
2026-11-03. Confirmed by reading the Prisma ORM v7 docs pages for the topic of this skill (Prisma Migrate getting started, mental model, development and production, baselining, customizing migrations, prototyping, troubleshooting, patching and hotfixing, generating down migrations, squashing, seeding, native types, unsupported features, native functions and extensions, limitations and known issues, and the Prisma Config reference). Commands, flags, error text, privilege lists, defaults and version notes were matched to those pages. Removed: unsupported detail about the exact SQL Server and MySQL lock mechanisms (migrate-deploy-production) and an inferred sentence about v6 experimental keys (config-removed-options).
Method: documentation only; no commands were run.
