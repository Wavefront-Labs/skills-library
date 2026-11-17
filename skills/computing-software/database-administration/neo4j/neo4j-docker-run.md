---
id: computing-software.database-administration.neo4j.neo4j-docker-run
name: neo4j-docker-run
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, docker-neo4j, neo4j-auth-env, volume-mounts, neo4j-docker, helm-neo4j, neo4j-kubernetes, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Container deployment"
sources:
  - https://neo4j.com/docs/operations-manual/current/docker/introduction/
  - https://neo4j.com/docs/operations-manual/current/docker/configuration/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running Neo4j in Docker

Goal: run a containerised instance.
- Example: `docker run -p 7474:7474 -p 7687:7687 -v data:/data -e NEO4J_AUTH=neo4j/<PASSWORD> neo4j:5`.
- Enterprise Edition needs `NEO4J_ACCEPT_LICENSE_AGREEMENT=yes`.
- Config via `NEO4J_` variables: dots become single underscores and each underscore in a setting name is written twice, for example `NEO4J_server_memory_heap_max__size`.
- The default memory assignments in the image are small (512M heap and page cache), so set both for real workloads.
Verify: browser at 7474 connects.

## Checked

2026-11-02. Confirmed in the Docker introduction (licence variable) and Docker configuration pages (`NEO4J_server_memory_heap_max__size`, doubled underscores, 512M defaults, `NEO4J_AUTH`). Removed: the mount list for /logs and /plugins (not read on the pages checked).
Method: documentation only; no commands were run.
