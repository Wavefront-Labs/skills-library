---
id: computing-software.web-development.appwrite.appwrite-databases-tables-columns
name: appwrite-databases-tables-columns
category: computing-software
field: web-development
product: appwrite
tags: [appwrite, databases, tables, columns, tablesdb, cli]
level: intro
status: docs-checked
description: "Create databases, tables and typed columns and indexes with the Console, TablesDB Server SDK or CLI."
sources:
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/databases/databases/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/databases/tables/+page.markdoc
  - https://github.com/appwrite/website/blob/main/src/routes/docs/products/databases/ai-suggestions/+page.markdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: stand up a schema.

Hierarchy: a database is the largest unit and holds tables; tables hold rows with identical structure.

Create:
- Console: Databases page > Create database, then Create table.
- Server SDK (Server SDKs require an API key): `tablesDB.create({ databaseId, name })`, `tablesDB.createTable({ databaseId, tableId, name, columns: [...] })`; permissions can also be set in `createTable`.
- CLI: `appwrite init tables`, then `appwrite push tables` to create it from `appwrite.json` settings.

Column types in the docs: `varchar` (maximum 16,383 characters; fully indexable if size is below 768), `text` (16,383), `mediumtext` (4,194,303), `longtext` (1,073,741,823), `integer` (32-bit), `bigint` (64-bit), `float`, `boolean`, `datetime`, `enum`, `ip`, `email`, `url`, `point`, `line`, `polygon` and `relationship`. `string` is deprecated.

Index types: `key`, `unique`, `fulltext` (required for the search query).

AI suggestions: tick it when creating a table in the Console and optionally add context such as e-commerce orders; Appwrite proposes columns and indexes you can edit before clicking Apply.

By default a new table grants no permissions, so nobody can create or read rows until you set them.

Column settings: mark a column `required`, or give it a default; choose single value or array. After creation you can change a column's key, default, size (text columns) and required flag. A varchar can grow without restriction; shrinking it fails unless existing data fits the new size. Appwrite recommends an index for every queried column.


## Checked

2026-11-04. Confirmed against the Appwrite docs pages Databases, Tables and AI suggestions: hierarchy, Console steps, `tablesDB.create` and `createTable` with columns and permissions, the CLI init and push flow, the column type table with limits, the deprecated `string` type, index types, AI suggestions steps and the default of no table permissions. Removed: the generic Verify step.
Method: documentation only; no commands were run.
