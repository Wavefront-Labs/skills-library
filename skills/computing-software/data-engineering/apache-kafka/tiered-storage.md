---
id: computing-software.data-engineering.apache-kafka.tiered-storage
name: tiered-storage
category: computing-software
field: data-engineering
product: apache-kafka
tags: [apache-kafka, kafka, kafka-operations, tiered-storage, remote-storage, kip-405, local-retention-ms, remote-log-manager, s3-tiering, long-retention]
level: advanced
status: docs-checked
description: "Use Kafka tiered storage (KIP-405, GA 3.9): broker remote storage plugin, per-topic remote.storage.enable and local.retention, costs, limits, and verifying segments upload."
sources:
  - https://kafka.apache.org/documentation/#tiered_storage
  - https://github.com/apache/kafka/blob/trunk/docs/operations/tiered-storage.md
  - https://github.com/apache/kafka/blob/trunk/docs/configuration/tiered-storage-configs.md
  - https://github.com/apache/kafka/blob/trunk/docs/operations/monitoring.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kafka tiered storage

**Goal:** keep weeks or months of topic history cheaply in object storage while brokers hold only recent segments on local disk.

## Model
Closed (rolled) log segments are copied to a remote store; local copies are deleted after `local.retention.ms`/`local.retention.bytes`. Total retention is still `retention.ms`/`retention.bytes`. Consumers reading old offsets fetch from remote transparently (slower first byte).

Kafka ships the framework and a default internal-topic-based `RemoteLogMetadataManager`, but no out-of-the-box `RemoteStorageManager`: you must supply an implementation for your object store via `remote.log.storage.manager.class.name` and `.class.path`. For a local preview the docs use the test-fixture `LocalTieredStorage`.

## Broker config
```properties
remote.log.storage.system.enable=true
remote.log.storage.manager.class.name=<plugin RemoteStorageManager class>
remote.log.storage.manager.class.path=/opt/kafka/plugins/tiered-storage/*
remote.log.metadata.manager.listener.name=INTERNAL        # mandatory with the default topic-based metadata manager
rlmm.config.remote.log.metadata.topic.replication.factor=3   # default 3; use 1 on a single-broker test cluster
# the default RemoteLogMetadataManager is topic based; plugin-specific settings use the rsm.config. prefix
```

## Topic config
```bash
kafka-configs.sh --bootstrap-server $B --alter --entity-type topics --entity-name events.v1 \
  --add-config remote.storage.enable=true,local.retention.ms=86400000,retention.ms=7776000000
```
1 day local, 90 days total. If `local.retention.*` is unset, `retention.*` applies locally. A local segment is deleted only after it has been uploaded.

## Limits and gotchas (check your version's notes)
- No support for **compacted topics**.
- Segments created before Kafka 2.8.0 may lack a producer snapshot file and are not supported; admin actions for tiering need clients from 3.0 onward.
- To disable at broker level you must first disable or delete every tiered topic; otherwise the broker fails at startup.
- Topic-level disablement (KRaft): `remote.storage.enable=true,remote.log.copy.disable=true` makes remote logs read-only (also set `local.retention.ms` and `local.retention.bytes` to the retention values or `-2`, because local retention no longer applies); `remote.storage.enable=false,remote.log.delete.on.disable=true` deletes the remote logs.
- Only non-active (rolled) segments upload, as soon as eligible by default; `remote.copy.lag.ms` and `remote.copy.lag.bytes` (broker: `log.remote.copy.lag.ms`, `log.remote.copy.lag.bytes`) delay upload to reduce redundancy between tiers.
- Remote-tier thread pools are dynamic broker configs (`remote.log.reader.threads`, `remote.log.manager.copier.thread.pool.size`, `remote.log.manager.expiration.thread.pool.size`, `remote.log.manager.follower.thread.pool.size`).

## Monitoring
`kafka.server:type=BrokerTopicMetrics` metrics `RemoteCopyBytesPerSec`, `RemoteFetchBytesPerSec`, `RemoteCopyErrorsPerSec`, `RemoteFetchErrorsPerSec`, `RemoteCopyLagBytes` and `RemoteCopyLagSegments` (per topic with `topic=`, or all-topic when omitted). Alert on copy lag growing (local disks will fill).

## Verify
- [ ] Objects appear in the remote store for the topic after a segment rolls.
- [ ] Local disk usage for the topic stays near `local.retention` while a consumer reading from the earliest offset still fetches the old data.

## Checked

2026-10-25, against Apache Kafka trunk documentation (apache/kafka docs/, commit date 2026-10-24). Confirmed: `remote.log.storage.system.enable`, `remote.log.storage.manager.class.name` and `.class.path`, no built-in RemoteStorageManager, default topic-based RemoteLogMetadataManager with mandatory `remote.log.metadata.manager.listener.name`, `rlmm.config.` prefix and its replication-factor and min.isr settings, topic configs `remote.storage.enable`, `local.retention.ms/bytes`, the documented limitations, topic-level disable options, delayed-upload settings, and the remote metric names. Fixed: the 3.6 to 3.9 disablement history is replaced with the current documented procedure. Removed: named vendor and cloud implementations, the 90-day arithmetic claim beyond the example, `kafka-get-offsets.sh --time -2` and the segment-cost remarks.

Method: documentation only; no commands were run.
