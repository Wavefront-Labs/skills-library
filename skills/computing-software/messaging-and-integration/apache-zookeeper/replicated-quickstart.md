---
id: computing-software.messaging-and-integration.apache-zookeeper.replicated-quickstart
name: replicated-quickstart
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, replicated-mode, server-list, initlimit, synclimit, myid]
level: practitioner
status: docs-checked
description: "Configure a three-server replicated ZooKeeper ensemble: shared zoo.cfg with server.N lines, initLimit and syncLimit, per-host myid, and single-machine test layout."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperStarted.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Replicated mode quickstart

Every server uses the same `conf/zoo.cfg`:
```
tickTime=2000
dataDir=/var/lib/zookeeper
clientPort=2181
initLimit=5
syncLimit=2
server.1=zoo1:2888:3888
server.2=zoo2:2888:3888
server.3=zoo3:2888:3888
```
- `initLimit=5`: followers get 5 ticks (10 s at tickTime 2000) to connect to the leader.
- `syncLimit=2`: bounds how far a follower may lag the leader.
- `server.X=host:peerPort:electionPort`: 2888 connects followers to the leader, 3888 is leader election.
- Each host needs a `myid` file in `dataDir` containing its number (ASCII), e.g. `1` on server.1.
- Single-machine testing: use localhost with unique port pairs (2888:3888, 2889:3889, 2890:3890) plus a distinct `dataDir`, `clientPort` and config file per server. No redundancy results.
- For lower latency set `dataLogDir` to a separate directory.

Verify: `bin/zkServer.sh status` on each host reports a leader on one and followers on the others.

## Checked

Method: docs-checked 2026-11-09 against zookeeperStarted.html (full page read)
