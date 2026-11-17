---
id: computing-software.messaging-and-integration.apache-zookeeper.heap-and-swapping
name: heap-and-swapping
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, java-heap, swapping, things-to-avoid, performance]
level: practitioner
status: docs-checked
description: "Sizing the ZooKeeper JVM heap below physical memory to avoid swapping, plus the other deployment mistakes the guide warns about."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Heap size and things to avoid

- Set the maximum heap well below physical memory, and never above it. Swapping severely degrades ZooKeeper: requests are ordered, so if one swaps the queued ones probably will too.
- Worked example from the guide: on a 4 GB machine, use about a 3 GB heap (the OS and cache also need memory), not 4 GB or 6 GB.
- Estimate the heap by running load tests and staying well below the usage that would cause swapping.
- The admin guide's "Things to Avoid":
  - inconsistent server lists across the ensemble,
  - poor transaction log placement (a dedicated device; a dedicated partition is not enough),
  - incorrect Java heap size,
  - a publicly accessible deployment: the ensemble expects a trusted environment, so put it behind a firewall.
- The shipped zkServer scripts launch the JVM with HeapDumpOnOutOfMemoryError and a kill on OutOfMemoryError.

Verify: the OS shows no swap use for the ZooKeeper process.

## Checked

Method: docs-checked 2026-11-09 against the ZooKeeper Administrator's Guide (deployment, Things to Avoid); the Programmer's Guide source, the znode-size claim and the mntr 80 percent heap check were dropped as unconfirmed.
