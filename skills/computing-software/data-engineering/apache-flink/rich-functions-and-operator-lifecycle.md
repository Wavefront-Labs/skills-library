---
id: computing-software.data-engineering.apache-flink.rich-functions-and-operator-lifecycle
name: rich-functions-and-operator-lifecycle
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, rich-functions, operator-lifecycle, open-close, runtime-context, datastream-api]
level: practitioner
status: docs-checked
description: "Use Flink rich functions correctly: open/close lifecycle, per-subtask clients and caches, RuntimeContext (state, metrics, subtask index), and serialization pitfalls."
sources:
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/datastream/user_defined_functions/#rich-functions
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/internals/task_lifecycle/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rich functions and operator lifecycle

Every user function (`MapFunction`, `FlatMapFunction`, `FilterFunction`, sinks...) has a `Rich*` variant (`RichMapFunction` etc.); `ProcessFunction`s are already rich.

## Lifecycle per parallel subtask
1. The function object is **serialised on the client** and deserialised in each subtask. Fields must be serialisable or `transient`.
2. `open(OpenContext)` in current releases (older ones: `open(Configuration)`): create clients, connections, caches, state handles, metrics.
3. `map`/`flatMap`... per record.
4. `close()`: release resources. Called on normal finish **and** on cancellation/failure; make it idempotent and null-safe.
5. On failover, a new instance is created and `open` runs again; nothing survives except Flink state.

```java
public class Enrich extends RichMapFunction<Event, Enriched> {
  private transient HttpClient client;            // not serialisable: transient + created in open
  private transient Counter misses;
  private final String endpoint;                  // config: plain serialisable field
  public Enrich(String endpoint) { this.endpoint = endpoint; }
  @Override public void open(OpenContext ctx) {
    client = HttpClient.newHttpClient();
    misses = getRuntimeContext().getMetricGroup().counter("cache_misses");
    int idx = getRuntimeContext().getTaskInfo().getIndexOfThisSubtask();   // older: getIndexOfThisSubtask()
  }
  @Override public Enriched map(Event e) { ... }
  @Override public void close() { /* client has no close; close pools/connections here */ }
}
```

## RuntimeContext gives you
- Keyed/operator state handles (`getState`, `getListState`, `getMapState`).
- Metric group for custom metrics.
- Task info: subtask index, parallelism, attempt number (useful for sharding external work or seeding).
- Distributed cache files (registered with `env.registerCachedFile`).
- User classloader (for dynamic class loading).

## Pitfalls
- Creating a client inside `map` per record: connection storms and slow jobs.
- A non-transient field holding a client: `NotSerializableException` at job submission.
- Static fields are shared by all subtasks in the same TaskManager JVM (slots share a JVM): fine for immutable caches, dangerous for mutable state or anything with per-subtask identity.
- Heavy work in `open` delays task start; keep it bounded (timeouts) or the task fails to reach RUNNING.
- Blocking network calls in `map` throttle throughput; use Async I/O instead.

## Verify
- [ ] Logs show `open` once per subtask, and `close` on cancel.
- [ ] Job graph submission works with a mini cluster in a unit test (catches serialization errors early).

## Checked

2026-10-28. Confirmed: open(OpenContext) is used in the current State Processor API examples. Removed: version numbers for the open() change, a quoted error and DataSet-era broadcast variables.

Method: documentation only; no commands were run.
