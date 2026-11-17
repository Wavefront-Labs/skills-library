---
id: computing-software.web-development.vapor.vapor-fluent-schema-builder
name: vapor-fluent-schema-builder
category: computing-software
field: web-development
product: vapor
tags: [vapor, fluent, fluent-schema, schemabuilder, migration, constraints, foreign-key, swift]
level: practitioner
status: docs-checked
description: "Use Fluent's schema builder: create, update, delete, field types and constraints, unique, foreign keys with actions, and custom SQL defaults."
sources:
  - https://docs.vapor.codes/fluent/schema/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: create and alter tables or collections with `database.schema("name")`, usually inside migrations. The name must match the model's `schema`.

## Actions
- `create()`: new table; field and constraint methods allowed, update/delete methods ignored. Errors if it exists unless `.ignoreExisting()`.
- `update()`: all create, update and delete methods allowed.
- `delete()`: no other methods.

```swift
try await database.schema("planets")
    .id()
    .field("name", .string, .required)
    .field("star_id", .uuid, .required, .references("stars", "id"))
    .create()

try await database.schema("planets").unique(on: "name").deleteField("star_id").update()
```

## Fields
`.field(name, type, constraints...)`; name should match the model key. Types: `.string`, `.int8/16/32/64`, `.uint8/16/32/64`, `.bool`, `.datetime` (recommended for `Date`), `.date` (no time of day), `.float`, `.double`, `.data`, `.uuid`, `.dictionary`, `.array`, `.enum`.

Field constraints: `.required` (no nil), `.references` (foreign key), `.identifier` (primary key), `.sql(...)` for anything else.

- `.id()` adds the default `@ID` field (key `.id`, UUID). Custom: `.field("id", .int, .identifier(auto: true))`.
- `.updateField("age", .double)` changes a type; `.deleteField("age")` removes a field.

## Constraints
- `.unique(on: "email")`; combos: `.unique(on: "first_name", "last_name")` (the combination must be unique). Remove with `.deleteUnique(on: "email")`.
- Custom name: `.unique(on: "email", name: "no_duplicate_emails")`, removed with `.deleteConstraint(name: "no_duplicate_emails")`.

## Foreign keys
Field form: `.field("star_id", .uuid, .required, .references("stars", "id"))`. Top-level form (also usable in `update()`, and nameable): `.foreignKey("star_id", references: "stars", "id", onDelete: .cascade)`.

Actions (`onDelete`/`onUpdate`): `.noAction` (default), `.restrict` (same), `.cascade`, `.setNull`, `.setDefault`.

Warning: these actions run in the database, bypassing Fluent, so model middleware and soft delete may not work correctly.

## Custom SQL
```swift
.field("active", .bool, .required, .sql(.default(true)))
.field("created_at", .datetime, .required, .sql(.default(SQLFunction("now"))))
```

## Space
`try await db.schema("planets", space: "mirror_universe").id().create()` places the table in a model space.

## Checked

2026-11-07. Confirmed against the Vapor docs page(s) fluent/schema, read in full with their code examples; every remaining claim matches the page text.
Method: documentation only; no commands were run.
