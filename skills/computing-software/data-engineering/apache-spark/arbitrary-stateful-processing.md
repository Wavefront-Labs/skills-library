---
id: computing-software.data-engineering.apache-spark.arbitrary-stateful-processing
name: arbitrary-stateful-processing
category: computing-software
field: data-engineering
product: apache-spark
tags: [apache-spark, spark, structured-streaming, transformwithstate, flatmapgroupswithstate, applyinpandaswithstate, stateful-processing, timers, state-ttl, groupstate, rocksdb-state-store, sessionization]
level: sme
status: docs-checked
description: "Custom stateful streaming in Spark: transformWithState (4.0) and the older flatMapGroupsWithState/applyInPandasWithState, timeouts/timers, TTL, and state schema rules."
sources:
  - https://spark.apache.org/docs/latest/streaming/structured-streaming-transform-with-state.html
  - https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#arbitrary-stateful-operations
  - https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.GroupedData.applyInPandasWithState.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arbitrary stateful processing in Structured Streaming

**Goal:** implement per-key logic the built-in aggregations cannot express (custom sessionization, alert-once-per-condition, running state machines) with bounded state.

## Which API
| API | Spark | Notes |
|---|---|---|
| `transformWithState` | 4.0+ | The guide encourages it since Spark 4.0 as the replacement for the older operators |
| `flatMapGroupsWithState` / `mapGroupsWithState` | Scala/Java, since 2.2 | Legacy operators: user code over grouped datasets that updates state |
| `applyInPandasWithState` | Python | Python counterpart of the legacy operators |

## applyInPandasWithState
Signature: `GroupedData.applyInPandasWithState(func, outputStructType, stateStructType, outputMode, timeoutConf)`. The PySpark API page gives the function contract and a worked example.

## transformWithState essentials (4.0)
- Implement a `StatefulProcessor`: `init` (declare state variables, for example `getValueState`), `handleInputRows` (process the rows of a grouping key and emit output), `handleExpiredTimer` (handle expired timers) and `close` (cleanup). The transformWithState page covers timers, TTL and the other state variable types.

## Rules
- **Always expire state**: timeouts/timers or TTL. Keys that never come back otherwise live forever.
- Check the docs for the state-schema change rules of each API; plan for a new checkpoint if a legacy operator's state schema must change.
- Python state functions run in Python workers: watch memory overhead and Arrow batch sizes (`spark.sql.execution.arrow.maxRecordsPerBatch`).

## Verify
- [ ] Unit test the state function with a local batch DataFrame / memory stream and crafted event sequences, including a timeout.
- [ ] State row count (query progress `stateOperators`) is bounded under a soak test.
- [ ] Restarting from the checkpoint resumes without duplicate alerts.

## Checked

2026-10-28. Confirmed against: transformWithState page (StatefulProcessor methods init/handleInputRows/handleExpiredTimer/close, getValueState, replacement for mapGroupsWithState/flatMapGroupsWithState/applyInPandasWithState since 4.0), PySpark applyInPandasWithState API page (signature), Structured Streaming guide (legacy operators since 2.2, stateOperators in progress). Removed (not confirmable in the fetched pages): applyInPandasWithState example body, version gates for Python, list/map state and TTL claims, timer registration calls, RocksDB requirement, ordering claim, schema-evolution claim.

Method: documentation only; no commands were run.
