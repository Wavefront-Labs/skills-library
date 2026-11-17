---
id: computing-software.messaging-and-integration.apache-zookeeper.watches
name: watches
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, watches, one-time-trigger, getdata, getchildren, exists, events]
level: practitioner
status: docs-checked
description: "ZooKeeper standard watches: which calls set them, event types, one-time trigger semantics, ordering guarantees and the cases where events are missed."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Watches

- Set as a side effect of the read calls `getData()`, `getChildren()` and `exists()`. `getData()` and `exists()` set data watches; `getChildren()` sets child watches.
- Events: Created (enabled by exists), Deleted (exists, getData, getChildren), Changed (exists, getData), Child (getChildren).
- A standard watch is a one-time trigger sent to the client that set it; to keep being notified, set another watch.
- Triggers: setData triggers data watches on that znode; create triggers a data watch on the new znode and a child watch on the parent; delete triggers data and child watches on the deleted znode and a child watch on the parent.
- Ordering: watches are ordered with respect to other events, other watches and asynchronous replies. A client sees the watch event before the new data, and event order matches the order of updates seen by the service.
- Watches are asynchronous, so the event may arrive after the change call has returned to the client that made the change.
- Because of latency between the event and re-registering, a znode may change several times in between; you cannot reliably see every change.
- The same watch object registered for both exists and getData fires once for a deletion.
- Watches are held on the server the client is connected to. While disconnected no watches are received; session events go to all outstanding watch handlers, so use them to enter a safe mode. On reconnect, registered watches are re-registered and triggered if needed.
- One missed case: a watch for the existence of a not-yet-created znode is missed if the znode is created and deleted while disconnected.
- `removeWatches` removes watches; with the local flag true a client can remove them without a server connection.

## Checked
Confirmed against the Programmers Guide watches section, 2026-11-08. Removed: the "wait for the connected event" advice and the zkCli verification line, which the page does not give.
Method: docs-only read of cited pages, 2026-11-08
