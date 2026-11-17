---
id: computing-software.web-development.node-express.parameterized-queries-and-raw-sql
name: parameterized-queries-and-raw-sql
category: computing-software
field: web-development
product: node-express
tags: [injection, parameterized-queries, raw-sql, sql-injection, orm, security, orm-raw-sql]
level: practitioner
status: docs-checked
description: "Preventing SQL injection with parameterised queries in node-postgres, mysql2, Prisma, Knex and Sequelize, the raw-SQL escape hatches that bypass them, and dynamic identifiers."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
  - https://node-postgres.com/features/queries
  - https://www.prisma.io/docs/orm/prisma-client/using-raw-sql/raw-queries
  - https://knexjs.org/guide/raw.html
  - https://sequelize.org/docs/v6/core-concepts/raw-queries/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Parameterised queries and ORM raw-SQL pitfalls

## 1. Parameterise every value
```js
// node-postgres
await pool.query("SELECT * FROM users WHERE email = $1 AND org_id = $2", [email, orgId]);
// mysql2
await conn.execute("SELECT * FROM users WHERE email = ?", [email]);
// Knex
await knex("users").where({ email }).first();
await knex.raw("SELECT * FROM users WHERE email = ?", [email]);
```
The driver sends SQL and values separately (or escapes correctly) - values can never change the query structure.

## 2. ORM escape hatches
| ORM | Safe | Injectable |
|---|---|---|
| Prisma | `` $queryRaw`... ${email}` `` (tagged template, parameterised) | `$queryRawUnsafe(\`... ${email}\`)` |
| Sequelize | `sequelize.query(sql, { replacements: { email } })` | string-built `sequelize.query` |
| Knex | `knex.raw(sql, bindings)`, `whereRaw("x = ?", [v])` | `knex.raw(\`... ${v}\`)` |
| Django | `Model.objects.raw(sql, [p])`, `cursor.execute(sql, [p])` | f-strings in `raw()`/`RawSQL` |
| Rails | `where("email = ?", e)`, `where(email: e)` | `where("email = '#{e}'")` |

## 3. Identifiers and keywords cannot be parameters
Column names, sort direction, table names, `LIMIT` in some drivers: map from an allowlist.
```js
const SORTS = { newest: "created_at DESC", price: "price ASC" };
const orderBy = SORTS[req.query.sort] ?? SORTS.newest;
```
For dynamic identifiers use the library's identifier binding (Knex `??`) only with allowlisted names.

## 4. Also watch
- `LIKE` patterns: parameterise the value and escape `%`/`_` if users should not wildcard.
- `IN` lists: generate one placeholder per value (Knex has no array binding).
- Stored procedures that concatenate inside SQL are still injectable.
- Second-order injection: data stored safely, later concatenated into another query.
- Least privilege DB user (no DDL, no superuser) limits blast radius.

## Verify
Grep for template literals/concatenation passed to `query(`, `raw(`, `Unsafe(`, `literal(`.

## Checked

2026-10-25 against the node-postgres, Prisma 7, Sequelize 6, Knex, Django and Rails docs and OWASP Cheat Sheet Series (OWASP/CheatSheetSeries, commit of 2026-10-24). Confirmed: node-postgres sends the query text unaltered with the parameters to the server; Prisma $queryRaw tagged template versus $queryRawUnsafe; Sequelize replacements; Knex raw bindings with ? for values and ?? for identifiers; Django Manager.raw and cursor.execute take params; Rails where("... ?", value); Knex has no array binding, so generate one ? per value.

Method: documentation only; no commands were run.
