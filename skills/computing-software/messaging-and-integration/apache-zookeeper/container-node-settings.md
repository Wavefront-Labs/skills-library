---
id: computing-software.messaging-and-integration.apache-zookeeper.container-node-settings
name: container-node-settings
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, container-znode, znode-container, checkintervalms, maxperminute]
level: advanced
status: docs-checked
description: "Container znodes: purpose for locks and elections, deletion after last child, NoNodeException handling, and the three znode.container settings."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
  - https://zookeeper.apache.org/doc/current/zookeeperCLI.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container znodes

- Added in 3.5.3 as special-purpose znodes for recipes such as leader election and locks.
- When the last child of a container is deleted, the container becomes a candidate for deletion by the server at some point in the future.
- Clients creating children must catch `KeeperException.NoNodeException` and recreate the container znode.
- zkCli creates one with `create -c path`.

Server settings (Java system properties only, new in 3.6.0):
- `znode.container.checkIntervalMs`: interval between checks of candidate container and ttl nodes; default 60000 ms.
- `znode.container.maxPerMinute`: maximum container and ttl nodes deleted per minute, to prevent herding; default 10000.
- `znode.container.maxNeverUsedIntervalMs`: how long a container that has never had children is retained; should be long enough for the client to create the container and then its children. Default 0, meaning such containers are never deleted.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Programmer's Guide (Container Nodes), the Administrator's Guide (znode.container.* options) and the CLI guide (`create -c`). Removed: the "Verify" claim that the container disappears within about one check interval (the pages say only "at some point in the future").
