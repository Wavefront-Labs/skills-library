---
id: computing-software.data-engineering.apache-nifi.cluster-basic-setup
name: cluster-basic-setup
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, clustering, zookeeper, nifi-properties, cluster-node]
level: practitioner
status: docs-checked
description: "Minimum nifi.properties for a clustered node: is.node, node address, protocol port above 1024, ZooKeeper connect string, cluster state provider, firewall file and thread limits."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Basic cluster setup

On every node:
- `nifi.cluster.is.node=true`
- `nifi.cluster.node.address`: defaults to localhost if blank.
- `nifi.cluster.node.protocol.port`: an open port above 1024.
- `nifi.cluster.node.protocol.max.threads`: 50.
- `nifi.zookeeper.connect.string`: comma-separated host:port list for the whole ZooKeeper quorum.
- `nifi.zookeeper.root.node`: the Basic Cluster Setup text says the default is `/root`, but the System Properties table says `/nifi`; set it explicitly, because the root node plus the ZooKeeper instance decide which cluster a node joins.
- `nifi.state.management.provider.cluster`: must name a provider defined in `state-management.xml`.
- `nifi.cluster.firewall.file`: optional file of permitted hosts, IPs or CIDR subnets, one per line.
- Use the same HTTP or HTTPS setting everywhere; set `nifi.cluster.protocol.is.secure=true` for two-way TLS.

Verify: start the nodes (order does not matter), open any node's UI and check the Cluster page lists every node.

Per the Security section, `nifi.cluster.protocol.is.secure=true` (default false) always requires two-way SSL using each node's keystore and truststore.

## Checked

Checked against the NiFi Administration Guide, Basic Cluster Setup, Cluster Node, ZooKeeper properties and Security sections: is.node, node address (localhost if blank), protocol port above 1024, max threads 50, connect string, state provider, firewall file (one entry per line; hostnames, IPs or CIDR subnets) and two-way SSL for secure cluster traffic match. Corrected the root node default, which the guide states two ways, and reworded the Connected-dialog verify step.

Method: docs-only read of cited pages, 2026-11-08
