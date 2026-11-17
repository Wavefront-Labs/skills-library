---
id: computing-software.messaging-and-integration.apache-kafka.kafka-log-compaction
name: kafka-log-compaction
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, log-compaction, cleanup-policy, tombstone, delete-retention-ms]
level: practitioner
status: docs-checked
description: "Keep the latest value per key with log compaction, tombstones, delete.retention.ms and min/max compaction lag."
sources:
  - https://kafka.apache.org/42/design/design/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: retain at least the last record for every key in a partition, for state restore, cache reload or change-data topics.

Compaction removes older records that have a newer record with the same key. A record with a key and a null payload is a tombstone (delete marker): it removes prior records for that key and is itself cleaned after a while.

Guarantees:
- A consumer that stays caught up to the head of the log sees every message, with sequential offsets.
- Ordering is never changed, and offsets never change; a compacted-away offset is equivalent to the next higher one.
- A consumer reading from the start sees at least the final state of each key.
- Tombstones are seen only if the consumer reaches the head within `delete.retention.ms` (default 24 hours).

Controls:
- `min.compaction.lag.ms` is the minimum time a message stays uncompacted.
- `max.compaction.lag.ms` is the maximum delay before a message becomes eligible for compaction.
- The active segment is never compacted.

Retention can be set per topic, so one cluster can mix time/size retention and compacted topics.

## Checked

Method: docs-checked 2026-11-09 against kafka.apache.org/42/design/design/ (Replication, Replicated Logs, Unclean Leader Election, Availability and Durability, Log Compaction sections read in full)
