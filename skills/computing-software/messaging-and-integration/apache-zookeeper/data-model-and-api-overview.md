---
id: computing-software.messaging-and-integration.apache-zookeeper.data-model-and-api-overview
name: data-model-and-api-overview
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, overview, data-model, api, replicated-database, leader]
level: intro
status: docs-checked
description: "What ZooKeeper is: hierarchical znode namespace, the seven API operations, in-memory replicated database, reads served locally and writes forwarded to the leader."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperOver.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Overview

- A coordination service for synchronisation, configuration maintenance, groups and naming; Java and C bindings.
- Namespace is a file-system-like hierarchy of znodes holding small data.
- API: create, delete, exists, get data, set data, get children, sync.
- Each server holds the full tree in memory; updates are logged to disk before being applied.
- A client connects to one server: reads come from its local replica; writes go to the leader and are agreed by followers via the atomic messaging protocol.
- Best on read-heavy loads (around 10:1 reads to writes).
- Watches notify of change; if the connection breaks the client gets a local notification.

Verify: you can name which operation is served locally (reads) and which needs the leader (writes).

## Checked

Method: docs-checked 2026-11-09 against zookeeperOver.html (full page read)
