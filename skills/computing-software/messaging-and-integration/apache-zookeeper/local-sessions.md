---
id: computing-software.messaging-and-integration.apache-zookeeper.local-sessions
name: local-sessions
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, local-sessions, localsessionsenabled, session-upgrade, ephemeral]
level: advanced
status: docs-checked
description: "ZooKeeper local sessions: localSessionsEnabled and localSessionsUpgradingEnabled (both default false), limits of a local session and the upgrade path."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperProgrammers.html
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Local sessions (3.5.0)

- Added in 3.5.0. Creating and closing global sessions needs quorum confirmation and can become the bottleneck with thousands of clients; local sessions are a lighter type.
- `localSessionsEnabled` and `localSessionsUpgradingEnabled`: new in 3.5, true or false, default false for both. The upgrading option only matters when `localSessionsEnabled` is on.
- With upgrading disabled: a local session cannot create ephemeral nodes; once lost it cannot be re-established with the session id and password (its watches are gone), though a lost TCP connection is not a lost session if the same server is reached again within the timeout; session info lives only on the connected server, the leader does not know of it and nothing is written to disk; pings and expiry are handled by that server.
- With upgrading enabled: a local session is upgraded to global automatically when needed. The guide says creating an ephemeral node is currently the only operation needing the upgrade; the session keeps its session id.
- The guide's stated reason for the option to disable upgrading: in a large deployment, clients connecting through observers are meant to be local only, so it is a safeguard against someone accidentally creating many ephemeral nodes and global sessions.
- Connection throttling weights for session types (`zookeeper.connection_throttle_local_session_weight` default 1, global 3, renew 2) are in the Administrator's Guide.

## Checked

Confirmed against the Programmer's Guide (Local session) and the Administrator's Guide (localSessionsEnabled, throttle weights). Removed the unsourced Verify step.

Method: docs-only read of cited pages, 2026-11-08
