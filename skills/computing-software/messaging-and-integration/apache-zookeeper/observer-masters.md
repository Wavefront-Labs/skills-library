---
id: computing-software.messaging-and-integration.apache-zookeeper.observer-masters
name: observer-masters
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, observer-master, observermasterport, leader-offload, observer-scaling]
level: advanced
status: docs-checked
description: "Offload the ZooKeeper leader by letting observers sync from followers: observerMasterPort setting, ObserverMaster thread and when it helps."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperObservers.html
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Observer masters

- Default: observers learn proposals by connecting to the leader along its quorum port.
- Option: let observers connect to followers instead, so the leader focuses on coordinating the commit of writes.
- Enable by adding `observerMasterPort=2191` (the guide's example port) to the server config of all members. Observers then connect to peers (leaders and followers) on that port and followers create an ObserverMaster thread listening on it. Admin guide: with the property set, a server hosts observer connections in follower mode as well as leader mode, and an observer attempts to connect to any voting peer.
- Benefits per the guide: better performance when the leader is under high load (for example after an election when many learners sync), fewer connections on the leader, the number of observers can scale into the hundreds, and observers finish syncing and serve clients sooner.
- Related admin settings: `observer.reconnectDelayMs` (default 0 ms; delay before an observer reconnects after losing its leader connection), `observer.election.DelayMs` (default 200 ms; delays observer participation in an election), `syncEnabled` (default true; observers log transactions and write snapshots like participants).

## Checked
Confirmed against the Observers guide and the Administrator's Guide parameter entries, 2026-11-08. Removed: the verification step about leader connection counts, which the pages do not give.
Method: docs-only read of cited pages, 2026-11-08
