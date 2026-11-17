---
id: computing-software.data-engineering.apache-flink.testing-flink-jobs
name: testing-flink-jobs
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink-testing, minicluster, operator-test-harness, keyedoneinputstreamoperatortestharness, junit, integration-tests, datastream-api]
level: advanced
status: docs-checked
description: "Test Flink jobs at three levels: plain unit tests for functions, operator test harnesses for state and timers, and MiniCluster integration tests with pluggable sources and sinks."
sources:
  - https://raw.githubusercontent.com/apache/flink/release-2.4/docs/content/docs/dev/datastream/testing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing Flink jobs

**Goal:** catch logic, state and timing bugs in CI. The docs advise unit-testing the classes holding business logic as much as possible, since Flink itself can be assumed correct outside user-defined functions.

## 1. Stateless, timeless functions: plain unit tests
Instantiate the function, call `map(...)` and assert the result. For functions using a `Collector` (`FlatMapFunction`, `ProcessFunction`), pass a mock collector (the page uses Mockito) and verify the `collect` calls.

## 2. Stateful or timer-based functions and custom operators: test harnesses
Harness classes:
- `OneInputStreamOperatorTestHarness`, `KeyedOneInputStreamOperatorTestHarness`, `TwoInputStreamOperatorTestHarness`, `KeyedTwoInputStreamOperatorTestHarness`.
- Keyed variants take a `KeySelector` plus `TypeInformation` for the key class.
- Extra test dependencies are required (see the configuration/testing page).
```java
testHarness = new OneInputStreamOperatorTestHarness<>(new StreamFlatMap<>(fn));
testHarness.open();                         // also calls open() on RichFunctions
testHarness.processElement(2L, 100L);       // timestamped element
testHarness.processWatermark(100L);         // triggers event-time timers
testHarness.setProcessingTime(100L);        // triggers processing-time timers
testHarness.getOutput();                    // emitted records
testHarness.getSideOutput(new OutputTag<>("invalidRecords"));  // ProcessFunction only
```
- For a `ProcessFunction`, the `ProcessFunctionTestHarnesses` factory (e.g. `forProcessFunction`) makes setup easier; the page points to `ProcessFunctionTestHarnessesTest` for KeyedProcessFunction, KeyedCoProcessFunction and BroadcastProcessFunction examples. `harness.extractOutputValues()` returns the output values.
- `WindowOperatorTest` in the Flink code base is cited as a good example for time-dependent operators.
- Caveat: `AbstractStreamOperatorTestHarness` and subclasses are not part of the public API and can change.

## 3. Whole jobs: MiniCluster
`MiniClusterWithClientResource` (JUnit rule, needs `flink-test-utils` test dependency) runs a job on an embedded mini cluster; configure it with `MiniClusterResourceConfiguration.Builder` (task managers, slots per task manager).
- Make sources and sinks pluggable in production code and inject test sources and sinks.
- Operators are serialized before distribution, so a test sink collecting results needs a static variable (e.g. a synchronized list that you clear before each test), or write to files in a temp directory.
- If the job uses event-time timers, the page suggests a custom parallel source that emits watermarks.
- Test with parallelism greater than 1 to expose bugs that only appear in parallel runs.
- Prefer `@ClassRule` over `@Rule` so tests share one cluster; cluster startup and shutdown usually dominate test time.
- To test custom state handling, enable checkpointing and restart the job in the mini cluster by throwing an exception from a test-only user-defined function.

## Checked
Method: 2026-11-08 read the Flink release-2.4 datastream testing page in full. Removed unsupported content: the JUnit 5 MiniClusterExtension, `executeAndCollect`/`fromData` code, harness snapshot/restore and `numKeyedStateEntries` checks, Table/SQL testing, Testcontainers advice, the ordering and closure gotchas and the verify checklist. Replaced with the page's own recommendations; description adjusted.
