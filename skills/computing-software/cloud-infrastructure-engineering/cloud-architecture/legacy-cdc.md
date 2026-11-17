---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.legacy-cdc
name: legacy-cdc
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, modernisation, legacy-cdc, change-data-capture, debezium, log-based-cdc, aws-dms-cdc, data-liberation]
level: advanced
status: draft
description: "Use log-based change data capture (Debezium, DMS, Datastream) to stream changes out of a legacy database so new services can be built without touching the legacy code."
sources: ["https://debezium.io/documentation/reference/stable/architecture.html", "https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Task.CDC.html", "https://cloud.google.com/datastream/docs/overview"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Change data capture to liberate legacy data

## Why
The legacy system stays the system of record while new services, search indexes, caches and the
analytics platform consume a stream of its changes, without dual writes or legacy code changes.

## Options
| Tool | Mechanism |
|---|---|
| Debezium (Kafka Connect / Server) | Reads MySQL binlog, Postgres logical replication, SQL Server CDC tables, Oracle LogMiner |
| AWS DMS (full load + CDC) | Managed replication instances/serverless; targets Kinesis, Kafka, S3, databases |
| Google Datastream | Serverless CDC from MySQL/Postgres/Oracle/SQL Server to BigQuery/GCS |
| Azure: SQL CDC + Event Hubs/Debezium, Fabric mirroring | |

## Steps
1. Enable source prerequisites: MySQL `binlog_format=ROW`, `binlog_row_image=FULL`; Postgres
   `wal_level=logical` and a replication slot; SQL Server CDC on tables; adequate log retention.
2. Initial snapshot, then streaming; tables with primary keys only (or define keys).
3. Event design: raw row-change events are internal; publish domain events via a translation
   layer (anti-corruption layer) for consumers outside the team.
4. Schema changes: schema registry with compatibility rules; test DDL handling.
5. Consumers must be idempotent and handle ordering per key (partition by primary key).
6. Monitor lag, slot growth, connector health.

## Gotchas
- Postgres replication slots that stop being consumed retain WAL until the disk fills.
- Large transactions and LOB columns slow or break CDC.
- Leaking legacy table structure to many consumers recreates coupling.

## Verify
- [ ] End-to-end lag within target under peak write load.
- [ ] Connector restart resumes without data loss or unbounded duplicates.
