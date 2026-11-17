---
id: computing-software.data-engineering.apache-nifi.connection-load-balancing
name: connection-load-balancing
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, load-balancing, connections, clustering, compression]
level: practitioner
status: docs-checked
description: "Per-connection load balance strategies (none, partition by attribute, round robin, single node) and compression options, plus the cluster connection summary."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/user-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Load balancing a connection

Settings tab on a connection:
- Strategy: default "Do not load balance"; others are Partition by attribute, Round robin, Single node.
- Compression: default "Do not compress"; or compress attributes only, or attributes and content.

The cluster-level transport settings live in `nifi.cluster.load.balance.*` (port 6342 by default).

To see how data is spread, open Global Menu > Summary > Connections and click "View Connection Details" for the Cluster Connection Summary (data per node).

Verify: after enabling round robin, each node's queue in the cluster summary receives FlowFiles.

## Checked

Checked against the NiFi User Guide connection Load Balance Strategy, Compression and Cluster Connection Summary sections, and the Administration Guide for `nifi.cluster.load.balance.port` (6342): strategy and compression names and defaults and the Summary > Connections path match.

Method: docs-only read of cited pages, 2026-11-08
