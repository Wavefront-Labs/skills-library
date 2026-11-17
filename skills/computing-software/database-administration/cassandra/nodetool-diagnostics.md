---
id: computing-software.database-administration.cassandra.nodetool-diagnostics
name: nodetool-diagnostics
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, nodetool-status, nodetool-info, netstats, nodetool, tablestats, tpstats, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Reading cluster state"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/tools/nodetool/nodetool.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/tools/nodetool/describecluster.html", "https://cassandra.apache.org/doc/latest/cassandra/managing/operating/topo_changes.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nodetool diagnostic commands

Goal: triage with nodetool.
- `status` (node state codes such as UN and DN, where DN is down), `info`, `describecluster`, `netstats`, `compactionstats`, `tablehistograms`, `proxyhistograms`, `gcstats`.
- Connect to a node with `-h <host>`; authenticate with `-u`/`-pw` or `-pwf`.
- Compare nodes to find the outlier.
Verify: you can state load, pending work and schema agreement from the output alone.

## Checked

2026-11-03. Confirmed against the Apache Cassandra documentation: command list and connection options (nodetool reference), `describecluster` printing the schema version. Removed: the UJ/UL codes and the JMX security advice.

Method: documentation only; no commands were run.
