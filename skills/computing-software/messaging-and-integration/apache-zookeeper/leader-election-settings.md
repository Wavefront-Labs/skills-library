---
id: computing-software.messaging-and-integration.apache-zookeeper.leader-election-settings
name: leader-election-settings
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, leader-election, leaderserves, cnxtimeout, quorumlistenonallips, electionportbindretry]
level: advanced
status: docs-checked
description: "Quorum and election tuning with defaults: leaderServes, cnxTimeout, quorumCnxnTimeoutMs, electionPortBindRetry, quorumListenOnAllIPs, observer delays, hierarchical weights."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Election and quorum settings

- `electionAlg`: default 3; only FastLeaderElection exists since 3.6.0.
- `leaderServes` (`zookeeper.leaderServes`): default yes; the leader accepts client connections.
- `cnxTimeout` (`zookeeper.cnxTimeout`): default 5 seconds, for electionAlg 3.
- `quorumCnxnTimeoutMs`: default -1, meaning syncLimit x tickTime.
- `electionPortBindRetry`: default 3; 0 retries forever.
- `quorumListenOnAllIPs`: default false; true listens for peers on all addresses.
- `tcpKeepAlive`: default false (quorum sockets); `clientTcpKeepAlive` default false (client sockets).
- `maxTimeToWaitForEpoch` (`zookeeper.leader.maxTimeToWaitForEpoch`, 3.6.0+): maximum time to wait for epochs from voters when activating a leader; past it the leader goes back to LOOKING and elects again. The guide says it can be much smaller than initLimit x tickTime.
- `observer.reconnectDelayMs` default 0; `observer.election.DelayMs` default 200.
- `group.x` and `weight.x` define hierarchical quorums; default weight is 1.
- `reconfigEnabled`: default false.

Verify: kill the leader in a test ensemble and confirm a survivor becomes leader (for example with the `srvr` four-letter command, which is whitelisted by default).

## Checked

Read the relevant entries of the ZooKeeper Administrator's Guide. Confirmed electionAlg, leaderServes, cnxTimeout, quorumCnxnTimeoutMs, electionPortBindRetry, quorumListenOnAllIPs, tcpKeepAlive and clientTcpKeepAlive, observer delays, group.x and weight.x, and reconfigEnabled defaults. Expanded maxTimeToWaitForEpoch from the guide. Removed the election_time_count metric from the verify step because the guide does not name it.

Method: docs-only read of cited pages, 2026-11-08
