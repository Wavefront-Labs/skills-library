---
id: computing-software.data-engineering.apache-nifi.state-management-providers
name: state-management-providers
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, state-management, zookeeper-state-provider, local-state, nifi-properties]
level: advanced
status: docs-checked
description: "NiFi state storage: state-management.xml, local and ZooKeeper state providers (Connect String, Root Node, Access Control) and the nifi.properties keys."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# State management

nifi.properties:
- `nifi.state.management.configuration.file`: `./conf/state-management.xml`
- `nifi.state.management.provider.local` (required) and `.cluster` (ignored when not clustered, required on cluster nodes)
- `nifi.state.management.embedded.zookeeper.start` false; `.properties` `./conf/zookeeper.properties`

Providers:
- Local: `WriteAheadLocalStateProvider`, stored in `$NIFI_HOME/state/local`.
- Cluster: `ZooKeeperStateProvider` with `Connect String` (port defaults to 2181 if omitted), `Root Node` (use a team path such as `/nifi/<team>/production` when sharing ZooKeeper), `Access Control` of `Open` or `CreatorOnly` (needs authentication).
- Username/Password are sent in plain text; use only on localhost or encrypted links.

Verify: after restart, a stateful processor resumes from where it left off, which is what state management exists for.

A standalone or disconnected node uses the local provider even for cluster-scope state, so state is not carried over when a standalone instance becomes a cluster.

## Checked

Checked against the NiFi Administration Guide, State Management, ZooKeeper Access Control and System Properties sections: property names, defaults (`./conf/state-management.xml`, embedded ZooKeeper false and `./conf/zookeeper.properties`), the two default providers, Connect String port default 2181, Root Node advice, Open and CreatorOnly, and the plain-text username and password warning all match. The List-processor example was reworded to the page's own statement. Added the standalone-to-cluster state note.

Method: docs-only read of cited pages, 2026-11-08
