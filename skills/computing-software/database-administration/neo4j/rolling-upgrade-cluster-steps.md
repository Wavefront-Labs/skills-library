---
id: computing-software.database-administration.neo4j.rolling-upgrade-cluster-steps
name: rolling-upgrade-cluster-steps
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, cluster, cordon, deallocate, show-servers, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Take one Neo4j cluster server out of service safely using SHOW SERVERS, cordoning and deallocating, and bring it back with ENABLE SERVER."
sources: ["https://neo4j.com/docs/operations-manual/current/clustering/servers/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rolling restart and server maintenance (cluster)

Goal: change one server at a time without an outage. Enterprise Edition clusters only.
- Check state first: `SHOW SERVERS` on the `system` database. Look at `state` and `health`. `Available` only means other servers can reach it.
- Prevent new databases from being placed on the server with `CALL dbms.cluster.cordonServer('<server-id>')`. It keeps the databases it already hosts. Bring it back with `ENABLE SERVER '<server-id>'`.
- To move its databases away first, use `DRYRUN DEALLOCATE DATABASES FROM SERVER '<id>'`, then the real command. Deallocation fails if the cluster cannot satisfy each database's topology, and is blocked when a hosted database is offline, when the server hosts a database with one primary, or when a primary quorum is cordoned. Deallocating is irreversible. Wait for state `Deallocated` before `DROP SERVER`.
- Reversible alternatives: `dbms.cluster.deallocateDatabaseFromServer("server-name", "database-name")` and related procedures.
- Do not drop a server just for a temporary fault, because that moves all its databases.
- A server that was dropped cannot rejoin until its installation is reset (reinstall, or `neo4j-admin server unbind`).
Verify: `SHOW SERVERS` shows every server `Enabled` and `Available` before you start the next one.

## Checked

2026-11-09. Confirmed against the operations manual Managing servers in a cluster page (docs-operations clustering/servers.adoc): states, SHOW SERVERS columns, cordon and enable commands, DEALLOCATE with DRYRUN and its blocking conditions, DROP SERVER, rejoin note. Removed: the `setAutomaticallyEnableFreeServers` "leader switch" suggestion (that procedure enables free servers, it does not move leaders), "let Raft elect", and "check follower lag in metrics" (not on this page); the upgrade-version steps are not covered by this page and are not claimed.

Method: documentation only; no commands were run.
