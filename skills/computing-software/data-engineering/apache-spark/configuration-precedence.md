---
id: computing-software.data-engineering.apache-spark.configuration-precedence
name: configuration-precedence
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, spark-defaults-conf, spark-config-precedence, sparkconf, spark-conf, runtime-sql-conf, configuration]
level: practitioner
status: docs-checked
description: "Work out which Spark setting actually wins: spark-defaults.conf vs --conf vs SparkConf vs spark.conf.set, static vs runtime SQL confs, and how to verify the effective value."
sources:
  - https://spark.apache.org/docs/latest/configuration.html#dynamically-loading-spark-properties
  - https://github.com/apache/spark/blob/master/sql/core/src/main/scala/org/apache/spark/sql/classic/SparkSession.scala
  - https://spark.apache.org/docs/latest/web-ui.html#environment-tab
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spark configuration precedence

**Goal:** know where a property came from, why a change "did nothing", and set each kind of property in the only place it can take effect.

## Order (highest wins)
1. Properties set directly on `SparkConf` (for example via `SparkSession.builder.config(...)`) before the context starts.
2. Flags passed to `spark-submit` / `spark-shell`: `--conf k=v` and `--properties-file`, plus dedicated flags such as `--executor-memory` and `--driver-memory`.
3. `conf/spark-defaults.conf`. When `--properties-file` is given, Spark no longer loads `spark-defaults.conf` unless `--load-spark-defaults` is also passed.
4. Built-in defaults.

`spark.conf.set(...)` at runtime only affects **runtime-modifiable SQL confs** (`spark.sql.*` mostly). Setting a static/core property there either is rejected for static SQL configs (for example `spark.sql.extensions`) and does not change core properties such as `spark.executor.memory` once the context has started. Use `spark.conf.isModifiable(key)` to test.

## Classify the property before setting it
| Kind | Examples | Where to set |
|---|---|---|
| Deploy / launch | `spark.driver.memory` (client mode), `spark.driver.extraJavaOptions`, `spark.jars.packages` | `spark-submit` or defaults file. In client mode the driver JVM already exists, so code-level values are too late. |
| Core runtime (fixed at context start) | `spark.executor.memory`, `spark.executor.cores`, `spark.dynamicAllocation.*`, `spark.serializer` | submit/defaults or builder before `getOrCreate()` |
| Static SQL | `spark.sql.extensions`, `spark.sql.catalogImplementation`, `spark.sql.warehouse.dir` | before session creation |
| Runtime SQL | `spark.sql.shuffle.partitions`, `spark.sql.adaptive.*`, `spark.sql.session.timeZone` | `spark.conf.set` or `SET k=v;` per session |

```python
spark.conf.isModifiable("spark.sql.shuffle.partitions")   # True
spark.conf.isModifiable("spark.executor.memory")          # False
```

## getOrCreate trap
`SparkSession.builder.config("spark.executor.memory","8g").getOrCreate()` in a notebook or a second module returns the **existing** session; core confs are not applied (the driver logs the warning "Using an existing Spark session; only runtime SQL configurations will take effect."). Restart the session/kernel or put it on the cluster config.

## Verify the effective value
```python
spark.sparkContext.getConf().get("spark.executor.memory")   # core conf as launched
spark.conf.get("spark.sql.shuffle.partitions")              # current session value
```
```sql
SET -v;                        -- all SQL confs with docs
SET spark.sql.adaptive.enabled;
```
The Spark UI **Environment** tab is where to verify the application runs with the configuration you expect.

## Gotchas
- Typos are not errors: `spark.sql.shuffle.partiton=50` is accepted and ignored. Check the Environment tab.
- `SPARK_WORKER_MEMORY` in `spark-env.sh` is a standalone-daemon setting (total memory a worker may give to applications), not an application property.

## Verify
- [ ] Each changed key is visible with the expected value in Environment tab or `getConf()`.
- [ ] No "only runtime SQL configurations will take effect" warning in driver logs.

## Checked
Checked 2026-10-25 against the Apache Spark documentation sources (apache/spark docs/ and SQLConf.scala on master, last commit 2026-10-24; docs site: spark.apache.org/docs/latest).
Confirmed: precedence (SparkConf, then spark-submit flags and --properties-file, then spark-defaults.conf) and the --properties-file / --load-spark-defaults rule in configuration.md; driver memory cannot be set via SparkConf in client mode; the 'only runtime SQL configurations will take effect' warning text in SparkSession.scala; SPARK_WORKER_MEMORY meaning in spark-standalone.md. Removed unconfirmed vendor-platform notes and the java-options merge claim.

Method: documentation only; no commands were run.
