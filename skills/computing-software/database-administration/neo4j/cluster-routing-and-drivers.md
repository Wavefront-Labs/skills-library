---
id: computing-software.database-administration.neo4j.cluster-routing-and-drivers
name: cluster-routing-and-drivers
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, bolt-routing, causal-clustering, bookmarks, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Client behaviour"
sources: ["https://neo4j.com/docs/operations-manual/current/clustering/setup/routing/", "https://neo4j.com/docs/python-manual/current/connect-advanced/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Routing and causal consistency

Goal: route client traffic correctly.
- Write transactions are always routed to the leader of the target database; with the default configuration the other servers act as readers.
- Client-side routing uses a routing table from `dbms.routing.getRoutingTable()`; drivers fetch it on first connect and refresh it after its time-to-live or when it looks stale.
- Drivers accept the schemes `neo4j`, `neo4j+s`, `neo4j+ssc`, `bolt`, `bolt+s`, `bolt+ssc`; the scheme must match the server's requirements. Cypher Shell connects to a cluster member with `-a neo4j://<member>:<bolt-port>`.
- A bookmark lets a client read its own writes: only servers that have a copy of the bookmark may respond.
Verify: a read in a new session using the previous session's bookmark sees the earlier write.

## Checked

2026-11-02. Confirmed in the Leadership, routing and load balancing page, the Python driver connection page, the Cypher Shell page and the clustering glossary (bookmark). Removed: 'prefer neo4j:// over bolt://' wording.
Method: documentation only; no commands were run.
