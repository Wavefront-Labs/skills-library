---
id: computing-software.data-engineering.apache-spark.defining-explicit-schemas
name: defining-explicit-schemas
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, pyspark, structtype-schema, ddl-schema, schema-of-json, from-json, schema-inference, data-types, nullable]
level: practitioner
status: docs-checked
description: "Define Spark schemas explicitly with StructType or DDL strings, derive them with schema_of_json, and avoid inference cost and type drift in production reads."
sources:
  - https://spark.apache.org/docs/latest/sql-ref-datatypes.html
  - https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.functions.schema_of_json.html
  - https://spark.apache.org/docs/latest/sql-data-sources-json.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Defining explicit schemas

**Goal:** production reads never depend on inference; types are stable, and parsing errors show up instead of silently becoming strings.

## Why not infer
- `inferSchema=true` (CSV) or JSON inference reads the data to work out types.
- Inference depends on the sample: a column that is all-int today becomes string tomorrow, breaking downstream writes.
- For streaming file sources, provide the schema explicitly rather than relying on inference.

## StructType
```python
from pyspark.sql.types import StructType, StructField, StringType, LongType, TimestampType, DecimalType, ArrayType
schema = StructType([
    StructField("order_id", LongType(), nullable=False),
    StructField("customer_id", StringType()),
    StructField("amount", DecimalType(18, 2)),
    StructField("created_at", TimestampType()),
    StructField("items", ArrayType(StructType([
        StructField("sku", StringType()), StructField("qty", LongType())]))),
])
df = spark.read.schema(schema).json("s3://raw/orders/")
```

## DDL strings (shorter, reviewable)
```python
ddl = "order_id BIGINT, customer_id STRING, amount DECIMAL(18,2), created_at TIMESTAMP, items ARRAY<STRUCT<sku: STRING, qty: BIGINT>>"
df = spark.read.schema(ddl).json(path)
```

## JSON columns inside a table
```python
sample = df.select("payload").first()[0]
spark.range(1).select(F.schema_of_json(F.lit(sample))).first()[0]   # returns DDL to paste
parsed = df.withColumn("p", F.from_json("payload", ddl, {"mode": "PERMISSIVE"}))
```
Pin the schema in code once derived; do not call `schema_of_json` on every run.

## Nullability
Do not rely on `nullable=False` as a check; validate key columns for nulls yourself.

## Gotchas
- Timestamp parsing uses the `timestampFormat` option. In PERMISSIVE mode a malformed record goes to the field named by `columnNameOfCorruptRecord` (default `_corrupt_record`) and malformed fields become null; add that string field to your schema to keep the raw record.
- `spark.sql.ansi.enabled` defaults to true in the current configuration docs; check the ANSI docs for how invalid casts and overflow behave on your version.

## Verify
- [ ] `df.printSchema()` matches the contract, no unexpected `string` columns.
- [ ] A row with a bad timestamp lands in `_corrupt_record` (or fails in FAILFAST), not silently null.

## Checked

2026-10-28. Confirmed against: Spark JSON data source page (PERMISSIVE and FAILFAST modes, columnNameOfCorruptRecord, timestampFormat), configuration page (spark.sql.ansi.enabled default true, spark.sql.columnNameOfCorruptRecord), PySpark schema_of_json page (DDL output). Removed (not confirmable in the fetched pages): streaming schemaInference setting, fromDDL/simpleString/json round-trip lines, nullability-not-enforced claim, CSV field-order claim, decimal overflow and Parquet user-schema claims.

Method: documentation only; no commands were run.
