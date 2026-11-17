---
id: computing-software.web-development.prisma.schema-models-and-fields
name: schema-models-and-fields
category: computing-software
field: web-development
product: prisma
tags: [prisma-schema-models-fields, prisma, scalar-fields, type-modifiers, map-attribute, unsupported-type]
level: intro
status: docs-checked
description: "Define Prisma models and fields, with type modifiers, optional versus required, scalar lists, @map and @@map to existing tables, and Unsupported types."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/models.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Models and fields in the Prisma schema

A `model` maps to a table in relational databases or a collection in MongoDB, and drives the Prisma Client API (`prisma.user.create(...)`, lower-case model name) and its generated TypeScript types. Naming convention is singular PascalCase.

A field has a name, a type, optional modifiers and optional attributes. Types are scalar (including enums) or another model, which makes it a relation field.

Modifiers: `[]` makes a list and `?` makes it optional. They cannot be combined, so optional lists are not supported. Fields without `?` are required, which is a `NOT NULL` constraint in relational databases. Scalar lists (`keywords String[]`) only work where the connector supports them natively or at the Prisma level.

Mapping names: a database table called `comments` introspects to `model comments`. Keep the convention and map it:

```prisma
model Comment {
  // fields
  @@map("comments")
}
```

`@map` renames a column or enum value, and `@@map` renames an enum or model; they decouple the client API names from database names.

Native type attributes are provider specific, PascalCase and prefixed `@db`, such as `@db.VarChar(200)`; introspection only adds them when the native type differs from the default.

Unsupported types: introspecting a relational database turns unknown column types into `Unsupported("POLYGON")?`. Such fields are absent from Prisma Client's API but can be queried with raw queries. MongoDB has no `Unsupported`.

Every model needs at least one unique identifier, either `@id` / `@@id` or `@unique` / `@@unique`. You can write the model by hand and use Migrate (schema is source of truth) or introspect an existing database (database is source of truth).

## Checked

2026-11-03. Read in the Prisma docs repository (prisma-schema/data-model/models pages, orm/v7): model mapping, naming, type modifiers, optional lists, NOT NULL, scalar-list note, @db native types and introspection rule, Unsupported types, unique identifier rule, source-of-truth workflows.

Method: documentation only; no commands were run.
