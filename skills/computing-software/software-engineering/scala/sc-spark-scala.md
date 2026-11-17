---
id: computing-software.software-engineering.scala.sc-spark-scala
name: sc-spark-scala
category: computing-software
field: software-engineering
product: scala
tags: [scala, sc-spark, spark-scala]
level: advanced
status: draft
description: "Use Spark's Scala API with DataFrames and typed Datasets and avoid closure serialisation pitfalls."
sources: ["https://docs.scala-lang.org/", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spark with Scala Datasets
- Spark versions pin a Scala binary version (2.12 or 2.13); match `scalaVersion` and mark Spark `% "provided"` in assemblies.
- `spark.read.parquet(path)`, `df.groupBy("k").agg(sum("v"))`; `Dataset[T]` needs `import spark.implicits.*` for encoders.
- Closures are serialised to executors: do not capture non-serialisable objects or the enclosing class; copy fields to local vals.
- Prefer built-in column functions over UDFs; check `explain()` plans.
Verify: run on a local master with a small dataset.
