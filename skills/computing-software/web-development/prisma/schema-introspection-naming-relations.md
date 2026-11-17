---
id: computing-software.web-development.prisma.schema-introspection-naming-relations
name: schema-introspection-naming-relations
category: computing-software
field: web-development
product: prisma
tags: [prisma-schema-introspection-naming, prisma, identifier-sanitization, duplicate-model-names, introspected-relation-names, relation-disambiguation]
level: practitioner
status: docs-checked
description: "Understand how db pull sanitizes identifiers with @map, how duplicate model names arise, and how it renders one-to-one, one-to-many, many-to-many and named relations."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/introspection.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# What introspection generates

Identifiers must match `[A-Za-z][A-Za-z0-9_]*`. Invalid characters are dropped if they appear before a letter, replaced by underscore after the first letter, and the original name is kept via `@map` or `@@map`. Table `"42User"` with columns `_id`, `_name`, `two$two` becomes `model User` with `@map("_id")`, `@map("_name")`, `two_two ... @map("two$two")` and `@@map("42User")`.

Duplicates: tables `"42User"` and `"24User"` both become `User`. Nothing stops this at pull time; `prisma generate` then fails with `The model "User" cannot be defined because a model with that name already exists.` Rename one model by hand.

Relations come from foreign keys:
- A foreign key column with a `UNIQUE` constraint becomes a one-to-one relation (optional `Profile?` side on the parent).
- Any other foreign key becomes one-to-many (`Post Post[]` on the parent).
- A relation table matching Prisma's conventions is recognised as an implicit many-to-many; otherwise it is rendered as a model, making an explicit many-to-many.
- `name` on `@relation` appears only when needed. Two foreign keys from `Post` to `User` produce names like `"Post_authorToUser"` and `"Post_favoritedByToUser"` and generated field names such as `User_Post_authorToUser`. Rename those Prisma-level fields freely for a nicer Client API; custom relation names survive re-pulls.

Per-database type mappings live on the supported-database pages (PostgreSQL, MySQL, SQLite, SQL Server).

## Checked

Method: 2026-11-08 read the cited introspection.mdx in full (raw file from the prisma/docs repo). The sanitization rules, duplicate-name error, relation rules and disambiguation names match the page. No claims were removed; the wording is unchanged apart from this section.
