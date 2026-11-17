---
id: computing-software.messaging-and-integration.apache-zookeeper.observers
name: observers
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, observers, peertype, non-voting, read-scaling, multi-datacenter]
level: practitioner
status: docs-checked
description: "Add non-voting ZooKeeper observers to scale reads and bridge data centers: peerType=observer, the :observer server-line suffix and the benefits."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperObservers.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Observers

- Non-voting members: they hear the results of votes, not the agreement protocol. Otherwise they work like followers: clients can connect and send reads and writes, and observers forward requests to the leader.
- Why: more voters slow writes (a write needs agreement from generally at least half the ensemble); observers can be added without harming vote performance.
- Not critical to availability, so they can fail or be disconnected without harming the service, and can use less reliable links or sit in another data center. Reads are served locally; writes cause less network traffic than with the vote protocol.

Configure:
1. In the config file of each observer node add `peerType=observer`.
2. In every server's config file, add `:observer` to that server's definition line, e.g. `server.1:localhost:2181:3181:observer`.
3. Connect as to a follower, e.g. `bin/zkCli.sh -server localhost:2181`.

Use cases from the guide: datacenter bridge (ensemble in one data center, only observers in the second, so partitions do not break the ensemble) and a link to a message bus (attach the proposal stream to a publish-subscribe system).

See also observer-masters for letting observers sync from followers (`observerMasterPort`).

## Checked
Confirmed against the ZooKeeper Observers guide, 2026-11-08. Removed: the `zkServer.sh status` verification line, which the page does not give.
Method: docs-only read of cited pages, 2026-11-08
