---
id: computing-software.web-development.drizzle-orm.drizzle-sql-template-operator
name: drizzle-sql-template-operator
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, sql-template, mapwith, raw-sql, sql-injection]
level: practitioner
status: docs-checked
description: "Use Drizzle's sql tagged template for raw fragments safely: parameter binding, sql<T> typing, mapWith, as alias, sql.raw, execute and toSQL output."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/sql.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: drop to SQL without losing safety.

```ts
import { sql } from 'drizzle-orm';
const id = 69;
await db.execute(sql`select * from ${usersTable} where ${usersTable.id} = ${id}`);
// select * from "users" where "users"."id" = $1; --> [69]
```

Tables and columns passed in are mapped to SQL with escaped names and the escaped table name appended to column names; dynamic parameters such as `${id}` become `$1` and the values go into an array passed separately to the database. The docs say this prevents SQL injection.

- `sql<T>`: purely a typing helper for Drizzle; it does no runtime mapping. Without it fields are typed `unknown`.
- `.mapWith(Number)`, `.mapWith(usersTable.name)` (maps at runtime like that column) or `.mapWith({ mapFromDriverValue: (value) => ... })`: runtime mapping of values from the driver.
- `.as('alias_name')`: explicit alias for a selected custom field, for example `sql`lower(${usersTable.name})`.as('lower_name')`.
- `sql.raw(string)`: included as-is, without parameterization or escaping: `sql.raw(`select * from users where id = ${12}`)` yields `id = 12`, whereas the template yields `id = $1` with `[12]`. It can also sit inside a template: `` sql`... where id = ${sql.raw(12)}` `` yields `id = 12`.

Usable in partial selects, where, orderBy, having, groupBy and relational query builders. Example select: `count: sql<number>`count(*)`.mapWith(Number)`.

Convert to string and params for a dialect:

```ts
import { PgDialect } from 'drizzle-orm/pg-core';
new PgDialect().sqlToQuery(sql`select * from ${usersTable} where ${usersTable.id} = ${12}`);
// select * from "users" where "users"."id" = $1; --> [ 12 ]
```

## Checked

Date: 2026-11-07

Confirmed against `pg/sql.mdx` in the drizzle-orm-docs repo (cloned from main, read in full, all 452 lines including every example and its SQL output): the template and parameter binding, the injection statement, `sql<T>` callout, `mapWith` variants, `.as()`, both `sql.raw()` examples, supported clauses, `sqlToQuery`, and the select, where, orderBy and having/groupBy examples.

Removed: the advice never to pass user input to `sql.raw` and the claim that aliases are needed in CTEs and subqueries (neither on this page), the claim about PostgreSQL `count(*)` arriving as a string, and the invented Verify step.

Method: documentation only; no commands were run.
