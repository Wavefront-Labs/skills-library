---
id: computing-software.messaging-and-integration.apache-zookeeper.minimum-config-keywords
name: minimum-config-keywords
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, clientport, secureclientport, datadir, ticktime, zoo-cfg]
level: intro
status: docs-checked
description: "The minimum zoo.cfg keywords: clientPort, secureClientPort, observerMasterPort, dataDir and tickTime, what each means and the derived session timeout bounds."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Minimum configuration keywords

The Administrator's Guide lists these as keywords that must be defined in the configuration file.

| Keyword | Meaning |
|---|---|
| `clientPort` | port to listen on for client connections (plaintext) |
| `secureClientPort` | port for SSL client connections; specifying both it and `clientPort` enables mixed mode, omitting either disables that mode. SSL needs the Netty `serverCnxnFactory` / `clientCnxnSocket` |
| `observerMasterPort` | port to listen on for observer connections; if set, the server hosts observer connections in follower mode as well as leader mode |
| `dataDir` | location of in-memory database snapshots and, unless specified otherwise, the transaction log |
| `tickTime` | basic time unit in ms, used for heartbeats and timeouts (the page's example is 2000) |

Derived from tickTime: `minSessionTimeout` defaults to 2 x tickTime and `maxSessionTimeout` to 20 x tickTime (both new in 3.3.0, no Java system property).

`clientPortAddress` (new in 3.3.0) is optional; by default the server accepts connections to clientPort on any address, interface or NIC. Multi-server setups add `initLimit`, `syncLimit` and `server.x` lines, whose timeouts are counted in ticks. From 3.5.0 some parameters belong in a dynamic configuration file; the server moves them over automatically if left in the static file.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Administrator's Guide (Minimum Configuration and Advanced Configuration). Removed: the "Verify" line about `ruok` returning `imok` (not given in the sections read) and the claim that no defaults exist.
