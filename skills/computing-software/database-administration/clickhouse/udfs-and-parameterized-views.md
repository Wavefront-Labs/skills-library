---
id: computing-software.database-administration.clickhouse.udfs-and-parameterized-views
name: udfs-and-parameterized-views
category: computing-software
field: database-administration
product: clickhouse
tags: [database-administration, clickhouse, udf, create-function, parameterized-view, query-parameters, stored-procedures]
level: practitioner
status: docs-checked
description: "Replace stored procedures in ClickHouse with lambda UDFs, parameterized views and typed query parameters."
sources:
  - https://github.com/ClickHouse/clickhouse-docs/blob/main/docs/guides/developer/stored-procedures-and-prepared-statements.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# udfs and parameterized views
ClickHouse has no stored procedures with IF/loop control flow, by design: running O(n) small queries is slower than fewer complex ones. Alternatives:

Lambda UDFs (SQL expressions only):
```sql
CREATE FUNCTION calculate_tax AS (price, rate) -> price * rate;
SELECT product_name, calculate_tax(price, 0.2) FROM products;
```
Parameterized views take typed placeholders and are called like a function:
```sql
CREATE VIEW sales_by_date AS
SELECT date, product_id, sum(quantity) AS total_quantity
FROM sales
WHERE date BETWEEN {start_date:Date} AND {end_date:Date}
GROUP BY date, product_id;

SELECT * FROM sales_by_date(start_date='2024-01-01', end_date='2024-01-31');
```
Query parameters use `{name:Type}` syntax in ad-hoc statements and are bound by the client, which is the safe alternative to string concatenation and prevents SQL injection.

Lambda UDFs cannot contain loops or complex control flow.

## Checked
2026-11-03. Confirmed against the ClickHouse docs guide "Stored procedures and prepared statements": no control-flow stored procedures, the O(n) small-queries rationale, `CREATE FUNCTION ... AS (args) -> expr` lambda UDFs, parameterized views and query parameters preventing SQL injection. Removed: the type-coercion gotcha and Verify step, which the page does not state.
Method: documentation only; no commands were run.
