---
id: computing-software.data-engineering.etl-pipeline-design.handling-source-ddl-in-cdc
name: handling-source-ddl-in-cdc
category: computing-software
field: data-engineering
product: etl-pipeline-design
tags: [etl-pipeline-design, cdc, cdc-schema-changes, ddl, debezium, schema-history, schema-evolution, column-rename]
level: advanced
status: docs-checked
description: "Keep CDC pipelines alive through source schema changes: how Debezium treats added, renamed, retyped and dropped columns, registry compatibility and warehouse propagation."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-schema-changes
  - https://debezium.io/documentation/reference/stable/connectors/mysql.html#mysql-schema-history-topic
  - https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Handling source DDL in CDC pipelines

**Goal:** an `ALTER TABLE` in the application database does not silently drop data, break consumers, or stall the pipeline.

## What happens per change type (Debezium)
| Source change | CDC events | Downstream risk |
|---|---|---|
| Add nullable column | new field appears in events after the DDL | Avro BACKWARD compatible if default null; warehouse needs column added |
| Add NOT NULL column with default | field appears | same; existing rows lack it until updated |
| Drop column | field disappears | BACKWARD compatible only if field had a default; downstream models referencing it break |
| Rename column | looks like drop + add | history split across two columns |
| Type change (int -> bigint) | new schema version | check the registry's compatibility rules for the format; a type change can be incompatible |
| Rename table | events are produced for the new table name | consumers of the old table's topic must be repointed |

MySQL: the connector reads the binlog, which records schema changes as well as data changes, and keeps an internal **database schema history topic** for its own use (consumers should read schema-change events from the separate schema change topic instead); do not delete or edit the history topic. Postgres: logical decoding does not support DDL changes, so the connector cannot report DDL change events to consumers; the new shape only shows up in the events after the change.

## Schema registry settings
- Confluent's default and preferred mode for Kafka is BACKWARD (consumers using the new schema read old data: add optional fields, remove fields); FULL allows only adding or removing optional fields. Deleting a field while staying backward compatible requires it to have been optional or to have a default. This is why optional fields with defaults matter for nullable source columns.
- An incompatible change -> the producer fails to register the new schema, and the connector fails. Decide: temporarily relax compatibility for that subject, or route to a new topic version.

## Warehouse propagation
- Check each sink or managed EL tool's behaviour for added, renamed, retyped and dropped columns before relying on it; many add columns automatically but handle renames and type changes differently (new column, resync or failure).
- dbt staging models with explicit column lists isolate marts from upstream renames; check your dbt version's `on_schema_change` options for incremental models.
- Lakehouse formats have their own schema-evolution switches for additive changes; type changes need explicit handling.

## Process (the real fix)
1. **Change contract with the app team:** DDL in their repo triggers a review by data owners (CODEOWNERS on migrations folder) or a data contract check.
2. Prefer additive changes; rename via expand-contract (add new, dual-write, backfill, drop old later).
3. Announce drops/renames with a deprecation window.
4. Test: run the migration against a staging DB with the CDC pipeline attached.

## Gotchas
- Debezium snapshot behaviour is set by `snapshot.mode` (default `initial` on the MySQL connector). For a corrupted or lost MySQL schema history, look up the schema recovery snapshot modes for your Debezium version rather than recreating the topic by hand.
- Postgres `REPLICA IDENTITY` determines what the connector can put in the `before` field of update and delete events, so check it when changing it.
- Column order changes are harmless for name-based formats, harmful for CSV/positional sinks.

## Verify
- [ ] Staging drill: add/drop/rename columns; connector stays RUNNING and warehouse columns follow policy.
- [ ] Alert on connector task failure and schema registry incompatibility errors.

## Checked
Date: 2026-11-09. Confirmed from the Debezium PostgreSQL page (logical decoding does not support DDL changes, REPLICA IDENTITY and before images, column.propagate.source.type), the Debezium MySQL page (binlog records schema changes, internal schema history topic vs schema change topic, snapshot.mode default initial) and the Confluent schema evolution page (BACKWARD/FORWARD/FULL definitions, BACKWARD default for Kafka, delete requires optional or default). The per-change table rows are design guidance built on those rules. Removed: auto.evolve claims, the x_v2 naming, dbt on_schema_change value, Delta mergeSchema and Auto Loader names, snapshot.mode recovery values, the Avro widening claim, and the new-topic claim for table renames. Not read: Debezium sink or JDBC connector docs.
Method: documentation only; no commands were run.
