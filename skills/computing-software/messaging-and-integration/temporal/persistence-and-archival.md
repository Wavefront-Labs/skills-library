---
id: computing-software.messaging-and-integration.temporal.persistence-and-archival
name: persistence-and-archival
category: computing-software
field: messaging-and-integration
product: temporal
tags: [persistence, cassandra, postgresql, mysql, archival, history-archival, visibility-store, archiver]
level: advanced
status: docs-checked
description: "Temporal persistence stores and tested database versions, what is stored, and experimental Archival to blob storage with its archive delay."
sources:
  - https://docs.temporal.io/temporal-service/persistence
  - https://docs.temporal.io/temporal-service/archival
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Persistence is the only required dependency of the Temporal Service. It stores Tasks to dispatch; workflow state (an execution table with mutable state and an append-only history table); Namespace metadata; and Visibility data. Elasticsearch is recommended for Visibility in production; since Server 1.20 SQL stores can also serve advanced Visibility.

Tested versions: Cassandra 3.11, 4.0 and 5.0.4+ (earlier 5.x unsupported); PostgreSQL 13.18, 14.15, 15.10, 16.6; MySQL 5.7 and 8.0 (8.0.19+ because of a bug). Vitess and CockroachDB are not tested. SQLite 3.x is for development and testing only.

Archival copies closed workflows' Event Histories and Visibility records to blob storage, keeping data beyond retention without loading persistence. It is useful for compliance and debugging.

How it runs: at close, the Service schedules tasks for Visibility records and history archival. Archival happens asynchronously after a randomised delay of up to 5 minutes (`history.archivalProcessorArchiveDelay`), capped by the Namespace Retention Period. The execution stays in persistence until retention cleanup, so it can exist in both places for a while.

Status: experimental, outside the normal versioning and support policy; unsupported under Docker; disabled by default for manual installs and the Helm chart; enable it in the server config. Custom archivers can be written.

## Checked

2026-11-03. Confirmed against the Temporal documentation pages: temporal-service/persistence, temporal-service/archival (under https://docs.temporal.io/). Removed the development.yaml pointer for enabling Archival.

Method: documentation only; no commands were run.
