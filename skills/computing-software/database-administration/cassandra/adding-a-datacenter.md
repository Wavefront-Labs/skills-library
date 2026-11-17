---
id: computing-software.database-administration.cassandra.adding-a-datacenter
name: adding-a-datacenter
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, add-datacenter, rebuild, nodetool-rebuild, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Multi-DC expansion"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/operating/topo_changes.html", "https://cassandra.apache.org/doc/latest/cassandra/developing/cql/security.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Adding or removing a datacenter

Goal: expand to a new region.
- Start new nodes with `auto_bootstrap: false`; the docs name this hidden parameter as useful when creating a new data-center.
- Add the new DC to each keyspace's replication with `ALTER KEYSPACE ... WITH replication = {'class': 'NetworkTopologyStrategy', ...}`.
- How existing data reaches the new DC is not covered by the pages checked; follow the operations guide for your version.
- Remove nodes with `nodetool decommission`, which streams the node's data out.
Verify: `nodetool netstats` shows streaming progress and the nodes reach UN.

## Checked

2026-11-02. Checked against topo_changes (auto_bootstrap hidden parameter for creating a new data-center, decommission streams data from the decommissioned node, netstats monitoring, UN state) and the system_auth ALTER KEYSPACE NetworkTopologyStrategy example. Removed: the `nodetool rebuild -- <source-dc>` step (nodetool rebuild has no reference page in the docs repo), the advice to move clients to LOCAL_* consistency first, the drop-DC-from-replication ordering, and the `nodetool status` full-load check.

Method: documentation only; no commands were run.
