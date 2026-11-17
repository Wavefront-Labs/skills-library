---
id: computing-software.database-administration.scylladb.procedure-arbiter-dc-and-scale-up
name: procedure-arbiter-dc-and-scale-up
category: computing-software
field: database-administration
product: scylladb
tags: [arbiter-dc, zero-token-nodes, join-ring, quorum, scale-up]
level: advanced
status: docs-checked
description: "Prevent quorum loss in two-DC clusters with a zero-token arbiter DC (join_ring false, RF 0), and upscale a cluster by adding bigger nodes or adding CPUs with scylla_setup."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/cluster-management/arbiter-dc.rst", "https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/procedures/cluster-management/scale-up-cluster.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Arbiter DC and scale-up

**Arbiter DC.** ScyllaDB needs a quorum of nodes to do schema and topology changes; reads and writes of user data continue without it. In a symmetric 2-DC cluster (for example 3 + 3 nodes) losing one DC loses quorum. An arbiter DC holds a zero-token node that stores no data and only takes part in Raft voting, so it costs no storage or replication traffic.

Setup: follow the add-a-DC procedure, but in `scylla.yaml` set `join_ring: false` before first start. On an already bootstrapped node the startup fails; you must decommission, wipe and re-add it. One node is enough; if you add more, set `join_ring=false` on every one. Follow-ups: the arbiter DC has RF 0 for all keyspaces, so ALTER keyspaces accordingly; drivers ignore zero-token nodes, so you can skip configuring clients not to connect to the new DC.

**Upscale.** Bigger machines with fewer nodes are generally better than many small ones. Two options:
1. Add bigger nodes, wait for streaming to finish, remove old smaller nodes, repeat. The cluster is only as strong as its weakest node, so do not overload it until all are upgraded.
2. Add CPUs (whole cluster, sequentially, quorum required): `nodetool drain`, stop, add cores, run `scylla_setup` to adapt to the new hardware, start. Changing the core count makes ScyllaDB reshard SSTables at startup by compacting all data on disk.

## Checked

2026-11-04. Confirmed against arbiter-dc.rst and scale-up-cluster.rst: quorum behaviour, 3 + 3 example, zero-token node, join_ring=false rules, RF 0 follow-ups, driver note, both upscale methods and the resharding note. Nothing removed.

Method: documentation only; no commands were run.
