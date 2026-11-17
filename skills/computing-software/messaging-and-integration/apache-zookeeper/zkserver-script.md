---
id: computing-software.messaging-and-integration.apache-zookeeper.zkserver-script
name: zkserver-script
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, zkserver-sh, zkenv, start-foreground, status, client-jvmflags]
level: intro
status: docs-checked
description: "bin/zkServer.sh commands: start, start-foreground, stop, restart, status, version, print-cmd, plus zkEnv.sh ZOO_LOG_DIR and the SSL status caveat."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperTools.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# zkServer.sh

- Usage: `./zkServer.sh {start|start-foreground|stop|version|restart|status|upgrade|print-cmd}`. `start-foreground` runs the server in the foreground for debugging; `print-cmd` prints the parameters of the start-up; `upgrade` is marked deprecated; `version` shows the server version.
- `status` shows the status, mode and role of the server (the example output includes "JMX enabled by default", the config path and "Mode: standalone"). It establishes a client connection to run diagnostic commands, so when the cluster runs in client SSL only mode (clientPort omitted from zoo.cfg) supply SSL settings through `CLIENT_JVMFLAGS` first, for example `-Dzookeeper.clientCnxnSocket=org.apache.zookeeper.ClientCnxnSocketNetty`, the `zookeeper.ssl.trustStore.*` and `zookeeper.ssl.keyStore.*` properties, and `-Dzookeeper.client.secure=true`.
- `zkEnv.sh` sets the server environment; `ZOO_LOG_DIR` is the directory to store the logs.
- `zkCleanup.sh` cleans old snapshots and transaction logs: args `dataLogDir [snapDir] -n count`, where `count` is the number to keep and must be at least 3 (example `./zkCleanup.sh -n 5`).

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the ZooKeeper Tools page (zkServer.sh, zkEnv.sh, zkCleanup.sh). Removed: "JMX local only" and the "Verify" line, which the page does not state.
