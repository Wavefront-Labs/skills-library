---
id: computing-software.data-engineering.streaming-architecture.designing-streaming-joins
name: designing-streaming-joins
category: computing-software
field: data-engineering
product: streaming-architecture
tags: [streaming-architecture, streaming-join-design, stream-stream-join, temporal-join, interval-join, lookup-join, state-management]
level: advanced
status: draft
description: "Pick the right streaming join (interval, temporal/versioned, lookup, regular, windowed) by data shape and correctness needs, with state bounds and late-data behaviour."
sources:
  - https://nightlies.apache.org/flink/flink-docs-stable/docs/dev/table/sql/queries/joins/
  - https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html#join-operations
  - https://kafka.apache.org/documentation/streams/developer-guide/dsl-api.html#joining
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Designing streaming joins

Every streaming join keeps state for rows that may still match. The design question is **what bounds that state** and **which version of the other side** a row should see.

## Decision table
| Data shape | Join type | State bound | Engine names |
|---|---|---|---|
| Two event streams correlated in time (order and its payment within 1 h) | interval join | time interval + watermark | Flink interval join / SQL `BETWEEN` on rowtimes, Spark stream-stream join with watermarks + time constraint, Kafka Streams KStream-KStream `JoinWindows` |
| Events enriched with the version of a slowly changing entity valid **at event time** (price at order time) | temporal (versioned) join | versions per key older than watermark are dropped | Flink `FOR SYSTEM_TIME AS OF o.order_time` on a versioned table (upsert-kafka/CDC), Kafka Streams KStream-KTable with versioned stores (3.5+) |
| Events enriched with the **current** value from an external DB | lookup join | none in Flink (cache optional) | Flink `FOR SYSTEM_TIME AS OF o.proc_time` with JDBC/HBase lookup, Async I/O; Spark stream-static join |
| Events enriched with a changelog table, latest value at processing time | stream-table join | table size | Kafka Streams KStream-KTable, Spark stream-static (static reloaded per batch) |
| Two changelogs (tables) joined, result is a continuously updated table | regular join | unbounded: both sides forever | Flink regular join (set `table.exec.state.ttl`), Kafka Streams KTable-KTable, foreign-key join |
| Aggregates per window from both sides | window join | window size | Flink window join TVF, Spark windowed join |

## Correctness questions to answer
1. **Which version?** Processing-time lookups are non-deterministic on replay (enrichment uses today's value for last month's events). If correctness on replay matters, use a temporal join with event time and a CDC changelog of the dimension.
2. **What if the match arrives late or never?** Inner join drops unmatched rows silently. Outer interval joins emit unmatched rows (null-padded) only after the watermark passes the interval, adding latency. Decide explicitly, and route unmatched rows to a side output to monitor match rate.
3. **Co-partitioning**: both inputs must be partitioned by the join key with equal partition counts (Kafka Streams) or be shuffled by the engine (Flink/Spark do it). GlobalKTable/broadcast avoids repartitioning for small dimensions.
4. **Updates and retractions**: regular joins over changelogs emit retractions; sinks must be upsert-capable.

## State bounds
- Interval: state = rate x interval width x (1 + watermark delay). Keep intervals tight.
- Regular join: set TTL (and accept missed matches after TTL) or redesign as temporal/interval join.
- Lookup join with cache: `lookup.cache` partial caching with TTL trades freshness for DB load.

## Verify
- [ ] Match rate metric (matched / input) per join, alert on drops.
- [ ] Replay test: results identical for event-time-based joins.
- [ ] State size flat over days.
