---
id: computing-software.web-development.drizzle-orm.drizzle-update-set-and-from
name: drizzle-update-set-and-from
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, update, set, update-from, returning]
level: practitioner
status: docs-checked
description: "Update rows with Drizzle: set values and SQL expressions, null versus undefined, returning, with-clause updates and PostgreSQL UPDATE ... FROM."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/update.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: update safely.

```ts
await db.update(users).set({ name: 'Mr. Dan' }).where(eq(users.name, 'Dan'));
// update "users" set "name" = $1 where "users"."name" = $2; -- params: ['Mr. Dan', 'Dan']
```

Rules from the docs: the object keys must match column names in your schema; values of `undefined` are ignored, so to set NULL pass `null`. SQL values are allowed: `.set({ updatedAt: sql`NOW()` })`. All values given to `.set()` are parameterized automatically.

Returning (PostgreSQL):

```ts
const updated = await db.update(users).set({ name: 'Mr. Dan' }).where(eq(users.name, 'Dan')).returning({ updatedId: users.id });
```

With clause: build a CTE (`db.$with('average_price').as(...)`) and call `db.with(averagePrice).update(products).set({ cheap: true }).where(lt(products.price, sql`(select * from ${averagePrice})`)).returning({ id: products.id })`.

Update from (PostgreSQL): the PostgreSQL docs describe it as a table expression allowing columns from other tables in the WHERE condition and update expressions.

```ts
await db.update(users).set({ cityId: cities.id }).from(cities)
  .where(and(eq(cities.name, 'Seattle'), eq(users.name, 'John')));
```

Joined tables can be aliased with `alias(cities, 'c')` (the updating table can be aliased too), and `.returning({ id: users.id, cityName: cities.name })` can return columns from the joined table in Postgres.

## Checked

Date: 2026-11-07

Confirmed against `pg/update.mdx` in the drizzle-orm-docs repo (cloned from main, read in full, all 134 lines including SQL outputs): parameterization callout, key and `undefined`/`null` rules, SQL values, returning, the `with update` example, and the Update ... from, alias and returning examples.

Removed: the "always include `.where()`" rule (not stated on the page) and the invented Verify step.

Method: documentation only; no commands were run.
