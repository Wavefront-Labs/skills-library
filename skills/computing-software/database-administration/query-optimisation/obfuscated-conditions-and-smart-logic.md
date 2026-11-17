---
id: computing-software.database-administration.query-optimisation.obfuscated-conditions-and-smart-logic
name: obfuscated-conditions-and-smart-logic
category: computing-software
field: database-administration
product: query-optimisation
tags: [database-administration, query-optimisation, composite-index, obfuscated-conditions, smart-logic, optional-filters, dynamic-sql, sargability]
level: practitioner
status: draft
description: "Remove index-defeating patterns: date truncation, numbers stored as strings, concatenated columns, and 'smart logic' optional filters like (:p IS NULL OR col = :p)."
sources:
  - https://use-the-index-luke.com/sql/where-clause/obfuscation
  - https://use-the-index-luke.com/sql/where-clause/bind-parameters
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Obfuscated conditions and smart logic

## Dates
```sql
-- defeats an index on created_at
WHERE DATE(created_at) = '2026-10-18'
WHERE to_char(created_at, 'YYYY-MM') = '2026-10'
-- index-friendly half-open ranges
WHERE created_at >= '2026-10-18' AND created_at < '2026-10-19'
WHERE created_at >= '2026-10-01' AND created_at < '2026-11-01'
```
Half-open ranges (`>=` and `<`) also avoid the `BETWEEN ... 23:59:59.999` precision bug.

## Numeric strings
A `varchar` column holding numbers compared to a number: the database converts the **column**
(each row) to number, so no index use, and errors on non-numeric rows in some engines. Compare
like with like (`WHERE account_no = '00123'`) or fix the column type.

## Combined columns
```sql
WHERE first_name || ' ' || last_name = 'Ada Lovelace'      -- no index
WHERE first_name = 'Ada' AND last_name = 'Lovelace'        -- composite index
```
If the expression is genuinely needed, index the expression (function-based / generated column).

## Math on the column
`WHERE amount + 10 > 100` -> `WHERE amount > 90`. Keep the indexed column alone on one side.

## Smart logic (optional filters)
```sql
SELECT * FROM orders
WHERE (:customer_id IS NULL OR customer_id = :customer_id)
  AND (:status IS NULL OR status = :status);
```
One cached plan must work for every combination of supplied/omitted parameters, so the
optimizer usually picks a full scan. Fixes:
- **Build the SQL dynamically** with only the supplied predicates (still with bind parameters):
  each combination gets its own good plan.
  ```python
  sql, params = "SELECT * FROM orders WHERE 1=1", []
  if customer_id is not None: sql += " AND customer_id = %s"; params.append(customer_id)
  if status is not None:      sql += " AND status = %s";      params.append(status)
  ```
- SQL Server: `OPTION (RECOMPILE)` lets the optimizer simplify away the `IS NULL` branches for
  the actual values (costs a compile per execution).
- PostgreSQL: custom plans (first five executions, or `plan_cache_mode = force_custom_plan`)
  also fold the constants.
- Oracle: dynamic SQL, or separate statements per common combination.

## Verify
EXPLAIN shows an index access (`Index Cond` / `access()` / Seek Predicate) on the rewritten
predicate for each common filter combination, with logical reads proportional to rows returned.
