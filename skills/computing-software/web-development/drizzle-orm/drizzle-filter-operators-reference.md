---
id: computing-software.web-development.drizzle-orm.drizzle-filter-operators-reference
name: drizzle-filter-operators-reference
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, operators, inarray, like, array-operators]
level: practitioner
status: docs-checked
description: "Reference of Drizzle filter operators: comparison, null and exists checks, inArray, between, like/ilike, boolean combinators and PostgreSQL array operators."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/operators.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: know which operator to import.

All come from `drizzle-orm`, and all values are parameterized.

- Comparison: `eq, ne, gt, gte, lt, lte`. Each accepts a value or another column (`eq(t.c1, t.c2)`).
- Existence: `exists(subquery)`, `notExists(subquery)`.
- Null: `isNull(col)`, `isNotNull(col)`.
- Membership: `inArray(col, [1,2,3])` or `inArray(col, subquery)`, and `notInArray`.
- Range: `between(col, 2, 7)`, `notBetween`.
- Pattern: `like`, `notLike` (case sensitive), `ilike`, `notIlike` (case insensitive), for example `ilike(t.col, '%llo wor%')`.
- Boolean: `not(cond)`, `and(a, b)`, `or(a, b)`. For conditional filters the select page passes `undefined` to `.where()`, as in `.where(term ? ilike(posts.title, term) : undefined)`.
- PostgreSQL arrays: `arrayContains` (column contains all elements of the list), `arrayContained` (the list contains all elements of the column), `arrayOverlaps` (column contains any element of the list). `arrayContains` is also shown with a subquery as the second argument.

```ts
await db.select({ id: posts.id }).from(posts)
  .where(arrayContains(posts.tags, ['Typescript', 'ORM']));
```

Any operator Drizzle lacks can be written with `sql` (see `drizzle-sql-template-operator`); the select page states all filter operators are implemented using the `sql` function.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (operators.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
