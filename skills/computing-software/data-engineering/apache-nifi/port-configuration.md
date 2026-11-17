---
id: computing-software.data-engineering.apache-nifi.port-configuration
name: port-configuration
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, ports, nifi-properties, firewall, cluster]
level: practitioner
status: docs-checked
description: "NiFi default ports and the nifi.properties keys that set them: HTTPS 8443, site-to-site, cluster protocol, load balancing 6342, ZooKeeper 2181, TLS Toolkit CA 9443."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NiFi ports

| Function | Key | Default |
|---|---|---|
| HTTPS | `nifi.web.https.port` | 8443 |
| Site-to-Site RAW | `nifi.remote.input.socket.port` | blank (10443 with TLS Toolkit) |
| Cluster node protocol | `nifi.cluster.node.protocol.port` | blank (11443 with TLS Toolkit) |
| Cluster load balancing | `nifi.cluster.node.load.balance.port` in the guide's port table (the System Properties table names it `nifi.cluster.load.balance.port`) | 6342 |
| Bootstrap listener | `nifi.listener.bootstrap.port` | random ephemeral |
| Embedded ZooKeeper client | `clientPort` in zookeeper.properties (marked deprecated since 1.10: the client port is now appended to the `server.N` line) | 2181 |
| TLS Toolkit CA | toolkit setting | 9443 |

Embedded ZooKeeper quorum lines look like `server.N=nifi-nodeN-hostname:2888:3888;2181`.

With no security configured NiFi binds to 127.0.0.1 only. Open the ports your topology uses between nodes.

Verify: each configured port is listening on the intended interface and reachable from peer nodes.

## Checked

Checked against the NiFi Administration Guide, Port Configuration and System Properties sections: HTTPS 8443, the TLS Toolkit values 10443 and 11443 for the two blank-by-default ports, 6342, the random ephemeral bootstrap port, CA port 9443, and the loopback-only binding without security match. Flagged the two property-name and deprecation discrepancies inside the guide.

Method: docs-only read of cited pages, 2026-11-08
