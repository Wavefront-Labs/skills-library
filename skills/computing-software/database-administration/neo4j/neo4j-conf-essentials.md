---
id: computing-software.database-administration.neo4j.neo4j-conf-essentials
name: neo4j-conf-essentials
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, neo4j-conf-settings, server-bolt-listen-address, default-database, neo4j-install, neo4j-conf, memory-configuration, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Core settings"
sources:
  - https://neo4j.com/docs/operations-manual/current/configuration/configuration-settings/
  - https://neo4j.com/docs/operations-manual/current/docker/configuration/
  - https://neo4j.com/docs/operations-manual/current/configuration/neo4j-conf/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# neo4j.conf essentials

Goal: configure a server.
- Settings live in `neo4j.conf`; the settings reference lists `server.default_listen_address`, `server.bolt.advertised_address`, `server.directories.data` and `dbms.security.auth_enabled`.
- Set `server.jvm.additional` for extra JVM flags.
- In Docker, settings are overridden by `NEO4J_` environment variables (see neo4j-docker-run).
- `neo4j-admin server validate-config` validates the Neo4j and Log4j configuration.
Verify: `neo4j console` starts and Bolt answers on 7687.

## Checked

2026-11-02. Confirmed in the Operations Manual configuration settings reference (the four setting names, `server.jvm.additional`), the `neo4j-admin server validate-config` page and the neo4j-admin tools table (`neo4j console`). Removed: the 4.x-name remark and the "confirm" hedges.
Method: documentation only; no commands were run.
