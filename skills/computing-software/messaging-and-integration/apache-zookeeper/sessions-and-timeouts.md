---
id: computing-software.messaging-and-integration.apache-zookeeper.sessions-and-timeouts
name: sessions-and-timeouts
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, sessions, session-timeout, reconnection, expiration, session-id]
level: practitioner
status: docs-checked
description: "ZooKeeper client sessions: states, 2x to 20x tickTime negotiated timeout, session id and password, automatic reconnect and handling expiration."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sessions

- Client states: CONNECTING, CONNECTED, CLOSED.
- Timeout is negotiated: minimum 2 x tickTime, maximum 20 x tickTime by default (`minSessionTimeout`, `maxSessionTimeout`, 3.3.0+).
- Identity is a 64-bit session ID plus a server-created password any server can validate; the client sends both when it reconnects to another server.
- The client library reconnects automatically. Do not create a new session on disconnect; create one only after an expiration notification.
- The cluster expires sessions (no heartbeat within the timeout) and deletes their ephemeral nodes; the disconnected client learns of it only after reconnecting.
- After SESSION_EXPIRED or AUTH_FAILED the handle is invalid.
- Changing the server list may drop the connection (probabilistic load balancing); clients on removed servers must move.

Verify: killing the client and waiting about the negotiated timeout removes its ephemeral nodes (`dump` shows none).

## Checked

Method: docs-checked 2026-11-09 against the ZooKeeper Programmer's Guide (sessions section, Java binding) and Administrator's Guide (minSessionTimeout, maxSessionTimeout).
