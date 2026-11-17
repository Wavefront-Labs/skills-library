---
id: computing-software.messaging-and-integration.apache-zookeeper.jmx-monitoring
name: jmx-monitoring
category: computing-software
field: messaging-and-integration
product: apache-zookeeper
tags: [messaging-and-integration, apache-zookeeper, jmx, mbeans, jconsole, org-apache-zookeeperservice, monitoring]
level: practitioner
status: docs-checked
description: "Inspect ZooKeeper through JMX: local-only default in zkServer.sh, jconsole use, MBean tree for replicated and standalone servers, and logging MBean properties."
sources:
  - https://zookeeper.apache.org/doc/current/zookeeperJMX.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JMX

- Start via `org.apache.zookeeper.server.quorum.QuorumPeerMain`; MBeans register at init. `zkServer.sh` supports only local JMX by default; remote needs the standard Java JMX setup (see the JMX Management Guide).
- jconsole (in the JDK, typically `JDK_HOME/bin/jconsole`): connect to the local or remote process, open MBeans tab, expand `org.apache.ZooKeeperService`.
- Replicated MBeans: Quorum `ReplicatedServer_id<#>`, LocalPeer/RemotePeer `replica.<#>`, LeaderElection, Leader and Follower, DataTree `InMemoryDataTree`, ServerCnxn named by hex session id.
- Standalone: ZooKeeperServer `StandaloneServer_port<#>`, DataTree, ServerCnxn.
- Logging MBeans: Logback is the default backend since 3.8.0; add `<jmxConfigurator />` to `logback.xml` to register its MBeans. Log4j MBeans (when log4j1 is the SLF4J backend) are deprecated; disable with `-Dzookeeper.jmx.log4j.disable=true`; name via `-Dzookeeper.jmx.log4j.mbean=log4j:hierarchy=default`.

Verify: jconsole lists `org.apache.ZooKeeperService` with your server's MBeans.

## Checked
Confirmed against the ZooKeeper JMX page, 2026-11-08. Added the Logback default-since-3.8.0 note and jconsole location from the page.
Method: docs-only read of cited pages, 2026-11-08
