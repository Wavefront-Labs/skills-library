---
id: computing-software.data-engineering.druid.druid-metadata-store-migration
name: druid-metadata-store-migration
category: computing-software
field: data-engineering
product: druid
tags: [metadata-migration, export-metadata, derby, mysql, postgresql]
level: advanced
status: docs-checked
description: "Migrate metadata from Derby to MySQL or PostgreSQL, or between production stores."
sources:
  - https://github.com/apache/druid/blob/master/docs/operations/metadata-migration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use this to move off the built-in Derby store, or between production stores such as PostgreSQL to MySQL.

Steps:
1. Shut down the non-coordinator services so metadata does not change during migration. When migrating from Derby the Coordinators must stay up at first because they host the Derby database.
2. Export metadata with the Export Metadata Tool, which exports from Derby or PostgreSQL into CSV files. Run `export-metadata` on the existing cluster and save the CSV files. The tool can also rewrite segment deep storage locations, useful for deep storage migration. After a successful export you can shut down the Coordinator.
3. Create the new database; the MySQL and PostgreSQL extension docs cover initial setup. Then update the Druid runtime properties with the new metadata configuration.
4. Create the Druid tables. If `druid.metadata.storage.connector.createTables` is `true` (the default) and the connect user has DDL privileges, Druid creates them at startup and you can skip this. Otherwise run the `metadata-init` tool from the Druid package root with `org.apache.druid.cli.Main tools metadata-init`, passing `--connectURI`, `--user`, `--password` and `--base` (the value of `druid.metadata.storage.tables.base`, `druid` by default), with the matching `mysql-metadata-storage` or `postgresql-metadata-storage` extension in `druid.extensions.loadList` and `druid.metadata.storage.type` set. The tool does not read cluster runtime properties, so pass any property that affects the tables: the `druid_segmentSchemas` table and the `schema_fingerprint` and `num_rows` columns of `druid_segments` are only created with `-Ddruid.centralizedDatasourceSchema.enabled=true`, which you should pass if the cluster uses centralized datasource schema or the source store already has them. Re-running the same command later updates tables to the latest compatible schema, running any needed ALTER statements.
5. Import the exported CSV files using the import commands for your target database in the Export Metadata Tool docs.
6. Restart the cluster.

## Checked

2026-11-08. Read operations/metadata-migration.md in full. Replaced the vague import step with the documented table creation, metadata-init parameters and ordering.

Method: documentation only; no commands were run.
