---
id: computing-software.messaging-and-integration.apache-zookeeper.consistency-guarantees
name: consistency-guarantees
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, consistency, sequential-consistency, stale-reads, sync]
level: advanced
status: docs-checked
description: "ZooKeeper consistency guarantees: sequential consistency, atomicity, single system image, reliability, timeliness, and why cross-client views can differ."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Consistency guarantees

Reads are faster than writes because ZooKeeper can serve older data. The guarantees:

- Sequential consistency: updates from a client are applied in the order sent.
- Atomicity: updates succeed or fail; no partial results.
- Single system image: a client sees the same view whichever server it connects to; it never sees an older view after failing over with the same session.
- Reliability: once applied, an update persists until a client overwrites it. If a client gets a successful return code, the update was applied; on failures such as communication errors or timeouts the client does not know whether it applied. Updates a client has seen, through a read or successful update, are not rolled back when recovering from server failures.
- Timeliness: the client's view is up to date within a time bound (on the order of tens of seconds); changes are seen within it, or the client detects a service outage.

Not guaranteed: simultaneously consistent cross-client views. If client A sets /a from 0 to 1 and tells client B to read /a, B may read 0 depending on its server. If both must read the same value, B should call `sync()` before the read.

These guarantees let leader election, barriers, queues and read/write revocable locks be built purely at the client (see the Recipes page).

## Checked
Confirmed against the Programmers Guide consistency section, 2026-11-08. Removed: the linearizable-writes and "ordered sequential consistency" labels, the Internals-page remark on sync, and the verification line, none of which that page states.
Method: docs-only read of cited pages, 2026-11-08
