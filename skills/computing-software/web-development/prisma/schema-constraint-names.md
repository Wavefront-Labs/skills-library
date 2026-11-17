---
id: computing-software.web-development.prisma.schema-constraint-names
name: schema-constraint-names
category: computing-software
field: web-development
product: prisma
tags: [prisma-schema-constraint-names, prisma, default-constraint-naming, custom-index-name, composite-id-name, pkey-fkey-idx]
level: practitioner
status: docs-checked
description: "Control constraint and index names with the map argument, know the default naming convention and trimming rule, and rename compound id and unique selectors with name."
sources: ["https://github.com/prisma/docs/blob/main/apps/docs/content/docs/orm/v7/prisma-schema/data-model/database-mapping.mdx"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Constraint and index names

`map` sets the underlying database name on `@id`, `@@id`, `@unique`, `@@unique`, `@@index` and `@relation`. Reasons given: company policy, conventions of other tools.

Default convention (aligned with PostgreSQL, deterministic):

- Primary key: `{table}_pkey`
- Unique constraint: `{table}_{columns}_key`
- Non-unique index: `{table}_{columns}_idx`
- Foreign key: `{table}_{columns}_fkey`

Default names are generated from the database names of tables and columns: if a model or field is remapped with `@@map` or `@map`, the generated name still uses the table or column name in the database. If a name exceeds the database limit, the part before the suffix is shortened so the whole name fits.

Introspection renders `map` only when a name differs from the convention; matching names are omitted, and a later migrate re-infers and persists them.

Custom names:

```prisma
model User {
  id Int @id(map: "Custom_Primary_Key_Constraint_Name") @default(autoincrement())
}
model Post {
  @@index([title, authorName], map: "My_Custom_Index_Name")
}
```

Note: the page's worked example tables list primary keys as `User_pk` and `Post_pk`, while its convention table says `{tablename}_pkey`. The page does not explain the difference.

Client API names are separate: `@@id` and `@@unique` take `name`. For `@@id([firstName, lastName])` the selector is `firstName_lastName`; with `@@id([firstName, lastName], name: "fullName")` it is `where: { fullName: { firstName: "Paul", lastName: "Panther" } }`.

## Checked

Method: 2026-11-08 read the cited database-mapping.mdx in full (raw file from the prisma/docs repo). The map argument, convention table, trimming rule, introspection behaviour and the name argument on @@id match the page. Corrected the earlier claim that @@map and @map change generated names (the page says defaults use the database names); replaced the unsupported "trust the convention table" advice with a plain note of the page's inconsistency.
