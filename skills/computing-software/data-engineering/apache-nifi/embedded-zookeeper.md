---
id: computing-software.data-engineering.apache-nifi.embedded-zookeeper
name: embedded-zookeeper
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, embedded-zookeeper, zookeeper-properties, myid, clustering]
level: advanced
status: docs-checked
description: "Run NiFi's embedded ZooKeeper: start flag, zookeeper.properties dataDir and server.N lines, ports 2181/2888/3888, myid files, secure port 2281, 3 or 5 node guidance."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Embedded ZooKeeper

1. On nodes that host ZooKeeper set `nifi.state.management.embedded.zookeeper.start=true`; `nifi.state.management.embedded.zookeeper.properties` points to `./conf/zookeeper.properties`.
2. In that file, `dataDir` defaults to `./state/zookeeper`; add one `server.N` line per member, such as `server.1 = myhost:2888:3888;2181` (2888 quorum, 3888 election, 2181 client; format `<hostname>:<quorum port>[:<leader election port>][:role];[<client port address>:]<client port>`, NiFi 1.10 and later).
3. Create a `myid` file in the data directory containing the node's server index.
4. Point `nifi.zookeeper.connect.string` at the members.

Guidance: the guide advises three or five ZooKeeper nodes (four gives no benefit over three). With TLS (NiFi 1.13 and later) set `secureClientPort=2281` in `zookeeper.properties` and `nifi.zookeeper.client.secure=true`; the embedded server then exposes no insecure `clientPort`. Open the ports between nodes in the firewall.

Verify: each ZooKeeper node has its `myid` file and the nodes form a quorum and join the cluster.

## Checked

Checked against the NiFi Administration Guide, Embedded ZooKeeper Server and Embedded ZooKeeper with TLS sections: start and properties keys, dataDir default, server.N format, myid file, 3 or 5 node advice, secureClientPort 2281 and the 2888 and 3888 ports match. The nifi-app.log verify wording was removed as unsourced.

Method: docs-only read of cited pages, 2026-11-08
