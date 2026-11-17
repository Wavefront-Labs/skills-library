---
id: computing-software.data-engineering.streaming-architecture.choosing-a-stream-processor
name: choosing-a-stream-processor
category: computing-software
field: data-engineering
product: streaming-architecture
tags: [streaming-architecture, stream-processor-selection, apache-flink, kafka-streams, spark-structured-streaming, streaming-sql, materialize, risingwave, architecture-decision]
level: advanced
status: draft
description: "Choose a stream processing engine (Flink, Kafka Streams, Spark Structured Streaming, streaming SQL databases, managed services) by latency, state, deployment model and team skills."
sources:
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/overview/
  - https://kafka.apache.org/documentation/streams/
  - https://spark.apache.org/docs/latest/streaming/index.html
  - https://docs.risingwave.com/get-started/intro
  - https://materialize.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing a stream processor

**Goal:** pick the engine whose operational model and semantics match the workload, instead of the one with the most conference talks.

## 1. Options at a glance
| Engine | Model | Latency | State | Deploy | Sweet spot |
|---|---|---|---|---|---|
| Apache Flink | dataflow cluster, DataStream + SQL | ms | very large (RocksDB, incremental checkpoints) | cluster (K8s operator) or managed (Confluent, AWS Managed Flink, Ververica) | complex event-time logic, big state, exactly-once across sources/sinks |
| Kafka Streams | library inside your app | ms | local RocksDB + changelog topics | just your service (any JVM deploy) | Kafka-in/Kafka-out microservices |
| Spark Structured Streaming | micro-batch (and real-time mode in newer versions) | ~100 ms-s | moderate (RocksDB state store) | Spark cluster / Databricks | lakehouse pipelines, teams already on Spark, batch+stream code reuse |
| Streaming SQL DBs (RisingWave, Materialize) | incrementally maintained views, Postgres wire protocol | ms-s | managed internally | service | SQL-only teams, serving fresh query results |
| Managed cloud (Google Dataflow / Apache Beam, Azure Stream Analytics, Kinesis Data Analytics=Managed Flink) | various | ms-s | managed | serverless-ish | single-cloud shops wanting low ops |
| ksqlDB | SQL on Kafka Streams | ms | Kafka Streams | Confluent | simple Kafka transforms (check product status/roadmap) |

## 2. Questions that decide it
1. **Latency need**: seconds-minutes → micro-batch (Spark, even triggered batch) is fine and cheaper to run. Sub-second → Flink/Kafka Streams.
2. **Sources and sinks**: only Kafka → Kafka Streams is simplest; many heterogeneous sources/sinks, CDC, lakehouse tables → Flink or Spark.
3. **State size and time semantics**: TB-scale keyed state, complex event-time joins, timers → Flink.
4. **Deployment model**: library in an existing service (Kafka Streams) vs a separate cluster (Flink/Spark) vs managed service.
5. **Language and skills**: JVM (Flink/Kafka Streams), Python/SQL (Spark, Flink SQL/PyFlink, streaming DBs).
6. **Reprocessing**: how will you replay history? Kafka retention/tiered storage + same job (Kappa), or batch backfill from the lake.
7. **Operations**: who runs checkpoints, upgrades, savepoints, scaling, 24/7 on-call?

## 3. Heuristics
- Lakehouse team on Databricks needing minute-level freshness → Spark Structured Streaming / Lakeflow pipelines.
- Event-driven microservices enriching Kafka topics → Kafka Streams.
- Fraud/real-time features with large state and strict event time → Flink (managed if possible).
- Analysts need always-fresh SQL views over CDC → streaming SQL database.
- Don't run two general-purpose engines without a clear reason; each costs an on-call skill set.

## 4. PoC checklist
Build one representative job: windowed aggregation with late data, a stream-table join, a restart from checkpoint, a schema change, a code upgrade with state retained, and a replay of one day. Measure throughput, p99 latency, recovery time and ops effort.

## Verify
- [ ] Decision record states latency/state/semantics requirements and why the engine meets them.
- [ ] PoC included upgrade-with-state and replay scenarios.
- [ ] Ownership for 24/7 operation is assigned before production.
