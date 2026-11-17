---
id: computing-software.data-engineering.streaming-architecture.streaming-databases
name: streaming-databases
category: computing-software
field: data-engineering
product: streaming-architecture
tags: [streaming-architecture, streaming-database, materialize, risingwave, incremental-view-maintenance, ksqldb, postgres-wire-protocol]
level: practitioner
status: draft
description: "Evaluate streaming databases (Materialize, RisingWave, ksqlDB) for incrementally maintained SQL views: when they beat Flink plus a serving DB, consistency models and limits."
sources:
  - https://materialize.com/docs/
  - https://docs.risingwave.com/
  - https://docs.confluent.io/platform/current/ksqldb/overview.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Streaming databases (Materialize / RisingWave)

A streaming database ingests streams (Kafka, CDC from Postgres/MySQL) and keeps **materialized views incrementally up to date**, then serves queries over them through a SQL (Postgres wire protocol) endpoint. It merges the stream processor and the serving store.

```sql
-- RisingWave / Materialize style
CREATE SOURCE orders FROM KAFKA (...) FORMAT ... ;            -- syntax differs per product
CREATE MATERIALIZED VIEW revenue_by_region AS
  SELECT r.name, date_trunc('minute', o.ts) AS minute, sum(o.amount) AS revenue
  FROM orders o JOIN regions r ON o.region_id = r.id
  GROUP BY r.name, date_trunc('minute', o.ts);
SELECT * FROM revenue_by_region WHERE name = 'EMEA' ORDER BY minute DESC LIMIT 10;   -- served directly
```
Any Postgres client, BI tool or app driver can query the view; `SUBSCRIBE` (Materialize) or sinks push changes out.

## Products
| | Materialize | RisingWave | ksqlDB |
|---|---|---|---|
| Engine | Timely/Differential Dataflow (Rust) | Rust, own storage on S3 (Hummock LSM) | Kafka Streams |
| Consistency | strict serializability across views ("virtual time") | consistent snapshots per barrier (checkpoint interval) | eventual per query |
| SQL | broad Postgres dialect, complex joins, recursive | broad Postgres dialect | limited dialect, push/pull queries |
| State | memory + disk-spilling (newer releases) | object storage-backed, scales state cheaply | RocksDB + changelog topics |
| Deployment | cloud and self-managed | open source (Apache 2.0) and cloud | Confluent (maintenance mode; Confluent steers to Flink SQL) |

## When they fit
- Many teams need live SQL views (dashboards, operational APIs) joining several streams/CDC tables, and you do not want Flink jobs plus a separate serving DB plus glue.
- Complex multi-way joins and aggregations where consistency across views matters (Materialize).
- Postgres-compatible serving is valuable (existing tools).

## When Flink + serving store is better
- Very high throughput with custom logic (UDF-heavy, CEP, ML features with complex state).
- Mature operational tooling and broad connector ecosystem required.
- Outputs mainly flow to other systems (lakehouse, Kafka) rather than being queried in place.

## Evaluation checklist
- Supported sources/sinks and CDC formats; exactly-once ingestion from your Kafka setup.
- Query patterns: are your joins supported incrementally (some non-equi joins, window functions, or `ORDER BY ... LIMIT` per group may be costly or unsupported)?
- State size and cost at your cardinality; recovery time after a failure.
- Freshness SLO: end-to-end lag under peak load.

## Verify
- [ ] Proof of concept with production-scale replay: view lag, query latency, and cost measured.
- [ ] View results match a batch query over the same data snapshot.
