---
id: computing-software.messaging-and-integration.apache-kafka.kafka-tiered-storage-disable
name: kafka-tiered-storage-disable
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, tiered-storage, remote-log-copy-disable, remote-log-delete-on-disable]
level: advanced
status: docs-checked
description: "Disable tiered storage per topic, keeping remote logs read-only or deleting them, and disable it at the broker safely."
sources:
  - https://kafka.apache.org/42/operations/tiered-storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: turn tiered storage off without surprises. This works in KRaft mode.

Make remote logs read-only (no more copying local segments to remote):
```
bin/kafka-configs.sh --bootstrap-server localhost:9092 --alter --entity-type topics --entity-name tieredTopic \
  --add-config 'remote.storage.enable=true,remote.log.copy.disable=true,local.retention.ms=-2,local.retention.bytes=-2'
```
Also set `local.retention.ms` and `local.retention.bytes` to the same values as `retention.ms` and `retention.bytes`, or to -2. After copying is disabled the local retention policies no longer apply, which could cause an unexpected full disk.

Disable completely and delete all remote logs:
```
bin/kafka-configs.sh --bootstrap-server localhost:9092 --alter --entity-type topics --entity-name tieredTopic \
  --add-config 'remote.storage.enable=false,remote.log.delete.on.disable=true'
```
You can re-enable the feature at topic level later.

Cluster level: you must first disable tiered storage on every topic that uses it, for example by deleting the topics with `kafka-topics.sh --delete`. Attempting to set `remote.log.storage.system.enable=false` while tiered topics exist causes an exception at startup. After the topics are gone, the broker setting can be switched off.

## Checked

2026-11-04: claims, commands, flags and config names confirmed against the Kafka 4.2 Tiered Storage page (Disable Tiered Storage). Removed: closing 'order of operations' paragraph (restatement not on the page).

Method: documentation only; no commands were run.
