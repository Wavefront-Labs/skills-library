---
id: computing-software.messaging-and-integration.debezium.mongodb-offset-consolidation-after-upgrade
name: mongodb-offset-consolidation-after-upgrade
category: computing-software
field: messaging-and-integration
product: debezium
tags: [mongodb, upgrade, offsets, sharded-cluster]
level: sme
status: docs-checked
description: "Understand how the MongoDB connector consolidates old replica_set offsets into sharded-mode offsets after an upgrade."
sources:
  - https://debezium.io/documentation/reference/stable/connectors/mongodb.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The connector no longer supports `replica_set` connections to sharded MongoDB deployments, so offsets recorded by older versions in that mode are incompatible. To avoid unnecessary snapshots, on restart after upgrade it runs an offset consolidation procedure:

- Offsets recorded by versions later than 2.5 are used as-is.
- Offsets from sharded connection mode on sharded deployments, or from replica set deployments, are used as-is.
- Shard-specific offsets from 2.5.x and earlier are used as-is only if both conditions hold: offsets exist for every current shard, and offset invalidation is enabled (`internal.mongodb.allow.offset.invalidation`, default `false`). If offset invalidation is disabled, the connector fails to start.
- After processing existing offsets, it resumes streaming and commits new offsets.
- If no existing offsets are found, it performs an initial snapshot.

Requirements: the connector user must be able to read the `config.shards` collection when the connector was upgraded from 2.5 or earlier, or when it captures from a sharded cluster (see mongodb-required-user-permissions).

Related: `topic.prefix` is the logical name of the replica set or sharded cluster and the unique identifier used when recording the change stream position of each replica set.

Procedure for upgrades:

1. Grant `config.shards` read access before upgrading.
2. Check that all current shards have offsets.
3. Keep the same `topic.prefix`.

## Checked

2026-11-08: read the Offset consolidation, Logical connector name and connector user permissions sections and the internal.mongodb.allow.offset.invalidation property row of the Debezium MongoDB connector reference (raw AsciiDoc source of the cited page, connectors/mongodb.adoc). Confirmed the consolidation steps, the config.shards permission requirement and the property default. Removed: the claim that renaming topic.prefix triggers a snapshot, the shard-change gotcha and the log Check line, none of which the page states.

Method: documentation only; no commands were run.
