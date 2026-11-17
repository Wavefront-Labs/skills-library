---
id: computing-software.data-engineering.data-modelling.document-modelling-for-mongodb
name: document-modelling-for-mongodb
category: computing-software
field: data-engineering
product: data-modelling
tags: [data-modelling, document-modelling, mongodb, embedding-vs-referencing, schema-design]
level: advanced
status: docs-checked
description: "Model data for document databases like MongoDB: embed vs reference by access pattern, document size limits, common schema patterns, schema validation and analytics impact."
sources:
  - https://www.mongodb.com/docs/manual/data-modeling/
  - https://www.mongodb.com/docs/manual/data-modeling/design-patterns/
  - https://www.mongodb.com/docs/manual/core/schema-validation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Document modelling (MongoDB)

**Goal:** documents shaped by how the application reads and writes, with bounded size and predictable analytics extraction.

## Embed or reference
| Embed when | Reference when |
|---|---|
| data is read together (order + line items) | child set is unbounded (user -> all events) |
| one-to-few, owned by the parent | many-to-many, shared entities (products in orders) |
| updated together atomically | children change independently and often |

## Size limits
The maximum BSON document size is 16 mebibytes. Unbounded arrays (comments, logs) eventually hit it: bound them or move children to a separate collection (see the design patterns page for grouping patterns).

## Common patterns
- **Computed values**: calculate in the database so results are ready when the client requests them.
- **Document and schema versioning**: prepare for schema changes (for example a `schema_version` field).
- **Polymorphic**: different shapes in one collection.
- **Group data**: group data into series to improve performance and account for outliers.
See the MongoDB design patterns page for the full list.

## Validation
Use JSON Schema validation on collections to enforce required fields and types; the schema validation page lists the commands and validation levels.

## Indexes follow queries
Compound indexes follow the ESR guideline (Equality, Sort, Range).

## Analytics impact
- Nested arrays need flattening (explode) in the warehouse.
- Keep field names and types consistent; type drift (string vs number) breaks downstream schemas.

## Verify
Top queries use indexes (check with `explain()`), and the largest production document stays far below the 16 mebibyte limit.

## Checked

2026-10-28. Confirmed: MongoDB limits page (maximum BSON document size is 16 mebibytes), the ESR guideline page, and the design patterns page (computed values, document and schema versioning, polymorphic, group data). Removed: the extended reference, subset and bucket pattern descriptions, the validation code (`$jsonSchema`, `validationLevel`; the fetched validation page did not show them), the transactions and change-stream claims, multikey index note.

Method: documentation only; no commands were run.
