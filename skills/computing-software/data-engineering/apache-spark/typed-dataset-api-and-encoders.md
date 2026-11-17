---
id: computing-software.data-engineering.apache-spark.typed-dataset-api-and-encoders
name: typed-dataset-api-and-encoders
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, scala, spark-dataset-api, dataset, encoders, case-class, typed-transformations, spark-sql]
level: advanced
status: docs-checked
description: "Use Spark's typed Dataset API in Scala: case-class encoders, as[T], typed map/groupByKey, and when lambdas defeat Catalyst optimisation versus DataFrame columns."
sources:
  - https://spark.apache.org/docs/latest/sql-getting-started.html#creating-datasets
  - https://spark.apache.org/docs/latest/api/scala/org/apache/spark/sql/Dataset.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Typed Dataset API and encoders (Scala)

`DataFrame` is `Dataset[Row]`. A typed `Dataset[T]` gives compile-time field checking in Scala/Java; Python has no typed Dataset.

```scala
case class Order(id: Long, customerId: Long, amount: BigDecimal, ts: java.sql.Timestamp)
import spark.implicits._                       // brings Encoders for case classes and primitives
val orders: Dataset[Order] = spark.read.parquet("s3a://lake/orders").as[Order]
val big = orders.filter(_.amount > 100)          // typed lambda
val perCustomer = orders.groupByKey(_.customerId)
  .mapGroups { (cid, it) => (cid, it.map(_.amount).sum) }
```

## Encoders
- Case-class fields map to columns **by name**; `as[T]` fails at analysis if a field is missing, and extra columns are kept in the plan until you `select`/`map`.
- Supported: primitives, `String`, `java.sql.Timestamp/Date`, `java.time.Instant/LocalDate`, `BigDecimal`, `Option`, `Seq`, `Map`, nested case classes. For other classes use `Encoders.kryo[T]` (opaque binary column, no pushdown) or `Encoders.bean`.
- Define case classes at top level, not inside a method, or you get encoder / serialization errors.
- `Option[T]` for nullable columns; a null into a primitive `Long` field throws at runtime.

## Typed vs untyped performance
- Lambdas (`filter(_.amount > 100)`, `map`) are opaque to Catalyst: no predicate pushdown into Parquet, and every row is deserialised into a JVM object and back. `explain()` shows `DeserializeToObject` / `SerializeFromObject`.
- Column expressions (`orders.filter($"amount" > 100)`) still return `Dataset[Order]` and keep pushdown. Use typed lambdas only for logic you cannot express with columns.
- `groupByKey` + `mapGroups` cannot partially aggregate; it shuffles every row. Prefer `groupBy(...).agg(...)` or a typed `Aggregator` (`udaf(...)`) which supports partial aggregation.
- `joinWith` returns `Dataset[(A, B)]`, keeping both sides typed.

## Verify
- [ ] `explain()` on hot paths shows pushed filters and no object (de)serialisation loops.
- [ ] Unit test `as[T]` on a sample with nulls to catch primitive-null crashes.

## Checked

2026-10-28. Confirmed: Dataset API names (as, groupByKey, joinWith) on the Dataset API page. Removed: an unconfirmed version gate and a quoted error message.

Method: documentation only; no commands were run.
