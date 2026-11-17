---
id: computing-software.data-engineering.apache-spark.nested-data-and-higher-order-functions
name: nested-data-and-higher-order-functions
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, pyspark, dataframe-api, nested-data-spark, explode, posexplode, higher-order-functions, transform, filter, aggregate, struct, array, map, from-json, schema-of-json, variant]
level: practitioner
status: docs-checked
description: "Work with arrays, structs and maps in Spark: explode vs explode_outer, flattening structs, transform/filter/aggregate higher-order functions, from_json with schemas."
sources:
  - https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/functions.html
  - https://spark.apache.org/docs/latest/sql-ref-functions-builtin.html
  - https://spark.apache.org/docs/latest/sql-ref-datatypes.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nested data: arrays, structs, maps and higher-order functions

**Goal:** flatten or reshape semi-structured data (JSON events, API payloads) without UDFs and without silently losing rows.

## Parse JSON strings with an explicit schema
```python
from pyspark.sql import functions as F, types as T
schema = T.StructType([
    T.StructField("order_id", T.StringType()),
    T.StructField("items", T.ArrayType(T.StructType([
        T.StructField("sku", T.StringType()),
        T.StructField("qty", T.IntegerType()),
        T.StructField("price", T.DecimalType(12, 2))]))),
    T.StructField("attrs", T.MapType(T.StringType(), T.StringType()))])
df = raw.withColumn("j", F.from_json("payload", schema))
```
Get a starting schema with `F.schema_of_json(F.lit(sample))` once, then pin it. An unparsable string yields a null result from `from_json`; count those rows.
Current Spark also has `VARIANT` functions (`parse_json`, `variant_get`) for schema-flexible storage.

## Structs
```python
df.select("j.order_id", "j.items")          # dot access
df.select("j.*")                            # expand all struct fields
df.withColumn("j", F.col("j").withField("source", F.lit("web")))   # 3.1+ modify nested field
df.withColumn("j", F.col("j").dropFields("attrs"))
```

## Arrays: explode carefully
```python
lines = df.select("j.order_id", F.explode_outer("j.items").alias("item")) \
          .select("order_id", "item.sku", "item.qty", "item.price")
```
- `explode` drops rows whose array is null or empty; `explode_outer` keeps them with null. Using `explode` on orders with no items silently loses orders.
- `posexplode` adds the position (line number); default output column names are `pos`, `col`, and `key`/`value` for maps.
- Only one explode is allowed per SELECT clause; to zip two arrays use `F.arrays_zip("a", "b")` (the shorter array is padded with nulls) then explode once.
- Exploding multiplies row counts: check sizes before joining exploded tables.

## Higher-order functions (no UDF, no explode)
```python
df = df.withColumn("items_total",
        F.aggregate("j.items", F.lit(0).cast("decimal(14,2)"),
                    lambda acc, x: acc + x.qty * x.price))
df = df.withColumn("big_items", F.filter("j.items", lambda x: x.qty > 10))
df = df.withColumn("skus", F.transform("j.items", lambda x: F.upper(x.sku)))
df = df.withColumn("has_promo", F.exists("j.items", lambda x: x.sku.startswith("PROMO")))
```
SQL equivalents: `transform(items, x -> x.sku)`, `aggregate(items, 0, (acc, x) -> acc + x.qty)`.

## Maps
`F.map_keys`, `F.map_values`, `F.col("attrs")["utm_source"]`, `F.explode(map)` yields `key`, `value`. `F.map_from_entries`, `F.map_filter`.

## Gotchas
- The `aggregate` merge function must return the same type as the initial value (cast the zero accordingly). Python UDFs are not supported inside the merge or finish functions.
- Pin schemas in production rather than inferring them from samples.

## Verify
- [ ] Row counts before and after exploding reconcile: `sum(size(items))` (treating null as 0) plus empties equals exploded rows with `explode_outer`.
- [ ] Rows with null parsed JSON are counted and routed to a quarantine path.

## Checked
Method: docs-checked 2026-11-09 against the Spark SQL built-in functions page, the PySpark functions index, and the PySpark reference pages for explode, explode_outer, from_json, aggregate, arrays_zip, Column.withField and Column.dropFields. The `withField` and `dropFields` methods are documented as added in 3.1.0. Dropped unconfirmed claims about the Spark 4.0 VARIANT release, schema-inference cost and predicate pushdown.
