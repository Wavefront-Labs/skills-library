---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.time-series-database
name: time-series-database
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, database-selection, time-series-database, timestream, influxdb, timescaledb, specialised-data-stores]
level: practitioner
status: docs-checked
description: "Choose a time-series store: Timestream, TimescaleDB, Azure Data Explorer or Bigtable, and design Bigtable time-series rows with time buckets and no timestamp-leading keys."
sources: ["https://docs.aws.amazon.com/timestream/latest/developerguide/what-is-timestream.html", "https://docs.timescale.com/", "https://docs.influxdata.com/", "https://learn.microsoft.com/azure/data-explorer/data-explorer-overview", "https://cloud.google.com/bigtable/docs/schema-design-time-series"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Time-series data stores

## Fit
Azure's data store guide describes time-series stores as typically append-only, optimised for
high-volume near-real-time ingestion, time-window queries and aggregations, and out-of-order ingestion.
Workloads: IoT sensor metrics, application telemetry, monitoring, industrial data, financial market data.
Considerations it names: tag cardinality management, retention cost, downsampling strategy and
specialised query languages. Evaluate ingestion performance, ad hoc queries, indexes beyond
date/time, and time-series analytics and alerts.

## Options as documented
- **Amazon Timestream for LiveAnalytics**: serverless, memory store for recent data and magnetic
  store for history, with user-configurable policies moving data between them; SQL with built-in
  smoothing, approximation and interpolation functions. The page points to Timestream for InfluxDB
  for similar capabilities and carries an availability-change notice, so check current availability
  before choosing it for a new workload.
- **TimescaleDB**: a PostgreSQL extension (not a separate fork) adding hypertables (automatic
  time-based partitioning), continuous aggregates (incrementally materialised views), columnar
  compression and retention policies. Azure notes Azure Database for PostgreSQL supports it, a fit
  when time-series data is queried alongside transactional data.
- **Azure Data Explorer**: managed big data platform queried with KQL (it also supports T-SQL);
  Azure also names Eventhouse in Fabric for a SaaS experience.
- **InfluxDB**: see the vendor documentation (the cited landing page was not used for specific claims).
- **Bigtable**: schema design patterns below.

## Bigtable row-key design (Google)
1. Time bucket pattern: each row holds a period (hour, day, week) for an entity and metric; the
   bucket size depends on queries and on the recommended maximum row size of 100 MB. Better read and
   write performance and compression than tall narrow tables, at the cost of design effort.
2. Single-timestamp rows put the timestamp at the end of the key; Google states "never use a
   timestamp value as a row key prefix" to avoid hotspots. The unserialised variant can still hotspot.
3. When adding new cells per event, set garbage collection rules; microsecond timestamp granularity
   to avoid collisions is available only on Enterprise Plus instances.
4. For several query shapes on one dataset, consider multiple tables with different row keys.

## Gotchas
- Timestamp-leading row keys hotspot a single node.
- Azure's guidance for a column-family store with slow time-window queries: adopt a purpose-built
  time-series database.

## Verify
- [ ] Cardinality estimate within the chosen store's documented limits.
- [ ] Retention and downsampling policies configured.

## Checked
Method: docs-only read of cited pages, 2026-11-08

Confirmed on the Timestream, Timescale (Tiger Data), Azure Data Explorer and Bigtable pages and the Azure
data store overview. Removed as not stated on the cited pages: the tags-versus-fields cardinality rule,
rollup intervals, QLDB deprecation, Neptune/Gremlin/Neo4j/Keyspaces ledger and graph guidance, and
Prometheus-compatible stores. The InfluxDB landing page was fetched but supports no specific claim.
