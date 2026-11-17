---
id: computing-software.data-engineering.polars.sql-iceberg-catalog
name: sql-iceberg-catalog
category: computing-software
field: data-engineering
product: polars
tags: [polars, sql, iceberg, register-catalog, create-table, insert-overwrite, polars-sql-context, namespaces, catalog]
level: practitioner
status: docs-checked
description: "Attach an Iceberg catalog to Polars SQLContext with register_catalog, resolve table names, and run CREATE, ALTER, INSERT, DELETE, TRUNCATE and DROP on catalog tables."
sources:
  - https://docs.pola.rs/user-guide/sql/intro/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: query and manage Iceberg catalog tables through Polars SQL instead of registering each table.

```python
from pyiceberg.catalog import load_catalog
ctx = pl.SQLContext()
ctx.register_catalog("lake", load_catalog("lake"), default_namespace="tpch", default=True)
ctx.execute("SELECT * FROM lineitem")            # lake: tpch.lineitem
ctx.execute("SELECT * FROM tpch.lineitem")       # default catalog
ctx.execute("SELECT * FROM lake.tpch.lineitem")  # catalog lake
```
Name resolution order: (1) a CTE or table registered in the context; (2) a table of the attached catalog the name starts with; (3) the default catalog (`default=True`), where a name with no namespace gets `default_namespace`.

Behaviour and gotchas
- Catalog tables scan lazily like `scan_iceberg`, loading when the schema is first needed. Identifiers pass to the catalog as written (case-sensitive); a quoted `"a.b"` is one part.
- With a default catalog, any name that is not a CTE or registered table is looked up in the catalog, including misspellings: `NoSuchTableError` can surface as late as `collect()`. Use full names such as `lake.tpch.lineitem` to be explicit.
- Catalogs attached inside `with SQLContext()` are detached on exit.
- A serialized plan over catalog tables can contain catalog properties and storage options, possibly credentials: treat it as secret.

Statements run at `execute()`
```python
ctx.execute("CREATE TABLE orders (id BIGINT NOT NULL, amount DOUBLE)")
ctx.execute("CREATE TABLE big_orders AS SELECT * FROM orders WHERE amount > 1000")
ctx.execute("CREATE TEMP TABLE staging AS SELECT * FROM orders")   # registered, not catalog
ctx.execute("DROP TABLE big_orders")
ctx.execute("CREATE SCHEMA IF NOT EXISTS lake.sales WITH ('location' = 's3://bucket/sales')")
ctx.execute("ALTER TABLE lake.sales.orders ADD COLUMN discount DOUBLE")
ctx.execute("INSERT INTO lake.sales.orders (id, quantity) VALUES (1, 10), (2, 20)")
ctx.execute("INSERT OVERWRITE lake.sales.orders SELECT * FROM staged_orders")
ctx.execute("DELETE FROM lake.sales.orders WHERE quantity = 0")
ctx.execute("TRUNCATE TABLE lake.sales.orders")
```
- `CREATE TABLE ... AS` commits rows with the create; a failed query creates no table.
- `NOT NULL` makes a required field; `LOCATION` and `WITH ('format-version' = 2, ...)` set location and properties; `PARTITION BY (region, day(ordered_at), bucket(16, id))` supports `year`, `month`, `day`, `hour`, `bucket(N, col)`, `truncate(W, col)`.
- `DROP TABLE` drops a registered table first, else the catalog table permanently; `PURGE` also deletes data files. `DROP SCHEMA` only for an empty namespace.
- `ALTER TABLE`: one change per statement. `INSERT OVERWRITE` replaces all rows in every partition; its `WHERE` selects the new rows. `DELETE` conditions compare columns with constants (but the same page also has a bullet saying DELETE is not supported on catalog tables, so test it before relying on it). See `SQLContext.register_catalog`.

## Checked

2026-11-07. Read in full and compared against this skill: https://docs.pola.rs/user-guide/sql/intro/. Corrected: Noted that the page also lists DELETE as unsupported on catalog tables, so it should be tested before relying on it. Any parameter, default, class, method or error string not found on those pages was removed.

Method: documentation only; no commands were run.
