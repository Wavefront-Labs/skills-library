---
id: computing-software.web-development.drizzle-orm.drizzle-set-operations
name: drizzle-set-operations
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, union, intersect, except, set-operations]
level: practitioner
status: docs-checked
description: "Combine query results with Drizzle union, unionAll, intersect, intersectAll, except and exceptAll in functional or chained style."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/set-operations.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: merge result sets of compatible selects.

Supported: `UNION`, `UNION ALL`, `INTERSECT`, `INTERSECT ALL`, `EXCEPT`, `EXCEPT ALL`. Each has an import-pattern function from the dialect core and a builder-pattern method of the same name.

Functional form imported from the dialect core:

```ts
import { union } from 'drizzle-orm/pg-core';
const result = await union(
  db.select({ name: users.name }).from(users),
  db.select({ name: customers.name }).from(customers)
).limit(10);
```

Chained form:

```ts
await db.select({ name: users.name }).from(users)
  .union(db.select({ name: customers.name }).from(customers))
  .limit(10);
```

Generated SQL wraps each block in parentheses, and the limit is a parameter: `(select "name" from "sellers") union (select "name" from "customers") limit $1 -- params: [10]`.

Semantics per the page:
- `union`: all results from two blocks, omitting duplicates.
- `unionAll`: all results, with duplicates (for example online and in-store transactions where duplicates are meaningful).
- `intersect` / `intersectAll`: only rows both blocks have in common, without / with duplicates.
- `except` / `exceptAll`: rows from the first block that are not in the second, without / with duplicates.

```ts
import { unionAll, intersect, exceptAll } from 'drizzle-orm/pg-core';
await unionAll(
  db.select({ transaction: onlineSales.transactionId }).from(onlineSales),
  db.select({ transaction: inStoreSales.transactionId }).from(inStoreSales));
await intersect(departmentACourses, departmentBCourses);
await db.select({ productId: regularCustomerOrders.productId }).from(regularCustomerOrders)
  .exceptAll(db.select({ productId: vipCustomerOrders.productId }).from(vipCustomerOrders));
```

## Checked

Date: 2026-11-07

Confirmed against `pg/set-operations.mdx` in the drizzle-orm-docs repo (cloned from main, read in full, all 412 lines including every import-pattern, builder-pattern and schema tab): the six operations, imports from `drizzle-orm/pg-core`, chained methods, `.limit(10)` on union, parenthesized blocks and `limit $1` in the shown SQL, and the definitions of each operation.

Removed: the claims that column counts and types must match and that `orderBy` applies to the combined result (neither is stated on the page), the "read only for union" caveat (all variants were read), and the invented Verify step.

Method: documentation only; no commands were run.
