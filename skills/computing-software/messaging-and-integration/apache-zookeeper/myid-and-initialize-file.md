---
id: computing-software.messaging-and-integration.apache-zookeeper.myid-and-initialize-file
name: myid-and-initialize-file
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, myid, initialize, new-ensemble, bootstrap, server-id]
level: practitioner
status: docs-checked
description: "Server IDs and bootstrapping a new ensemble: myid range 1-255 (1-254 with TTL nodes), the empty initialize marker file, and voting behaviour of empty peers."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# myid and the initialize marker

- Put a `myid` file in `dataDir` containing only that server's ID. IDs are unique, between 1 and 255; if extended features such as TTL nodes are enabled the range is 1-254.
- Every server's config lists the same members; each learns its identity from `myid`.
- When bringing up a brand-new ensemble, also create an empty `initialize` file in the same directory as `myid`. The server then creates an empty database and removes the marker.
- Without the marker, an empty data directory means the peer has no voting rights until it syncs from an active leader.
- Start with `java -cp zookeeper.jar:lib/*:conf org.apache.zookeeper.server.quorum.QuorumPeerMain zoo.conf` (or `zkServer.sh`).
- Data directory auto-creation can be disabled with `zookeeper.datadir.autocreate=false` (or `ZOO_DATADIR_AUTOCREATE_DISABLE=1` when using `zkServer.sh`); `zkServer-initialize.sh` then creates the required directories and can set up `myid`. Running it also creates the required initialization file when db existence validation is on.

Verify: the `initialize` file is gone after first start and `bin/zkCli.sh -server 127.0.0.1:2181` connects.

## Checked

Method: docs-checked 2026-11-09 against zookeeperAdmin.html (Clustered Setup steps, data directory autocreation and db existence validation sections)
