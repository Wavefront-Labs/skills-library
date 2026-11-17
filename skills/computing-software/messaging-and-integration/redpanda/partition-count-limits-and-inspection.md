---
id: computing-software.messaging-and-integration.redpanda.partition-count-limits-and-inspection
name: partition-count-limits-and-inspection
category: computing-software
field: messaging-and-integration
product: redpanda
tags: [partitions, limits, invalid-partitions, file-descriptors, memory, cluster-config]
level: advanced
status: docs-checked
description: "How Redpanda caps partition replicas by core, memory and file descriptors, the properties and defaults behind each limit, and how to read them with rpk cluster config get."
sources:
  - https://docs.redpanda.com/streaming/current/deploy/redpanda/manual/sizing/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Guidance: keep total partitions at or below 1K per core and under 50K per cluster. Beyond 1K per core, expect higher latency, more leadership elections and less stability.

**Enforcement.** On topic creation or adding partitions, Redpanda checks the resulting total of partition replicas (partitions x replication factor; internal topics such as `__consumer_offsets` count, but are not blocked). A request over any limit fails with `INVALID_PARTITIONS` and the broker logs a `Refusing to create` warning naming the limit. Core and memory limits assume every broker is as small as the smallest broker, so partitions can still move during rebalancing or decommissioning.

| Limit | Maximum replicas | Properties and defaults |
|---|---|---|
| Core | brokers x cores on smallest broker x `topic_partitions_per_shard`, minus brokers x `topic_partitions_reserve_shard0` | 5000 and 0 |
| Memory | brokers x memory on smallest broker x `topic_partitions_memory_allocation_percent` / `topic_memory_per_partition` | 10 and 204800 (200 KiB) |
| File descriptors | brokers x soft open file limit on the controller leader / `topic_fds_per_partition` | 5 |

Notes from the page:
- The file descriptor check reads the limit only on the controller leader and assumes all brokers match; an unlimited soft limit disables the check.
- `topic_memory_per_partition` of 400 KiB or more makes Redpanda use all broker memory for the memory limit, preserving older behavior.
- Worked example: one broker with one core and 1 GiB gives 1 GiB x 10% / 200 KiB = 524 replicas, well under the 5,000 core limit.
- `dev-container` mode sets `topic_partitions_per_shard` to 1000; it is the default when `developer_mode` is true in `redpanda.yaml`, as in the Docker image.

**Inspect the values**
```bash
rpk cluster config get topic_partitions_per_shard
rpk cluster config get topic_partitions_reserve_shard0
rpk cluster config get topic_memory_per_partition
rpk cluster config get topic_partitions_memory_allocation_percent
rpk cluster config get topic_fds_per_partition
```

## Checked

2026-11-04. The recommendations, limit table, notes, worked example and commands were confirmed on the Sizing page (Partition count section).

Method: documentation only; no commands were run.
