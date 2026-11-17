---
id: computing-software.data-engineering.apache-flink.flink-user-defined-functions
name: flink-user-defined-functions
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, flink-sql, table-api, flink-udf, scalarfunction, tablefunction, aggregatefunction, pyflink-udf, type-inference]
level: practitioner
status: docs-checked
description: "Write and register Flink SQL/Table UDFs: scalar, table and aggregate functions in Java, type hints, open/close setup, determinism, PyFlink vectorized UDFs and deployment."
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/dev/table/functions/udfs/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/reference/ddl/create/#create-function
  - https://github.com/apache/flink/blob/release-2.3/flink-python/docs/user_guide/table/udfs.rst
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Flink user-defined functions

**Goal:** extend Flink SQL with custom logic that is correctly typed, efficient, and deployable without restarting the SQL gateway.

## 1. Scalar function (one row → one value)
```java
public class MaskEmail extends ScalarFunction {
  public String eval(String email) {
    if (email == null) return null;
    int at = email.indexOf('@');
    return at < 0 ? "***" : "***" + email.substring(at);
  }
}
```
Overloads: multiple `eval` methods. Types are derived by reflection from the class and its evaluation methods; `@DataTypeHint` and `@FunctionHint` supply types where that is not enough (for example `@DataTypeHint("DECIMAL(18,2)")`).

## 2. Table function (one row → many rows)
```java
@FunctionHint(output = @DataTypeHint("ROW<word STRING, len INT>"))
public class SplitWords extends TableFunction<Row> {
  public void eval(String s) {
    if (s == null) return;
    for (String w : s.split("\\s+")) collect(Row.of(w, w.length()));
  }
}
```
```sql
SELECT d.id, t.word FROM docs AS d, LATERAL TABLE(SplitWords(d.body)) AS t(word, len);
-- keep rows that produce nothing:
SELECT ... FROM docs d LEFT JOIN LATERAL TABLE(SplitWords(d.body)) AS t(word, len) ON TRUE;
```

## 3. Aggregate function
```java
public class WeightedAvg extends AggregateFunction<Double, WeightedAvg.Acc> {
  public static class Acc { public double sum = 0; public long weight = 0; }
  public Acc createAccumulator() { return new Acc(); }
  public void accumulate(Acc a, Double v, Long w) { if (v != null && w != null) { a.sum += v * w; a.weight += w; } }
  public void retract(Acc a, Double v, Long w) { if (v != null && w != null) { a.sum -= v * w; a.weight -= w; } }  // required for OVER window aggregations
  public void merge(Acc a, Iterable<Acc> it) { for (Acc o : it) { a.sum += o.sum; a.weight += o.weight; } } // session/hop windows, many bounded aggregations, two-phase agg
  public Double getValue(Acc a) { return a.weight == 0 ? null : a.sum / a.weight; }
}
```
Accumulators are state, so keep them small. `TableAggregateFunction` is the variant that can emit multiple rows.

## 4. Lifecycle and determinism
- `open(FunctionContext ctx)` for expensive setup (for example read `ctx.getJobParameter(name, defaultValue)`); `close()` to release.
- Override `isDeterministic()` to return `false` for functions that are not purely functional (random, current time); the default is `true`, and the planner may pre-evaluate deterministic calls with constant arguments during planning.
- A plain `ScalarFunction` calling an external system is a synchronous request per row; the UDF docs describe asynchronous scalar and table functions for such lookups.

## 5. Register
```sql
CREATE TEMPORARY SYSTEM FUNCTION mask_email AS 'com.example.udf.MaskEmail' LANGUAGE JAVA;
CREATE FUNCTION analytics.mask_email AS 'com.example.udf.MaskEmail' LANGUAGE JAVA
  USING JAR 's3://<artifacts-bucket>/udfs/udfs-1.4.0.jar';         -- catalog function; the statement supports a USING clause with jar paths
```
Table API: `tEnv.createTemporarySystemFunction("mask_email", MaskEmail.class);`. Versioned jar names are a deployment convention, not a Flink requirement.

## 6. PyFlink
```python
from pyflink.table.udf import udf
from pyflink.table import DataTypes
@udf(result_type=DataTypes.DOUBLE(), func_type="pandas")     # vectorized: receives pandas.Series batches
def fx_convert(amount, rate): return amount * rate
t_env.create_temporary_system_function("fx_convert", fx_convert)
```
Vectorized Python UDFs (`func_type="pandas"`) transfer batches between the JVM and Python in Arrow columnar format, which reduces serialization and invocation overhead compared with non-vectorized UDFs.

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the User-defined Functions page (base-class methods `open`, `close`, `isDeterministic`, `supportsConstantFolding`; `FunctionContext.getJobParameter`; type inference with `@DataTypeHint`/`@FunctionHint`; table functions with `LATERAL TABLE` and `LEFT JOIN ... ON TRUE`; aggregate `createAccumulator`/`accumulate`/`retract`/`merge` requirements; async scalar functions), the CREATE FUNCTION grammar (`TEMPORARY SYSTEM`, `LANGUAGE`, `USING JAR`) and the PyFlink UDF guide (`func_type="pandas"`, Arrow batches, `create_temporary_system_function`). Corrected the `retract` requirement (OVER aggregations) and the blocking-UDF advice; removed unconfirmed Python worker and managed-memory statements.

Method: documentation only; no commands were run.

## Verify
- [ ] Unit tests call `eval`/`accumulate`/`retract` directly, including NULL inputs.
- [ ] `EXPLAIN` shows the UDF types as intended (no unexpected RAW/STRING casts).
- [ ] UDF jar is versioned and the SQL references a specific version.
