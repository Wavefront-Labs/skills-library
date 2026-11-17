---
id: computing-software.database-administration.neo4j.cluster-server-lifecycle
name: cluster-server-lifecycle
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, enable-server, deallocate-database, drop-server, rolling-upgrade-cluster, server-drain, cordon-server, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Managing members"
sources: ["https://neo4j.com/docs/operations-manual/current/clustering/servers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Server lifecycle in a cluster

Goal: add and remove servers.
- `SHOW SERVERS` lists servers; the `state` column is one of Free, Enabled, Cordoned, Deallocating, Deallocated or Dropped. A new server starts Free and is added with `ENABLE SERVER 'serverId'`.
- Cordon a server (it keeps its databases but gets no new ones) with `CALL dbms.cluster.cordonServer('<id>')`; return it with `ENABLE SERVER`.
- `DEALLOCATE DATABASE[S] FROM SERVER[S] 'name'` moves databases off a server. It is prevented when a hosted database is offline, when the server holds a database with one primary allocation, or when a quorum of primaries is cordoned.
- Once a server is deallocated and hosts only the system database, `DROP SERVER '<id>'` removes it.
- `REALLOCATE DATABASES` rebalances databases across the servers; `CREATE DATABASE` allocates on its own and needs no reallocate.
- A permanently failed server shows `Unavailable` in the health column; cordon a temporarily failed one rather than dropping it.
Verify: `SHOW SERVERS` shows the expected states and every database keeps its primaries.

## Checked

2026-11-02. Confirmed in the Managing servers in a cluster page (syntax, states, deallocation limits, drop, error handling) and the databases page (reallocate). Removed: the '5.x' version note and the Raft-majority line (not on those pages).
Method: documentation only; no commands were run.
