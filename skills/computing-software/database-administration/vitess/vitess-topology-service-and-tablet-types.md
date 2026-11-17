---
id: computing-software.database-administration.vitess.vitess-topology-service-and-tablet-types
name: vitess-topology-service-and-tablet-types
category: computing-software
field: database-administration
product: vitess
tags: [topology-service, etcd, cell, tablet-types, global-topology, local-topology]
level: intro
status: docs-checked
description: "Vitess topology service (global vs per-cell), cells, tablet types, and what keeps serving when topology is unavailable."
sources:
  - https://vitess.io/docs/25.0/concepts/topology-service/
  - https://vitess.io/docs/25.0/concepts/cell/
  - https://vitess.io/docs/25.0/concepts/tablet/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A tablet is one `mysqld` plus its `vttablet`, with a type that sets its role: `primary` (the current MySQL primary; `master` is a deprecated alias), `replica` (eligible for promotion, typically serving live user traffic), `rdonly` (cannot be promoted; used for backups, dumps, analytics and heavy jobs), `backup` (replication stopped at a consistent snapshot to upload a backup, then returns to its previous type), `restore` (started empty and restoring from the latest backup, then becomes replica or rdonly), and `drained` (reserved by a Vitess background process such as resharding).

The topology service is a distributed, consistent key-value store with locking, with plug-in backends; the default plugin is `etcd2`. It lets tablets coordinate, lets Vitess discover tablets for routing, and persists administrator configuration. There is one global topology plus a local topology in each cell.

- Global: keyspaces, shards and each shard's primary tablet alias. Rarely used by design (reparenting and resharding use it). To survive losing a cell, place its nodes in several cells with enough to keep quorum.
- Local: tablets in that cell, the cell's keyspace graph and replication graph.

Local topology must be available for discovery and routing changes, but no topology calls are on the steady-state query path, so queries keep being served during a temporary topology outage.

A cell is a failure-isolated group of servers (a data centre or availability zone). Vitess serves reads only from the local cell; writes go cross-cell to wherever the shard primary lives. Each cell has its own local topology so it can be taken down and rebuilt as a unit.

## Checked

2026-11-08. Read in full: tablet types on the Tablet page; global and local topology, default etcd2 and steady-state behaviour on the Topology Service page; cell semantics on the Cell page. Dropped the Architecture page as a source because no claim relies on it.

Method: documentation only; no commands were run.
