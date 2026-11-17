---
id: computing-software.data-engineering.apache-hadoop.hdfs-short-circuit-reads
name: hdfs-short-circuit-reads
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, hdfs, short-circuit, performance, domain-socket, local-reads]
level: advanced
status: docs-checked
description: "Enabling HDFS short-circuit local reads: dfs.client.read.shortcircuit, dfs.domain.socket.path, libhadoop requirement, and why the legacy mode is insecure."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/ShortCircuitLocalReads.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Short-circuit local reads

Normally the DataNode reads the file from disk and sends it over a TCP socket. Short-circuit reads let a client co-located with the data bypass the DataNode and read directly, which the page says gives a substantial performance boost to many applications.

Setup needs `libhadoop.so` enabled (see the Native Libraries page). It uses a UNIX domain socket whose path you set; the DataNode must be able to create it, but no user other than the HDFS user or root should be able to, so paths under `/var/run` or `/var/lib` are often used. Client and DataNode exchange information via a shared memory segment on `/dev/shm`. Configure both the DataNode and the client:

```xml
<property><name>dfs.client.read.shortcircuit</name><value>true</value></property>
<property><name>dfs.domain.socket.path</name><value>/var/lib/hadoop-hdfs/dn_socket</value></property>
```

Legacy short-circuit reads (clients open block files directly) remain available for platforms other than Linux. Set `dfs.client.use.legacy.blockreader.local` to true in addition to `dfs.client.read.shortcircuit`, set `dfs.datanode.data.dir.perm` to 750 instead of the default 700, and chmod/chown the tree under `dfs.datanode.data.dir` so client and DataNode can read it. The page warns the client can then read all block files, bypassing HDFS permissions. Because it is insecure, access is limited to users listed in `dfs.block.local-path-access.user` (example `foo,bar`).

## Checked

Method: 2026-11-08 docs-only read of the page's source file (ShortCircuitLocalReads.md in the apache/hadoop repo). Removed an unsupported "Verify" metric claim and a "prefer domain-socket" recommendation the page does not state.
