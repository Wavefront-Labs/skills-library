---
id: computing-software.web-development.drizzle-orm.drizzle-aggregations-and-count
name: drizzle-aggregations-and-count
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, aggregation, group-by, having, count]
level: practitioner
status: docs-checked
description: "Aggregate in Drizzle with groupBy/having and the count, sum, avg, min, max helpers, and handle PostgreSQL returning bigint as string."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/select.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: aggregate correctly and get numbers, not strings.

Group and filter groups with `.groupBy()` and `.having()`:

```ts
await db.select({ age: users.age, count: sql<number>`cast(count(${users.id}) as int)` })
  .from(users).groupBy(users.age).having(({ count }) => gt(count, 1));
```

In PostgreSQL `count()` returns `bigint`, delivered as a string, hence `cast(... as int)` or `.mapWith(Number)`.

Helpers from `drizzle-orm`: `count()`, `count(col)`, `countDistinct`, `avg`, `avgDistinct`, `sum`, `sumDistinct`, `max`, `min`. Per the docs they are equivalent to `sql` templates: `count` maps with `Number`; `avg` and `sum` map with `String` (so they return strings); `max`/`min` map with the column.

When mixing aggregate and plain columns in one select, you must `groupBy` the plain ones.

Join plus aggregate pattern:

```ts
db.select({ id: orders.id, productsCount: sql<number>`cast(count(${details.productId}) as int)`,
  totalPrice: sql<number>`sum(${details.quantity} * ${details.unitPrice})` })
 .from(orders).leftJoin(details, eq(orders.id, details.orderId)).groupBy(orders.id).orderBy(asc(orders.id));
```

The docs recommend the `$count` API when you only need a row count.

## Checked

2026-11-04: every command, option, default and code identifier above was compared with the cited documentation pages (select.mdx) read in full.

Removed because the pages do not confirm them: unsourced advice, "Verify" steps and behavioural claims.

Method: documentation only; no commands were run.
