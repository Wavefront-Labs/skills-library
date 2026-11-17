---
id: computing-software.web-development.drizzle-orm.drizzle-query-aliases-and-dynamic-builders
name: drizzle-query-aliases-and-dynamic-builders
category: computing-software
field: web-development
product: drizzle-orm
tags: [drizzle, alias, as, self-join, subquery-alias]
level: practitioner
status: docs-checked
description: "Alias tables, columns, subqueries and CTEs in Drizzle with alias(), .as() on columns and sql expressions, and $with names."
sources:
  - https://github.com/drizzle-team/drizzle-orm-docs/blob/main/src/content/docs/pg/aliases.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: use SQL AS correctly in four places (aliasing maps directly to the SQL `AS` keyword).

- Tables: `import { alias } from 'drizzle-orm/pg-core'; const manager = alias(employees, 'manager'); db.select({ employeeName: employees.name, managerName: manager.name }).from(employees).leftJoin(manager, eq(employees.managerId, manager.id));`. Useful when you join the same table multiple times, for example employees and their managers.
- Columns: `users.name.as('lower_name')` and `sql<string>`lower(${users.name})`.as('lower_name')`.
- Subqueries: when a subquery is a data source you must provide an alias with `.as()`: `const sq = db.select().from(users).where(eq(users.id, 42)).as('sq'); db.select().from(sq);` and in joins `leftJoin(sq, eq(users.id, sq.id))`.
- CTEs: `db.$with('sq').as(...)` and `db.with(sq).select().from(sq)`; `sql` expressions inside a CTE must be aliased with `.as()` to be referenced in the outer query (for example `sql<string>`upper(${users.name})`.as('name')` then `sq.name`).

## Checked

Date: 2026-11-07

Confirmed against `pg/aliases.mdx` in the drizzle-orm-docs repo (cloned from main, read in full, all 127 lines including every code and SQL block): table, column, subquery and CTE aliasing, the "must provide an alias" rule and the CTE `sql` aliasing rule.

Removed: the claim that aliasing is the only way to disambiguate a repeated table, the claim about same-named tables in different schemas (neither on the page), and the invented Verify step. Thin: the skill name mentions dynamic builders but the cited page covers only aliases.

Method: documentation only; no commands were run.
