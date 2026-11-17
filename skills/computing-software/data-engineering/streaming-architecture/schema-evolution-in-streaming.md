---
id: computing-software.data-engineering.streaming-architecture.schema-evolution-in-streaming
name: schema-evolution-in-streaming
category: computing-software
field: data-engineering
product: streaming-architecture
tags: [streaming-architecture, schema-evolution, long-running-state, rolling-deployment, avro-evolution, protobuf-evolution, stateful-operator-migration, blue-green-streaming, dual-write, backward-compatibility]
level: advanced
status: draft
description: "Evolve message schemas in a live streaming pipeline without breaking in-flight state, joins or downstream consumers."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources:
  - https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Schema evolution in streaming — harder than evolving a database column

**Goal:** change a message schema while a stateful streaming job keeps running for weeks or months, without restarting from scratch or corrupting in-flight state. This is specifically about the *stateful streaming job's* side of schema evolution — computing-software.data-engineering.apache-kafka.schema-registry-and-compatibility covers the registry/compatibility-mode mechanics on the wire-format side this builds on.

## 1. Why streaming schema evolution is a harder problem than batch
A batch job reads a schema, runs, and exits — the next run just reads whatever schema is current. A **stateful streaming job keeps state alive across the schema change**: a windowed aggregation, a long-lived join, or accumulated session state was built from the old schema's shape and keeps running while new messages in the new schema start arriving. The job has to correctly interpret old-schema-shaped accumulated state alongside new-schema-shaped incoming events, often indefinitely (state built before the change may not expire for the state's full TTL) — this is a fundamentally different problem from "the next batch run sees the new schema."

## 2. What actually breaks, specifically
- **Deserializer failures**: a consumer compiled against the old generated class (Avro/Protobuf codegen) encountering a new, incompatible field addition without proper default handling throws at deserialize time, not at some "schema check" step — this surfaces as a sudden spike in deserialization-error-routed dead-letter records exactly at the moment a producer deploys the new schema, correlating with the deploy if anyone's watching for that correlation.
- **Stateful operator state schema mismatch** (Flink/Kafka Streams/Spark Structured Streaming): if the *keyed state's own* serialized representation changes (not just the input message schema, but the aggregation's internal accumulator type), restoring from a checkpoint/savepoint taken before the change can fail outright or (worse) silently misinterpret bytes — see computing-software.data-engineering.apache-flink.state-backends-and-savepoints for the Flink-specific uid/schema-evolution mechanics; the general principle (test restore against a real snapshot before deploying a change that touches accumulator types) applies across engines.
- **Join key/shape mismatch across streams**: a stream-stream join assumes both sides' schemas evolve compatibly with each other, not just independently — if one side adds a field the join logic now depends on before the other side's producers have deployed it, the join silently treats every row as if that field were absent/default rather than erroring.

## 3. The safe evolution pattern
1. **Additive-only changes while the job is running** — add a field with a default, never remove/rename/retype a field a running job's deserializer or state logic depends on. This is backward-compatible under BACKWARD or FULL compatibility mode (see the schema-registry skill) and is restorable from existing state without special handling.
2. **For changes that aren't additive** (a field removal, a type change, a key schema change): treat it as a new logical stream/topic version, not an in-place mutation. Run the new-schema pipeline **in parallel** against a new topic/table (dual-write from the producer, or a migration job translating old→new), validate its output matches expectations over a real time window, then cut consumers over and decommission the old pipeline — rather than attempting an in-place schema swap on a running stateful job and hoping restore handles it.
3. **For stateful jobs specifically**: a non-additive change to anything the accumulator/state depends on usually means resetting state (a fresh start from a point in time, accepting the loss of accumulated history) or a deliberate state-migration job that reads the old savepoint/checkpoint format and rewrites it into the new one before the new job version starts — test this migration path against production-scale state before relying on it, it is not something most engines do automatically.

## 4. Rolling deploys and the mixed-version window
During a rolling deploy, producers and consumers running old and new code coexist for some period — every schema change must be safe for that mixed-version window, not just safe "once everyone's upgraded." This is the practical reason compatibility mode (BACKWARD/FORWARD/FULL) must match the actual deploy order: if consumers deploy first, the new consumer code must handle both old and new producer output (BACKWARD on the consumer's read path); if producers deploy first, old consumers still running must tolerate the new producer output (FORWARD) until they're upgraded.

## Verify
- [ ] Every schema change was reviewed for whether it's additive-only (safe for a running stateful job) or structural (needs a parallel-pipeline migration) before deploying.
- [ ] A test restore from a real checkpoint/savepoint taken before the change succeeds after deploying the new schema, for any change touching state-dependent fields.
- [ ] The compatibility mode (BACKWARD/FORWARD/FULL) matches the actual rollout order of producers vs consumers for this specific change.
- [ ] A non-additive change went through parallel validation (new pipeline's output checked against expectations) before cutover, not an in-place swap.
