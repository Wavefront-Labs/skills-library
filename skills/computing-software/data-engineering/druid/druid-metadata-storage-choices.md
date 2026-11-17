---
id: computing-software.data-engineering.druid.druid-metadata-storage-choices
name: druid-metadata-storage-choices
category: computing-software
field: data-engineering
product: druid
tags: [metadata-storage, derby, mysql, postgresql, acid, high-availability]
level: practitioner
status: docs-checked
description: "Pick a production Druid metadata store, set Derby or DBCP properties, and know the metadata tables and which processes access them."
sources:
  - https://github.com/apache/druid/blob/master/docs/design/metadata-storage.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Druid uses an external metadata store for system metadata (not the data itself). It holds segment records, rule records, configuration records, task-related tables and audit records.

## Choosing a store

- Supported: Derby, MySQL, PostgreSQL. Derby is the default but not suitable for production; use MySQL or PostgreSQL via their metadata-storage extensions.
- The store must be ACID-compliant, or you can see problems such as tasks failing sporadically.
- To avoid trouble when an upgrade changes the schema of a large metadata table, prefer a store version with instant ADD COLUMN semantics (see the database-specific docs).
- Set up high availability: lost metadata cannot be restored.

## Derby (evaluation only)

```properties
druid.metadata.storage.type=derby
druid.metadata.storage.connector.connectURI=jdbc:derby://localhost:1527/<derby-dir>;create=true
```
`<derby-dir>` is a placeholder for the state directory.

## Custom DBCP properties

Prefix connection-pool properties with `druid.metadata.storage.connector.dbcp.` (for example `maxConnLifetimeMillis` or `defaultQueryTimeout`; the numbers on the page are examples). These five cannot be set through the dbcp prefix and use `druid.metadata.storage.connector.` instead: `username`, `password`, `connectURI`, `validationQuery`, `testOnBorrow`. The full list is the Apache Commons DBCP BasicDataSource configuration.

## Tables

- Segments (`druid.metadata.storage.tables.segments`): segments that should be available; polled by the Coordinator. Column `used` is 1 when a segment should be loaded and 0 when it should not (unloaded without deleting metadata, which eases rollback). `used_status_last_updated` records when `used` last changed and lets the Coordinator judge kill eligibility. `payload` is a JSON blob with all segment metadata, intentionally duplicating some columns.
- Rules: where segments should land; used by the Coordinator.
- Config: runtime configuration objects; the page says the mechanism may not be kept.
- Task-related tables: created and used by the Overlord and Middle Manager.
- Audit: history of configuration changes such as rule changes.

## Access

Only indexing service processes (if any), realtime processes (if any) and Coordinator processes access the metadata store, so grant network access (for example cloud security groups) to just those machines.

## Checked

2026-11-08. Read the cited metadata-storage page in full. Expanded the draft with the table descriptions, DBCP prefix rules and access guidance; replaced the sample Derby state path with a placeholder.

Method: documentation only; no commands were run.
