---
id: computing-software.messaging-and-integration.apache-zookeeper.client-connection-limits
name: client-connection-limits
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, maxclientcnxns, maxcnxns, clientportaddress, connection-limits, servercnxnfactory]
level: practitioner
status: docs-checked
description: "Limit and shape ZooKeeper client connections: maxClientCnxns 60 per IP, maxCnxns, clientPortAddress, listen backlog, keepalive and the Netty connection factory."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Client connection limits

- `maxClientCnxns`: default 60, per client IP per server; 0 removes the limit.
- `maxCnxns` (`zookeeper.maxCnxns`): default 0 = no limit; total concurrent connections per client port.
- `clientPortAddress`: default binds all interfaces.
- `clientPortListenBacklog`: default -1 (Linux uses 50); must be positive if set.
- `clientTcpKeepAlive`: default false.
- `serverCnxnFactory`: default NIOServerCnxnFactory; set NettyServerCnxnFactory for TLS.
- `sessionRequireClientSASLAuth`: default false.
- Session bounds: `minSessionTimeout` default 2 x tickTime, `maxSessionTimeout` default 20 x tickTime.

Verify: a client exceeding the limit from one IP is refused and `cons` (if whitelisted) shows the capped count.

## Checked

Read the relevant entries of the ZooKeeper Administrator's Guide. Confirmed maxClientCnxns, maxCnxns, clientPortAddress, clientPortListenBacklog, clientTcpKeepAlive, serverCnxnFactory, sessionRequireClientSASLAuth, and the session timeout defaults. Removed the num_alive_connections alert example, which the guide does not state, and the load-test advice.

Method: docs-only read of cited pages, 2026-11-08
