---
id: computing-software.messaging-and-integration.apache-zookeeper.quorum-tls-rolling-upgrade
name: quorum-tls-rolling-upgrade
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, quorum-tls, sslquorum, portunification, rolling-restart, upgrade]
level: sme
status: docs-checked
description: "Enable TLS between ZooKeeper quorum members with no downtime using portUnification and sslQuorum, plus keystore and hostname gotchas."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperAdmin.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Quorum TLS without downtime (3.5.5+)

Settings: `sslQuorum` (true/false), `serverCnxnFactory=org.apache.zookeeper.server.NettyServerCnxnFactory`, `portUnification` (true/false), `ssl.quorum.keyStore.location`, `ssl.quorum.keyStore.password`, `ssl.quorum.trustStore.location`, `ssl.quorum.trustStore.password`.

Upgrade path, create the keystores and truststores for all participants first, then:
1. Set `sslQuorum=false` and `portUnification=true` (plus the Netty factory and keystore settings), restart each node in turn and check the quorum is healthy after each.
2. Set `sslQuorum=true` (with `portUnification=true`), rolling restart again.
3. Once the whole ensemble runs on TLS, set `portUnification=false` and do a final rolling restart.

Gotchas:
- Netty is required because NIO does not support SSL.
- The keystore alias (`-alias`) and `-dname` must match the host's hostname, or hostname verification will not work.
- `sslQuorum` default is false.
- Consider enabling `leader.closeSocketAsync` and `learner.closeSocketAsync` with sslQuorum to avoid slow SSL socket closes.

Verify: logs show "Using TLS encrypted quorum communication" after step 2 (and "Port unification disabled" after step 3), and the ensemble keeps a leader throughout.

## Checked

Method: docs-checked 2026-11-09 against the ZooKeeper Administrator's Guide (Quorum TLS and Upgrading existing non-TLS cluster sections).
