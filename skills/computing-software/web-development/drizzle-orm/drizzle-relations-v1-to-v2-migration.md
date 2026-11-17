---
id: computing-software.web-development.drizzle-orm.drizzle-relations-v1-to-v2-migration
name: drizzle-relations-v1-to-v2-migration
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, relations, migration, rqb-v2, drizzle-kit-pull]
level: advanced
status: docs-checked
description: "Migrate from relations() and callback where to defineRelations and object where, using drizzle-kit pull or manual conversion."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/relations-v1-v2.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: upgrade relational queries to v2.

The guide targets `drizzle-orm@rc` and `drizzle-kit@rc`. Import change: `import { relations } from 'drizzle-orm'` (0.x) becomes `import { defineRelations } from 'drizzle-orm'`. Early v1 betas exposed the legacy function as `drizzle-orm/_relations`; the guide says RQB v1 support has been removed from the database drivers in rc.5.

Differences to plan for:
1. One relations object instead of one `relations(table, ...)` per table; `drizzle(url, { relations })` replaces `drizzle(url, { schema })`. Parts can be split with `defineRelationsPart` and merged as `{ relations: { ...relations, ...part } }`.
2. `fields`/`references` become `from`/`to` (single value or array); `relationName` becomes `alias`; new `through` for many-to-many, `optional: false` (removes `null` from the inferred type, creates no database constraint) and a `where` on a relation for predefined filters.
3. No `mode` option in `drizzle()` for MySQL any more.
4. `where` becomes an object (`where: (users, { eq }) => eq(users.id, 1)` becomes `where: { id: 1 }`); `orderBy` accepts objects (`{ id: 'asc' }`) and the callback form still works.
5. Offset works on nested relations; you can filter by relations.
6. Custom types gain a `codec` function.

Migration options: Option 1 is `drizzle-kit pull`, which in the new version can pull a `relations.ts` in the new syntax (written to `drizzle/relations.ts`; move it to your own relations file, point its `./schema` import at a file holding all your tables, and pass `relations` instead of `schema` to `drizzle()`); Option 2 is manual conversion using the Drizzle Relations docs.

After converting definitions, migrate queries:
- Convert `where` statements to the object form (`AND`, `OR`, `NOT`, `RAW` and the previous operators).
- From `1.0.0-rc.5` an explicit `undefined` in a relational filter throws; omit the field or use `EmptyFilter` from `drizzle-orm/relations`.
- Relation existence: `where: { posts: true }` requires a related row, `{ posts: false }` requires none; from rc.5 `{ posts: {} }` skips the filter.
- Convert `orderBy` (the callback form needs no change); ordering by related rows uses forms such as `orderBy: { posts: 'desc(count)' }`.
- From rc.5 the default `optimized` query strategy can nest relation subqueries differently, so raw SQL in `where` or `orderBy` that refers to generated relation aliases may stop working; prefer relation filters and ordering, or opt out per root query with `strategy: 'basic'`.
- Replace manual junction-table queries with a `through` relation.

## Checked

Date: 2026-11-07

Confirmed against `pg/relations-v1-v2.mdx` in the drizzle-orm-docs repo (cloned from main, read in full, all 1156 lines including code callouts): import changes and legacy `_relations` note, one place for relations and `defineRelationsPart`, `from`/`to`, `alias`, `optional`, `through`, predefined `where`, mode removal, object `where`, callback `orderBy` still supported, nested offset, codec, both migration options, rc.5 undefined/`EmptyFilter`, relation existence checks, order by related rows, raw SQL and `strategy: 'basic'`, many-to-many migration.

Removed: the instruction to check that raw SQL references "use the callback parameter" (the page actually warns about generated relation aliases and offers `strategy: 'basic'`), the vague "writes the relations definition" phrasing for pull, and the invented Verify step.

Method: documentation only; no commands were run.
