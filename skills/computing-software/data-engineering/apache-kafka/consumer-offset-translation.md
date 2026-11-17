---
id: computing-software.data-engineering.apache-kafka.consumer-offset-translation
name: consumer-offset-translation
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, geo-replication, offset-translation, mirrorcheckpointconnector, checkpoints-topic, remoteclusterutils, sync-group-offsets, offset-syncs, failover]
level: sme
status: docs-checked
description: "Fail consumers over between replicated Kafka clusters: MM2 checkpoints and offset-syncs, sync.group.offsets, RemoteClusterUtils, and translation precision limits."
sources:
  - https://kafka.apache.org/40/configuration/mirrormaker-configs/
  - https://cwiki.apache.org/confluence/display/KAFKA/KIP-382%3A+MirrorMaker+2.0
  - https://cwiki.apache.org/confluence/display/KAFKA/KIP-545%3A+support+automated+consumer+offset+sync+across+clusters+in+MM+2.0
  - https://issues.apache.org/jira/browse/KAFKA-14666
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consumer offset translation across clusters

**Goal:** when a consumer group fails over to the replica cluster, it resumes near where it left off instead of from the beginning or the end.

## Why translation is needed
Offset 1,000,000 on primary partition 3 is not offset 1,000,000 on the replica: retention, compaction and transaction markers shift offsets. MM2 records the correspondence.

## Mechanism
1. `MirrorSourceConnector` periodically writes **offset-syncs** (source offset <-> target offset pairs) to an internal offset-syncs topic (`offset-syncs.topic.location`: `source` by default, or `target`).
2. `MirrorCheckpointConnector` reads source consumer group offsets for groups matching `groups` (default `.*`, with `groups.exclude` defaulting to `console-consumer-.*,connect-.*,__.*`), translates them with the syncs, and writes **checkpoints** to a topic like `<source-alias>.checkpoints.internal` on the target (KIP-382).
3. With `sync.group.offsets.enabled=true` (default false; together with `emit.checkpoints.enabled`, KIP-545), it also writes translated offsets into the target's `__consumer_offsets`, **only as long as no active consumers of that group are connected to the target**. Interval: `sync.group.offsets.interval.seconds` (default 60).

## Failover procedure
1. Stop consumers on primary (or primary is down).
2. Confirm the group's committed offsets on DR: `kafka-consumer-groups.sh --bootstrap-server $DR --describe --group billing-projector`.
3. If not auto-synced, translate with the `RemoteClusterUtils` / `MirrorClient` classes from the MM2 client library (KIP-382: they translate consumer offsets between clusters), then apply the translated offsets to the DR group while it is inactive (for example `kafka-consumer-groups.sh --reset-offsets --from-file`).
4. Start consumers on DR (subscribed to the remote topic names when using the default replication policy, e.g. `<source-alias>.<topic>`).

## Expect some reprocessing
- Translation is only as fresh as the last checkpoint (`emit.checkpoints.interval.seconds`, default 60) plus offset-sync frequency.
- KAFKA-14666 (fixed in 3.3.3, 3.4.1 and 3.5.0) makes MM2 translate offsets for groups that are behind the replication flow on a best-effort basis; before it, such offsets were not translated. `offset.lag.max` (default 100) controls how far a remote partition can be out of sync before a new offset-sync is written: a trade-off between sync volume and precision.
- Therefore consumers must be idempotent.

## Failback
Reverse replication (dr->primary) needs its own MM2 flow and translation.

## Verify
- [ ] In a DR drill, the group resumes on DR with lag roughly equal to (replication lag + checkpoint interval), not full topic size.
- [ ] Downstream dedup/idempotency absorbs the reprocessed window (no duplicate effects).
- [ ] Checkpoint topic receives entries for every replicated group.

## Checked
2026-10-28. Confirmed in the Kafka 4.0 MirrorMaker configuration page, KIP-382, KIP-545 and KAFKA-14666: defaults for `offset-syncs.topic.location` (source), `offset.lag.max` (100), `emit.checkpoints.interval.seconds` (60), `sync.group.offsets.enabled` (false), `sync.group.offsets.interval.seconds` (60), `groups` and `groups.exclude`; checkpoints topic naming; `RemoteClusterUtils` / `MirrorClient`; KAFKA-14666 fix versions. Removed: the exact offset-syncs topic name, the 2.7 and 3.5 version gates, the code sample (method signatures not confirmed), the never-skip guarantee and the `IdentityReplicationPolicy` remark.
Method: documentation only; no commands were run.
