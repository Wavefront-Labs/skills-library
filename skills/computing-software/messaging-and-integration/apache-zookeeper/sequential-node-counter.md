---
id: computing-software.messaging-and-integration.apache-zookeeper.sequential-node-counter
name: sequential-node-counter
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, sequential-nodes, counter, ordering, overflow, create-s]
level: practitioner
status: docs-checked
description: "How ZooKeeper sequential znode suffixes work: ten-digit zero-padded counter per parent, signed 4-byte overflow, and lexicographic ordering pitfalls."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html
  - https://zookeeper.apache.org/doc/current/zookeeperTutorial.html
  - https://zookeeper.apache.org/doc/current/zookeeperCLI.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sequential nodes

- The counter has the format `%010d`: 10 digits, zero padded, so that names sort easily. The counter is maintained by the parent node.
- It is a signed int (4 bytes); incrementing beyond 2147483647 overflows and the resulting name is `-2147483648`.
- zkCli: `create [-s] [-e] [-c] [-t ttl] path [data] [acl]`; `create -s /path data` makes a persistent-sequential node and `create -s -e` an ephemeral-sequential one.
- `getChildren()` returns children in lexicographic order, which does not necessarily follow numeric counter order. The tutorial's queue consumer strips the `element` prefix from each name and compares the numeric counters to find the smallest.
- The tutorial's producer uses the SEQUENCE flag so the counter imposes a total order on queue elements.

## Checked

Confirmed against the Programmer's Guide (Sequence Nodes -- Unique Naming), the Tutorial (queue produce and consume) and the CLI guide (create syntax and examples). Removed the unsourced claims about a lost create reply and about locks and elections, and the Verify step.

Method: docs-only read of cited pages, 2026-11-08
