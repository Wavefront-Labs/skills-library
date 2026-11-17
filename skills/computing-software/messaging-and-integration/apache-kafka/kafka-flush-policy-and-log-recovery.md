---
id: computing-software.messaging-and-integration.apache-kafka.kafka-flush-policy-and-log-recovery
name: kafka-flush-policy-and-log-recovery
category: computing-software
field: messaging-and-integration
product: apache-kafka
tags: [apache-kafka, fsync, log-recovery, crc32, page-cache]
level: advanced
status: docs-checked
description: "Leave application fsync disabled, rely on replication and OS flushing, and know how log recovery uses CRC checks after a crash."
sources:
  - https://kafka.apache.org/42/operations/hardware-and-os/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose a flush policy and understand crash recovery.

Kafka writes data to the filesystem immediately; the flush policy controls when it is forced to disk, by elapsed time or message count. The docs recommend disabling application-level fsync and relying on the OS background flush plus Kafka's own background flush. Durability does not require syncing to disk because a failed node recovers from its replicas, which the docs consider a stronger guarantee than local fsync. Application-level policies remain supported if you want both.

Drawbacks of application-level flush: less efficient disk usage (the OS has less room to reorder writes) and extra latency, since fsync on most Linux filesystems blocks writes to the file.

Page cache: data stays there until flushed by an application fsync or OS policy, via background flusher threads. If they fall behind, writers block, adding latency. `/proc/meminfo` shows current memory state. The cache batches small writes, lets the I/O scheduler reorder them, and uses free memory automatically.

Recovery after a crash: for log segments not known to be fsynced, Kafka checks each message's CRC and rebuilds the offset index at startup.

## Checked

Method: 2026-11-08 docs-only read of the cited Kafka 4.2 hardware-and-os page. Removed the claims on the exact validity rule, truncation to last valid offset and the two corruption types, which the page text I read did not support. No hands-on run.
