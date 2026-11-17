---
id: computing-software.web-development.prisma.schema-datasource-block
name: schema-datasource-block
category: computing-software
field: web-development
product: prisma
tags: [prisma-schema-datasource, prisma, datasource-provider, one-datasource, connection-in-config]
level: intro
status: docs-checked
description: "Declare the single datasource block with a provider in Prisma 7, keep the connection URL in prisma.config.ts, and know where TLS options live."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/overview/data-sources.mdx", "https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/overview/generators.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# The datasource block in Prisma 7

```prisma
datasource db {
  provider = "postgresql"
}
```

A schema can have only one datasource. In v7 the block holds the `provider`; connection details such as the URL are configured in Prisma Config (`datasource.url` in `prisma.config.ts`, usually `env("DATABASE_URL")`; see `prisma-config-datasource-url`).

Things you can still do with one datasource:

- Override the database connection when creating `PrismaClient` (documented in the client reference; for adapters see `prisma-client-driver-adapter`).
- Specify a different database for Prisma Migrate's shadow database if you work with cloud-hosted development databases (see `prisma-migrate-shadow-database`).

TLS and SSL: certificate locations go in the connection configuration for providers that support them, and the docs point to the PostgreSQL, MySQL and SQL Server pages for the exact options, shown as Prisma Config examples.

A second `datasource` block is not allowed: the docs state a Prisma schema can only have one data source.

## Checked

2026-11-03. Read in the Prisma docs repository (prisma-schema/overview/data-sources pages, orm/v7): single datasource with provider, connection details in Prisma Config, connection override, shadow database, TLS pointers. Removed an unconfirmed shadowDatabaseUrl key and a cross-page remark.

Method: documentation only; no commands were run.
