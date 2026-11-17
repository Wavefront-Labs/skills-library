---
id: computing-software.messaging-and-integration.apache-kafka.kafka-tiered-storage-setup
name: kafka-tiered-storage-setup
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, tiered-storage, remote-log-storage-system-enable, remote-storage-enable, local-retention-ms]
level: advanced
status: docs-checked
description: "Enable tiered storage on brokers and topics: remote.log.storage.system.enable, RemoteStorageManager class, remote.storage.enable and local retention."
sources:
  - https://kafka.apache.org/42/operations/tiered-storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep recent log segments on local disks and move completed segments to remote storage such as HDFS or S3 (KIP-405).

Broker configuration:
- `remote.log.storage.system.enable=true` (off by default).
- `remote.log.storage.manager.class.name` and `remote.log.storage.manager.class.path` select the RemoteStorageManager. Kafka ships no production implementation; you must supply one.
- RemoteLogMetadataManager defaults to an internal-topic implementation; override with `remote.log.metadata.manager.class.name` and `.class.path`. For the default, `remote.log.metadata.manager.listener.name` is mandatory.

Topic configuration: `remote.storage.enable=true` (default false). Then set retention:
- `local.retention.ms` / `local.retention.bytes`: how long or large the local log can be before moving to remote and being deleted; if unset, `retention.ms` and `retention.bytes` apply.
- `retention.ms` / `retention.bytes`: total retention including remote.

A local segment is deleted only after it has been uploaded to remote.

Preview: the test class LocalTieredStorage (build with `./gradlew clean :storage:testJar`) simulates remote storage in a local directory, with a multi-broker cluster needing a higher `rlmm.config.remote.log.metadata.topic.replication.factor`.

Limitations: no compacted topics; clients must be 3.0 or newer for admin actions; log segments without a producer snapshot file (topics created before v2.8.0) are unsupported.

## Checked

Method: 2026-11-08 docs-only read of the cited Kafka 4.2 tiered-storage page. All claims matched; no content changes. No hands-on run (the LocalTieredStorage preview was not built).
