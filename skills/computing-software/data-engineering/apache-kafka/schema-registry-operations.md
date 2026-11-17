---
id: computing-software.data-engineering.apache-kafka.schema-registry-operations
name: schema-registry-operations
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, schema-registry, schema-registry-migration, schemas-topic, import-mode, readonly-mode, backup, disaster-recovery]
level: advanced
status: docs-checked
description: "Operate Confluent Schema Registry: the _schemas topic, primary election, READONLY/IMPORT modes, backups, and migrating schemas to a new registry while keeping ids."
sources:
  - https://docs.confluent.io/platform/current/schema-registry/installation/deployment.html
  - https://docs.confluent.io/platform/current/schema-registry/installation/migrate.html
  - https://docs.confluent.io/platform/current/schema-registry/develop/api.html#mode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Schema Registry operations

## How it stores state
All schemas, configs and modes live in a compacted Kafka topic, `_schemas` by default (`kafkastore.topic`). Instances read it into memory at startup. One instance is the **primary** (elected through the Kafka group protocol, `schema.registry.group.id`); writes to secondaries are forwarded to it.
- `_schemas`: a single-partition, durable, compacted topic; the deployment page creates it with `--replication-factor 3 --partitions 1 --config cleanup.policy=compact`. It must be compacted so retention does not lose data.
- `leader.eligibility=false` keeps nodes from being elected primary (the deployment page uses it for nodes in a secondary datacenter).

## Backups
- The `_schemas` topic is the source of truth for the registry, so back it up or mirror it to the DR cluster like any other critical topic.

## Modes
```bash
curl -X PUT -H "Content-Type: application/json" --data '{"mode":"READONLY"}' $SR/mode          # global
curl -X PUT -H "Content-Type: application/json" --data '{"mode":"IMPORT"}' $SR/mode/orders-value   # per subject
```
- Modes are `READWRITE` (default), `READONLY`, `IMPORT` and `FORWARD`. `IMPORT` allows registering a schema **with a given id and version**, required to migrate while preserving ids. Subject-level IMPORT requires the subject to be empty or nonexistent; `?force=true` forces a mode change when the registry already has schemas (the API reference describes it for disaster recovery with Schema Linking).

## Migrating to a new registry (keep ids)
Ids are embedded in every serialized record, so the target must reuse the same ids.
1. Set the source to READONLY (freeze), target to IMPORT.
2. For each subject/version: `POST /subjects/<s>/versions` with body `{"schemaType":..., "version":..., "id":..., "schema":...}` (the migration page's example for a subject-level migration).
3. Copy compatibility configs (see the API reference).
4. Switch target to READWRITE, point clients at it, retire the source.
On Confluent Platform 7.0.0 and later, Schema Linking migrates schemas; the migration page also covers Replicator-based migration.

## Upgrades and incidents
- Rolling restart instances one at a time.
- Never recreate `_schemas` in place: it is the registry's source of truth.

## Checked
2026-10-28. Confirmed on the Confluent Schema Registry deployment, migration and API pages: `_schemas` topic spec (1 partition, RF 3, compact), `leader.eligibility`, modes IMPORT/READONLY/READWRITE/FORWARD, IMPORT needing an empty or nonexistent subject, `?force=true`, POST with `id` and `version`, Schema Linking on Platform 7.0.0 and later. Removed: backup console-consumer command, REST export, `schema-exporter`, `/v1/metadata/id`, outage-behaviour claims.
Method: documentation only; no commands were run.

## Verify
- [ ] Restore drill: a new registry populated from backup returns the same schemas for sampled ids.
