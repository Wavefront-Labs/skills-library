---
id: computing-software.database-administration.neo4j.cluster-topology-setup
name: cluster-topology-setup
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, cluster-discovery, primary-servers, secondary-servers, neo4j-cluster, primaries-secondaries, raft, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Enterprise cluster"
sources:
  - https://neo4j.com/docs/operations-manual/current/clustering/setup/discovery/
  - https://neo4j.com/docs/operations-manual/current/clustering/databases/
  - https://neo4j.com/docs/operations-manual/current/configuration/configuration-settings/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cluster topology and discovery

Goal: understand cluster topology and discovery.
- Discovery uses `dbms.cluster.endpoints` (a list of server addresses with cluster port, for example `server01.example.com:6000`), or a single DNS name with port 0.
- A database topology is set at creation: `CREATE DATABASE foo TOPOLOGY 3 PRIMARIES 2 SECONDARIES`.
- `server.cluster.system_database_mode` sets a server's mode for the system database.
Verify: `SHOW SERVERS` and `SHOW DATABASES` show hosted roles.

## Checked

2026-11-02. Confirmed in the clustering discovery and databases pages (`dbms.cluster.endpoints`, `TOPOLOGY 3 PRIMARIES 2 SECONDARIES`, `server.cluster.system_database_mode`). Removed: `dbms.cluster.discovery.endpoints` (only a removed 5.x setting appears in breaking changes), the odd-primaries rule, and the Raft description.
Method: documentation only; no commands were run.
