---
id: computing-software.cloud-infrastructure-engineering.google-cloud.datastream-cdc-into-bigquery
name: datastream-cdc-into-bigquery
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, datastream, datastream-cdc, change-data-capture, bigquery, mysql-binlog, postgresql-logical-replication, oracle-logminer]
level: practitioner
status: docs-checked
description: "Replicate MySQL, PostgreSQL, Oracle or SQL Server changes into BigQuery with Datastream: source prep, private connectivity, stream config, backfill, staleness and failures."
sources: ["https://cloud.google.com/datastream/docs/overview", "https://cloud.google.com/datastream/docs/configure-your-source-postgresql-database", "https://cloud.google.com/datastream/docs/destination-bigquery"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Datastream CDC into BigQuery

## Source preparation
Datastream supports sources including MySQL, Oracle, PostgreSQL, AlloyDB for PostgreSQL, SQL Server, MongoDB and Spanner. Follow the source-specific configuration page for each database.
- **PostgreSQL**: Datastream uses logical decoding to read WAL changes through a **publication** and a **replication slot** that you create on the source; see "Configure a source PostgreSQL database".

## Connectivity
Private connectivity configurations let Datastream reach a source over a private network (within Google Cloud, or external sources connected over VPN or Interconnect).
```bash
gcloud datastream private-connections create ds-pc --location=<R> --display-name=ds-pc \
  --vpc=projects/<P>/global/networks/prod --subnet=10.50.0.0/29
```

## Stream
Create connection profiles (source + BigQuery), then the stream with the objects to include, a backfill choice, and the BigQuery destination settings described on the BigQuery destination page.
```bash
gcloud datastream streams create orders-cdc --location=<R> --display-name=orders-cdc \
  --source=pg-src --postgresql-source-config=src.json \
  --destination=bq-dst --bigquery-destination-config=dst.json --backfill-all
```

## Operations
- Tables without a primary key at the source are append-only in BigQuery; tables with one carry the documented metadata columns, and tables without one add an `IS_DELETED` field.

## Verify
- [ ] An insert and an update on the source appear in BigQuery.

## Checked

2026-10-27. Confirmed in the Datastream overview, PostgreSQL source and BigQuery destination pages and the `gcloud datastream private-connections create` and `streams create` reference pages: supported sources, publication and replication slot for PostgreSQL, private connectivity over VPN or Interconnect, `--vpc`/`--subnet`/`--display-name`/`--location` on private-connections create, `--backfill-all`, `--postgresql-source-config` and `--bigquery-destination-config` on streams create, append-only behaviour and `IS_DELETED` for tables without primary keys. Removed: MySQL and Oracle source settings (no page fetched), PostgreSQL `wal_level`, flag and SQL snippets, the freshness metric name, the max_staleness and merge-mode description, schema-change claims, the WAL-retention and replica gotchas. Read end to end.

Method: documentation only; no commands were run.
