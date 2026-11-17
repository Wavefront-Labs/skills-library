---
id: computing-software.messaging-and-integration.apache-zookeeper.multi-server-timing-limits
name: multi-server-timing-limits
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, initlimit, synclimit, connecttolearnermasterlimit, server-x, standaloneenabled, multiaddress]
level: practitioner
status: docs-checked
description: "Ensemble settings: initLimit, syncLimit, connectToLearnerMasterLimit, server.x syntax, electionAlg, multiAddress and standaloneEnabled with defaults."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-server settings

- `initLimit` (example 5): ticks followers get to connect and sync to the leader. Raise it for a large dataset.
- `syncLimit` (example 2): ticks a follower may lag before being dropped.
- `connectToLearnerMasterLimit`: ticks for followers to connect to the leader after election; defaults to `initLimit`.
- `server.x=host:port:port`: first port for followers to the leader, second for election. All servers share the same list.
- `electionAlg`: default 3 (TCP fast leader election); 1 and 2 deprecated.
- `multiAddress.enabled`: default false; since 3.6.0 allows several addresses per server separated by `|`. `multiAddress.reachabilityCheckTimeoutMs` default 1000.
- `standaloneEnabled`: default true; false allows a single server to run replicated and permits reconfiguring down to one node.

Tune limits in ticks: with tickTime 2000, initLimit 5 is 10 seconds.

Verify: after a restart all followers connect and sync within initLimit ticks (check each server's role with the `srvr` four-letter command).

## Checked

Read the relevant entries of the ZooKeeper Administrator's Guide. Confirmed initLimit and syncLimit (example values 5 and 2 with tickTime=2000), connectToLearnerMasterLimit, the server.x port roles, electionAlg history, multiAddress.enabled and reachabilityCheckTimeoutMs (1000), and standaloneEnabled. The 10 second figure is initLimit 5 x tickTime 2000 ms. Reworded the verify step to a documented command.

Method: docs-only read of cited pages, 2026-11-08
