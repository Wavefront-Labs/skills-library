---
id: computing-software.web-development.prisma.schema-introspection-unsupported-warnings
name: schema-introspection-unsupported-warnings
category: computing-software
field: web-development
product: prisma
tags: [prisma-schema-introspection-warnings, prisma, introspection-unsupported-features, check-constraints, row-level-security, expression-indexes]
level: advanced
status: docs-checked
description: "Read db pull warnings for features the Prisma schema cannot express, such as check constraints, RLS and partitioned tables, and apply them through a create-only migration."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/introspection.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Introspection warnings for unsupported features

When `prisma db pull` detects a database feature the schema language cannot express, the CLI prints a warning with a workaround suggestion and adds a comment on the affected model or field. Features it reports:

- Partitioned tables
- PostgreSQL Row Level Security
- Index sort order and `NULLS FIRST` / `NULLS LAST`
- CockroachDB row-level TTL
- Comments
- PostgreSQL deferred constraints
- Check constraints (MySQL and PostgreSQL)
- Exclusion constraints
- MongoDB `$jsonSchema`
- Expression indexes

Workaround for relational databases, to add such a feature through Migrate:

1. `npx prisma migrate dev --create-only` to make a draft migration.
2. Edit the SQL to add the feature the warning named.
3. `npx prisma migrate dev` to apply it.

The page links each listed feature to a Prisma ORM GitHub issue and says features Prisma intends to support are tracked under the `topic:database-functionality` label.

## Checked

Method: 2026-11-08 read the cited introspection.mdx in full (raw file from the prisma/docs repo). The feature list, the comment-plus-warning behaviour and the three-step create-only workaround match the page. Removed the claim that warnings do not stop the pull and two cross-references to other skills, none of which the page states.
