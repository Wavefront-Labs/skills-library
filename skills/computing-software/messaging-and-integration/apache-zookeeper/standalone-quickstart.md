---
id: computing-software.messaging-and-integration.apache-zookeeper.standalone-quickstart
name: standalone-quickstart
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, standalone, getting-started, zoo-cfg, zkserver]
level: intro
status: docs-checked
description: "Start a single standalone ZooKeeper server for development: the three-line zoo.cfg, zkServer.sh start and what standalone does not protect against."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperStarted.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Standalone quickstart

1. Create a configuration file, conventionally `conf/zoo.cfg` (the file can be called anything):
```
tickTime=2000
dataDir=/var/lib/zookeeper
clientPort=2181
```
2. `dataDir` must be an existing directory, empty to start with. It holds in-memory database snapshots and, unless specified otherwise, the transaction log.
3. `tickTime` is the basic time unit in ms, used for heartbeats; the minimum session timeout is twice the tickTime.
4. `clientPort` is the port to listen on for client connections.
5. Start with `bin/zkServer.sh start`.
6. Connect with `bin/zkCli.sh -server 127.0.0.1:2181`; the client prints "Welcome to ZooKeeper!" and `ls /` lists `[zookeeper]` on a fresh server.

Logging uses logback; messages go to the console (default) and/or a log file depending on the logback configuration.

Standalone has no replication: if the process fails the service goes down. The page calls this fine for most development, and convenient for evaluation and testing; production should run replicated mode. For long-running production systems dataDir and logs must be managed externally.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Getting Started page (standalone operation). Reworded: "unpack a stable release" dropped as the page does not say it.
