---
id: computing-software.web-development.drizzle-orm.drizzle-sql-composition-helpers
name: drizzle-sql-composition-helpers
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, sql-join, sql-fromlist, sql-append, dynamic-sql]
level: advanced
status: docs-checked
description: "Build SQL dynamically in Drizzle with sql.join, sql.fromList, append and sql.empty while keeping every value parameterized."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/sql.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: assemble variable-length SQL safely.

The `sql` template generates SQL chunks. These helpers combine chunks you collect with your own business logic into a single statement.

`sql.fromList(chunks)` combines an array of `SQL` chunks into one statement. In the docs example each chunk carries its own spaces (`` sql` where ` ``, `` sql` or ` ``).

`sql.join(chunks, separator)` does the same job with more flexibility over spaces between chunks or a custom separator (any string or character):

```ts
const chunks: SQL[] = [sql`select * from users`, sql`where`];
for (let i = 0; i < 5; i++) {
  chunks.push(sql`id = ${i}`);
  if (i < 4) chunks.push(sql`or`);
}
const finalSql: SQL = sql.join(chunks, sql.raw(' '));
// select * from users where id = $1 or id = $2 or id = $3 or id = $4 or id = $5; --> [0, 1, 2, 3, 4]
```

`sql.append(chunk)` adds a new chunk to SQL you already generated with the `sql` template, with the same effect as `fromList`: `const finalSql = sql`select * from users`; finalSql.append(sql` where `); finalSql.append(sql`id = ${1}`);`.

`sql.empty()` starts a blank SQL object to append chunks into as needed. After it you still have the full range of `sql` template features, such as parameterization, composition and escaping.

To see the generated query string and parameters, convert with a dialect: `new PgDialect().sqlToQuery(sql\`...\`)` (`PgDialect` from `drizzle-orm/pg-core`); the dialect matters because databases differ in parameterization and escaping.

## Checked

Date: 2026-11-07

Confirmed against `pg/sql.mdx` in the drizzle-orm-docs repo (cloned from main, read in full, all 452 lines including every example and its SQL output): `sql.fromList`, `sql.join` with `sql.raw(' ')`, `sql.append`, `sql.empty` and `sqlToQuery`; the shown output with placeholders `$1` to `$5` and values `[0, 1, 2, 3, 4]`.

Removed: the "safer choice" claim for `join`, the rules of thumb (no string concatenation of user data, constant separators fine, prefer `and()`/`inArray` over hand-built lists), none of which are on the page, and the invented Verify step.

Method: documentation only; no commands were run.
