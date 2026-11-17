---
id: computing-software.cloud-infrastructure-engineering.aws.purpose-built-databases-selection
name: purpose-built-databases-selection
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, purpose-built-databases, documentdb, neptune, keyspaces, timestream, qldb, mongodb-compatible, graph-database, gremlin, opencypher, sparql, cassandra-compatible, cql, time-series, ledger, immutable-ledger, opensearch, memorydb, database-selection, nosql, workload-fit, migration-off-qldb]
level: advanced
status: draft
description: "Choose and run AWS purpose-built databases: DocumentDB (MongoDB API), Neptune (graph), Keyspaces (Cassandra), Timestream, QLDB (retiring) and MemoryDB, with their compatibility and sizing traps."
sources: ["https://docs.aws.amazon.com/documentdb/latest/developerguide/what-is.html", "https://docs.aws.amazon.com/documentdb/latest/developerguide/functional-differences.html", "https://docs.aws.amazon.com/neptune/latest/userguide/intro.html", "https://docs.aws.amazon.com/keyspaces/latest/devguide/what-is-keyspaces.html", "https://docs.aws.amazon.com/timestream/latest/developerguide/what-is-timestream.html", "https://docs.aws.amazon.com/qldb/latest/developerguide/what-is.html", "https://docs.aws.amazon.com/memorydb/latest/devguide/what-is-memorydb.html", "https://aws.amazon.com/products/databases/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Purpose-built databases — DocumentDB, Neptune, Keyspaces, Timestream, QLDB, MemoryDB

**Goal:** pick the engine whose data model matches the workload *and* whose
compatibility gaps you can live with, size it the way that engine bills, and know the
exit path before you commit. Relational (RDS/Aurora), key-value (DynamoDB), cache
(ElastiCache) and warehouse (Redshift) have their own skills.

## 1. Selection table
| Workload shape | Service | Compatible API | Billing unit |
|---|---|---|---|
| JSON documents, MongoDB drivers, flexible schema, rich queries | **DocumentDB** | MongoDB 4.0/5.0 wire protocol (subset) | Instance-hours + storage + I/O (or I/O-Optimized); Elastic clusters by shard capacity |
| Highly connected data: recommendations, fraud rings, knowledge graphs, identity | **Neptune** | Gremlin, openCypher, SPARQL (RDF) | Instance-hours (+ Serverless NCUs) + storage + I/O |
| Wide-column, Cassandra apps, high write throughput, no ops | **Keyspaces** | CQL 3.x (subset) | On-demand or provisioned RRU/WRU + storage |
| Metrics/IoT/telemetry, time-windowed queries, downsampling | **Timestream** (for LiveAnalytics; also Timestream for InfluxDB) | SQL (Timestream) / InfluxDB API | Writes + memory-store + magnetic-store GB + bytes scanned |
| Immutable, cryptographically verifiable history | **QLDB** | PartiQL, ION; journal | I/O requests + storage — **retiring**; new designs use Aurora PostgreSQL + verification, see §6 |
| Redis-compatible **primary** store needing durability | **MemoryDB** | Valkey/Redis | Node-hours + data written |
| Full-text / log search / vector | OpenSearch Service | OpenSearch REST | Instance-hours / OCU |
If the honest answer is "relational with a JSON column" → Aurora PostgreSQL `jsonb`.
If it is "key-value at scale" → DynamoDB. Purpose-built engines earn their keep only
when the access pattern needs their model.

## 2. DocumentDB
```bash
aws docdb create-db-cluster --db-cluster-identifier docs --engine docdb --engine-version 5.0.0 \
  --master-username admin --master-user-password <PASSWORD> --storage-encrypted --db-subnet-group-name private \
  --vpc-security-group-ids sg-docdb --backup-retention-period 7 --deletion-protection \
  --db-cluster-parameter-group-name docs-50   # tls=enabled, audit_logs=enabled, ttl_monitor=enabled
aws docdb create-db-instance --db-cluster-identifier docs --db-instance-identifier docs-1 --db-instance-class db.r6g.large --engine docdb
mongosh "mongodb://admin:<PASSWORD>@docs.cluster-xxxx.<REGION>.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=global-bundle.pem&replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
```
- Aurora-style architecture: shared storage, up to 15 replicas (ms lag), failover via
  cluster endpoint, fast clones, PITR. **Elastic clusters** shard collections (`shardCollection`)
  for > one-writer throughput.
- Compatibility gaps that bite: `retryWrites` must be **false**; no `$lookup` across
  databases; limited `$expr`/aggregation operators by version; **no change streams on
  5.0 until enabled per collection** (`modifyChangeStreams`); no transactions across
  collections on 3.6; index builds are foreground-only (one at a time); `$text` absent
  (use OpenSearch); case-insensitive collation partial. Run the **compatibility scanner**
  (`amazon-documentdb-tools/compat-tool`) against your app's query log before migrating.
- Indexes: every query without an index is a collection scan; `explain()` shows
  `COLLSCAN`. Unlike MongoDB, DocumentDB does not auto-create `_id` + compound; create them.
- Connect with `readPreference=secondaryPreferred` to use replicas; TLS on by default.
- Migration from MongoDB: DMS (full load + CDC), `mongodump/mongorestore` (offline), or
  the DocumentDB migration tool for live cut-over.

## 3. Neptune
```bash
aws neptune create-db-cluster --db-cluster-identifier graph --engine neptune --engine-version 1.3.2.0 \
  --serverless-v2-scaling-configuration MinCapacity=1,MaxCapacity=32 --storage-encrypted --db-subnet-group-name private \
  --vpc-security-group-ids sg-neptune --enable-cloudwatch-logs-exports audit --deletion-protection
aws neptune create-db-instance --db-cluster-identifier graph --db-instance-identifier graph-1 --db-instance-class db.serverless --engine neptune
curl -X POST https://graph.cluster-xxxx.<REGION>.neptune.amazonaws.com:8182/gremlin -d '{"gremlin":"g.V().hasLabel(\"user\").limit(5)"}'
```
- Three query languages over one store (property graph via Gremlin/openCypher; RDF via
  SPARQL) — property graph data is not visible to SPARQL and vice versa.
- Access only inside the VPC over HTTPS/WebSocket on 8182; IAM auth (SigV4) optional
  but recommended; no public endpoint.
- **Bulk loader** (`POST /loader` with S3 source in CSV/N-Quads formats, IAM role on
  the cluster) is the only fast ingest — ~100k+ records/s; Gremlin `addV` one by one is
  100x slower. Batch writes in one traversal (`g.addV()...addV()...`).
- Query hygiene: anchor traversals on an indexed property (`has('id', …)`), avoid
  unbounded `repeat()`; `explain`/`profile` endpoints show which steps hit the index
  (Neptune indexes everything in 3 of 4 orderings; `OSGP` index is optional for
  predicate-first lookups — enable `neptune_lab_mode`/`OSGPIndex` only if needed).
- Neptune Analytics (separate service) for whole-graph algorithms (PageRank, community
  detection) and vector similarity; load from the Neptune DB or S3 in minutes.
- Neptune ML + SageMaker for link prediction / node classification.

## 4. Keyspaces (for Apache Cassandra)
```sql
CREATE KEYSPACE app WITH REPLICATION = {'class': 'SingleRegionStrategy'};
CREATE TABLE app.events (device_id text, ts timestamp, value double, PRIMARY KEY ((device_id), ts))
  WITH CLUSTERING ORDER BY (ts DESC) AND default_time_to_live = 7776000
  AND CUSTOM_PROPERTIES = {'capacity_mode': {'throughput_mode': 'PAY_PER_REQUEST'}, 'point_in_time_recovery': {'status': 'enabled'}};
```
- Serverless Cassandra: no nodes, compaction or repair; connect with any Cassandra 3.x
  driver using **SigV4 auth plugin** or service-specific credentials, TLS required
  (`sf-class2-root.crt`), `LOCAL_QUORUM` consistency for writes and `LOCAL_ONE`/`LOCAL_QUORUM` reads.
- Gaps: no `ALLOW FILTERING` on non-key columns beyond limits, no UDFs/UDAs/triggers,
  no materialized views, no lightweight transactions beyond `IF NOT EXISTS`, batches
  only unlogged and ≤ 30 statements, row size ≤ 1 MB, no counter columns; check the
  "supported CQL" page for each feature the app uses. DDL is asynchronous (poll `system_schema_mcs.tables`).
- Pricing mirrors DynamoDB (RRU/WRU on-demand or provisioned with auto scaling);
  multi-region keyspaces replicate at the keyspace level.
- Partition design is Cassandra's: bounded partitions (< 100 MB equivalent), time
  buckets in the partition key for append-only series.

## 5. Timestream
- **For LiveAnalytics**: tables with a **memory store** (recent, fast, hours-days
  retention) tiering to **magnetic store** (months-years); writes must land within the
  memory-store window (late data → `RejectedRecordsException` unless `MagneticStoreWriteProperties` enabled).
  Write via `WriteRecords` batched 100/request with `Dimensions`, `MeasureName`,
  `MeasureValue(s)`, `Time`; multi-measure records cut cost. Query with SQL + time
  functions (`bin(time, 5m)`, `interpolate_linear`, `derivative`); scheduled queries
  pre-aggregate into rollup tables. Cost is dominated by bytes scanned — always
  bound `WHERE time > ago(…)` and select specific measures.
- **For InfluxDB**: managed InfluxDB 2.x instance (Flux/InfluxQL, Telegraf, Grafana
  plugins work unchanged) — the pick for existing InfluxDB stacks and sub-second dashboards.
- Alternative many teams end up on: Prometheus/AMP for metrics, Aurora PostgreSQL
  for small series. Timestream wins at IoT scale with ad-hoc SQL.

## 6. QLDB (and what replaces it)
Ledger with an immutable, hash-chained journal, SQL-like PartiQL over Amazon Ion
documents, `history()` function and cryptographic verification (`GetDigest`, `GetRevision`).
**AWS announced end of support for QLDB in July 2024 (service ends 31 July 2025)**: no new ledgers, migrate existing
ones — the documented path is **Aurora PostgreSQL** with an append-only history table,
triggers, and application-level hashing/verification (AWS publishes a migration guide
and `qldb-export` tooling to export journal blocks to S3 → load into Postgres). Treat
"ledger" needs as: audit table with hash chaining in Aurora, or a blockchain only if
multi-party trust is the actual requirement (Managed Blockchain).

## 7. MemoryDB
Valkey/Redis-compatible with a **durable multi-AZ transaction log**: writes
acknowledged after replication to the log, so failover loses nothing — a primary
database for session/leaderboard/geo workloads rather than a cache. Cluster-mode
only, RBAC, snapshots; ~µs reads, single-digit ms writes. Costs more than ElastiCache
per node plus per-GB data written; pick it only when Redis *is* the system of record.

## Gotchas
- "Compatible" never means "identical": run the vendor compatibility tool and the app's
  test suite against the AWS engine before committing (DocumentDB, Keyspaces especially).
- All of these are VPC-only (except Keyspaces/Timestream public endpoints via IAM);
  Lambda needs VPC config or an interface endpoint.
- Storage-billed engines (DocumentDB, Neptune) never shrink storage automatically;
  deleted data frees space inside the volume for reuse but the high-water mark bills.
- Neptune and DocumentDB share Aurora's "a reader is not a backup" property.
- Timestream memory-store retention set too short rejects slightly-late IoT batches.
- Unconfirmed: exact QLDB end-of-support date and DocumentDB 8.0 feature list; confirm current announcements.

## Verify
- [ ] Workload fit documented: data model, top-5 queries, and which service's native API answers each in one call.
- [ ] Compatibility scan (DocumentDB compat-tool / Keyspaces supported-CQL review) shows zero unsupported operators used by the app.
- [ ] Failover drill (DocumentDB/Neptune `failover-db-cluster`, Keyspaces n/a) — app reconnects within 30 s.
- [ ] Cost model at 12-month projected volume computed in the service's own units (I/O, RRU/WRU, bytes scanned) and signed off.
- [ ] Exit path rehearsed: export (DMS / `mongodump` / `UNLOAD`-equivalent / Timestream `UNLOAD` to S3) of a sample succeeds.
