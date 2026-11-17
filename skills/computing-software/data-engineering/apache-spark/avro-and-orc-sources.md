---
id: computing-software.data-engineering.apache-spark.avro-and-orc-sources
name: avro-and-orc-sources
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, spark-data-sources, spark-avro, orc, avro, from-avro, to-avro, avroschema, orc-bloom-filter, file-formats, kafka-avro]
level: practitioner
status: docs-checked
description: "Use Avro and ORC with Spark: spark-avro package, reader schemas and evolution, from_avro/to_avro for Kafka payloads (Confluent wire format caveat), ORC options and bloom filters."
sources:
  - https://spark.apache.org/docs/latest/sql-data-sources-avro.html
  - https://spark.apache.org/docs/latest/sql-data-sources-orc.html
  - https://github.com/apache/spark/blob/master/sql/catalyst/src/main/scala/org/apache/spark/sql/internal/SQLConf.scala
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Avro and ORC in Spark

**Goal:** read and write Avro (row-oriented) and ORC (columnar) correctly.

## Avro
The `spark-avro` module is external and not included in `spark-submit` or `spark-shell` by default: add `--packages org.apache.spark:spark-avro_<SCALA_BINARY>:<SPARK_VERSION>`.
```python
df = spark.read.format("avro").load("s3://landing/orders_avro/")
df.write.format("avro").option("compression", "snappy").save("s3://out/")   # snappy is the default; also uncompressed, deflate, bzip2, xz, zstandard
```
- `avroSchema` (JSON) can be set to an evolved schema that is compatible with but different from the schema in the files; deserialization then follows the evolved schema: `.option("avroSchema", open("order_v3.avsc").read())`.
- Unions: `union(int, long)` maps to LongType, `union(float, double)` to DoubleType, `union(something, null)` to that type with nullable true; all other unions map to a struct with fields `member0`, `member1`, ... (`enableStableIdentifiersForUnionType`, default false, gives type-based names instead).
- `positionalFieldMatching` (default false, since 3.2.0) matches the provided Avro schema to the SQL schema by field position instead of name.

## Avro inside Kafka messages
```python
from pyspark.sql.avro.functions import from_avro, to_avro
schema_str = open("order.avsc").read()
parsed = kafka_df.select(from_avro(F.col("value"), schema_str, {"mode": "PERMISSIVE"}).alias("o"))
```
`from_avro` and `to_avro` convert a column to and from Avro binary, which suits Kafka payloads. They decode with the schema you pass, so messages carrying extra framing from a schema-registry serializer need that framing handled outside these functions (see your registry's wire-format documentation).

## ORC
```python
df.write.format("orc").option("compression", "zstd") \
  .option("orc.bloom.filter.columns", "customer_id").save("s3://out/orc/")
```
- The `native` implementation (`spark.sql.orc.impl`, default native) supports a vectorized reader and has been the default since Spark 2.3; `hive` follows Hive's behaviour and uses Hive SerDe.
- `spark.sql.orc.filterPushdown` defaults to true.
- ORC table options such as `orc.bloom.filter.columns`, `orc.dictionary.key.threshold` and `orc.column.encoding.direct` are passed in `OPTIONS` when creating a table or as write options.
- The compression codec comes from the `compression` option, then `orc.compress`, then `spark.sql.orc.compression.codec`.

## Choosing
| Format | Pick when |
|---|---|
| Avro | Kafka payloads and landing raw records with evolving schemas |
| Parquet | Columnar analytics (Spark's default data source format) |
| ORC | Estates already on ORC (Hive heritage) |

## Verify
- [ ] Reading old and new Avro files together with the latest reader schema succeeds with defaults filled.
- [ ] Kafka Avro decode produces no nulls on a sample of known-good messages.
- [ ] `explain` on an ORC filter shows the pushed filters.

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/, SQLConf.scala and python/pyspark/sql/readwriter.py on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed in sql-data-sources-avro.md: spark-avro external module and --packages coordinates, avroSchema evolved-schema semantics, positionalFieldMatching (3.2.0, false), union mapping rules (int/long, float/double, nullable, memberN structs), enableStableIdentifiersForUnionType, compression codecs and default snappy (SQLConf). Confirmed in sql-data-sources-orc.md and SQLConf.scala: native vs hive implementation, vectorized reader default since 2.3, filterPushdown true, orc.bloom.filter.columns / dictionary / encoding table options, compression precedence. Wrong claim fixed: not every non-nullable union becomes a struct (int/long and float/double have simple mappings). Removed Databricks and ABRiS claims, the 5-byte header substring recipe, fpp option, ACID ORC and stripe-statistics claims.

Method: documentation only; no commands were run.
