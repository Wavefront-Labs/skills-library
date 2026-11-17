---
id: computing-software.data-engineering.apache-spark.debugging-and-profiling-pyspark
name: debugging-and-profiling-pyspark
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, pyspark, pyspark-profiler, udf-profiler, python-worker-logs, debugging, memory-profiler, pyspark-udfs]
level: advanced
status: docs-checked
description: "Debug and profile PySpark: find Python worker tracebacks, use the UDF CPU/memory profilers, faulthandler for hangs, and remote debugging of executor code."
sources:
  - https://spark.apache.org/docs/latest/api/python/development/debugging.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Debugging and profiling PySpark

## Where the error really is
- Driver-side Python errors appear in your notebook/console normally.
- Errors inside UDFs surface on the driver with the Python traceback in the message. `spark.sql.execution.pyspark.udf.simplifiedTraceback.enabled` is true by default and simplifies the traceback.
- `print()` inside a UDF runs on the executor: look in the executor logs linked from the Executors tab, not the driver console.
- Python worker crashes: check executor stderr and the container's OOM events. `spark.executor.pyspark.memory`, when set, limits PySpark memory per executor; when unset Spark does not limit it.
- Hung or crashing Python worker: `spark.python.worker.faulthandler.enabled` turns on Python fault-handler dumps (see the configuration page).

## UDF profilers
Session-based profiling:
```python
spark.conf.set("spark.sql.pyspark.udf.profiler", "perf")     # or "memory"
df.select(my_udf("x")).collect()
spark.profile.show(type="perf")
```
Older approach: `spark.python.profile=true` and `sc.show_profiles()` (see the configuration page).

## Driver-side profiling
Most "slow PySpark" is actually slow JVM stages. Check the SQL tab first: if `ArrowEvalPython` (Python UDF evaluation) nodes dominate, the Python is the bottleneck; otherwise tune the plan, not the Python.

## Remote debugging
See the PySpark debugging page for remote-debugging setups; on a cluster, reproduce on a small sample locally.

## Verify
- [ ] The failing input row is identified (wrap UDF body in try/except that returns the row id and error string while debugging).
- [ ] Profile shows the top functions; optimisation reduces their cumulative time.

## Checked

2026-10-28. Confirmed against: PySpark debugging and profiling page (simplifiedTraceback default true, spark.sql.pyspark.udf.profiler perf/memory, spark.profile.show), configuration page (spark.executor.pyspark.memory, spark.python.profile, faulthandler setting name), Spark web UI page (executor logs link). Removed (not confirmable in the fetched pages): exception message strings, py-spy, version gates, memory-profiler note, profile.dump/clear, BatchEvalPython, debugpy/pydevd instructions.

Method: documentation only; no commands were run.
