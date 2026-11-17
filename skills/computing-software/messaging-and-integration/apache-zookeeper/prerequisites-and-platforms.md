---
id: computing-software.messaging-and-integration.apache-zookeeper.prerequisites-and-platforms
name: prerequisites-and-platforms
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, prerequisites, java, jdk, supported-platforms, linux]
level: intro
status: docs-checked
description: "ZooKeeper runtime prerequisites: Java 1.8 or later, which JDKs the admin guide lists, and which operating systems are production versus development only."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prerequisites and supported platforms

- Needs Java 1.8 or later. The admin guide lists JDK 8 LTS, JDK 11 LTS and JDK 12 as supported; Java 9 and 10 are not.
- Support matrix:
  - GNU/Linux: client, server, native client and contrib all Dev and Prod.
  - Solaris, FreeBSD, Windows: client and server Dev and Prod; native client and contrib not supported.
  - Mac OS X: client and server Dev only.
- Other platforms may work but are not fully supported.
- Read the matrix before planning production hosts: pick Linux for the server unless there is a reason not to.

Verify: `java -version` reports 1.8 or later and the host OS is Prod-supported for the server column.

## Checked

Method: docs-checked 2026-11-09 against zookeeperAdmin.html (System Requirements section)
