---
id: computing-software.data-engineering.apache-flink.flink-sql-and-table-api
name: flink-sql-and-table-api
category: computing-software
field: data-engineering
product: apache-flink
tags: [apache-flink, flink, flink-sql, table-api, flink-cdc, temporal-join, interval-join, watermark-ddl, dynamic-tables, retract-stream, upsert-kafka, sql-client, ververica, confluent-flink]
level: practitioner
status: docs-checked
description: "When to use Flink SQL/Table API instead of the DataStream API, and the gotchas around time attributes, joins and connectors."   # quoted: YAML would cut an unquoted value at " #" or choke on ": "
sources:
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/overview/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/concepts/sql-table-concepts/dynamic_tables/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/sql/reference/queries/joins/
  - https://nightlies.apache.org/flink/flink-docs-release-2.3/docs/concepts/sql-table-concepts/time_attributes/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Flink SQL and the Table API — when they're the right tool

**Goal:** get streaming joins, windows and aggregations working in hours with SQL instead of weeks of hand-rolled DataStream operators, and know when SQL's abstractions leak and you need the lower-level API.

## 1. When SQL/Table API is the right call
Standard relational-shaped work — filtering, windowed aggregation, stream-stream and stream-table joins, upserts into a sink — is faster to write, read and maintain as Flink SQL than as DataStream code. Reach for DataStream/ProcessFunction instead when you need: custom state beyond what windows/joins express, fine-grained timer control, complex multi-output routing, or a `KeyedProcessFunction`-level event-time pattern SQL can't express directly. Table API and DataStream interoperate (`StreamTableEnvironment.fromDataStream`/`toDataStream`) — mixing them in one job for the parts each is best at is normal, not a hack.

## 2. Dynamic tables are streams in disguise — know your stream kind
A Flink SQL table over a stream is a **dynamic table**: continuously changing, emitting rows as inserts, updates, or deletes depending on the query. A `GROUP BY` aggregation without a window emits an unbounded sequence of **retractions and updates** (an "update-changelog" stream, not append-only) as each group's running result changes — the sink must be able to consume update changes, so check the query's changelog mode (`EXPLAIN CHANGELOG_MODE`) against what the sink connector accepts. Appending such a result to an append-only sink is the usual first problem moving from toy windowed queries to real aggregation pipelines.

## 3. Time attributes and watermarks are DDL, not code
Event time comes from a `WATERMARK FOR <col> AS <col> - INTERVAL '5' SECOND` clause on the table DDL — get the source column and bound wrong here and every windowed/temporal query downstream silently uses the wrong lateness tolerance. Processing-time attributes (`PROC_TIME AS PROCTIME()`) skip watermarks entirely — fine for non-deterministic, replay-unsafe use cases only; never use proctime where exactly-reproducible backfills matter.

## 4. Joins — pick the right one for the semantics you need
- **Regular (unbounded) join**: both sides' full history kept as state forever (or until TTL) — state grows unbounded without idle-state retention config (`table.exec.state.ttl`). Fine for small dimension tables, dangerous for two large unbounded streams.
- **Interval join**: needs at least one equi-join predicate plus a time-bounding condition such as `a.ts BETWEEN b.ts - INTERVAL '1' HOUR AND b.ts` — correct for "events that happened near each other in time."
- **Temporal join** (`FOR SYSTEM_TIME AS OF`): joins a stream against the state of a changing dimension table *as it was* at the stream row's event time — the right tool for "enrich with the dimension value valid at that point in time," avoiding both unbounded state and the "which version of the dimension row" ambiguity a regular join has.
- **Lookup join**: `FOR SYSTEM_TIME AS OF` a processing-time attribute against a table backed by a lookup source connector (the docs example uses JDBC) — use for slow-changing reference data that's too large to keep as Flink state, accepting lookup latency per row.

## 5. CDC ingestion
Change-data-capture sources (the separate Apache Flink CDC project) can feed a database's change log into a Flink dynamic table. Check the Flink CDC documentation for supported databases, Flink version compatibility and snapshot behaviour before pointing it at a production OLTP primary (not covered by the Flink core docs).

## Checked

2026-10-25 against the Apache Flink 2.3.0 documentation (release-2.3 branch on GitHub). Confirmed from the Dynamic Tables, Joins (regular, interval, temporal, lookup), Time Attributes, DataStream API integration and EXPLAIN pages and the generated configuration table (`table.exec.state.ttl`). Removed the unconfirmed error string, connector names and Flink CDC specifics; Flink CDC is a separate project whose documentation was not checked, so the skill only points to it.

Method: documentation only; no commands were run.

## Verify
- [ ] Every event-time query's source table has an explicit `WATERMARK FOR` clause reviewed for correct lateness bound — not left at a copy-pasted default.
- [ ] An unbounded `GROUP BY`/join's sink is a connector that accepts the query's changelog mode, not an append-only sink.
- [ ] State TTL (`table.exec.state.ttl`) is set for any unbounded regular join or aggregation on an open-ended key space; the docs warn this can affect result correctness.
- [ ] A temporal join was chosen over a regular join wherever "value of the dimension as of event time" is the actual requirement.
