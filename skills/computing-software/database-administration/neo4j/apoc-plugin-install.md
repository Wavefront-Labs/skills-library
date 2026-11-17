---
id: computing-software.database-administration.neo4j.apoc-plugin-install
name: apoc-plugin-install
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, apoc-core, apoc-extended, plugin-allowlist, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Extending the server"
sources:
  - https://neo4j.com/docs/operations-manual/current/configuration/plugins/
  - https://neo4j.com/docs/operations-manual/current/kubernetes/plugins/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# APOC and plugin installation

Goal: enable APOC.
- APOC Core ships in the `labs` directory (see file locations); copy it into `plugins/` to use it.
- Enable it with `dbms.security.procedures.unrestricted=apoc.*` and `dbms.security.procedures.allowlist=apoc.*`.
- Restrict procedures that can write files or call external URLs (see Securing extensions).
Verify: `RETURN apoc.version()` works.

## Checked

2026-11-02. Confirmed in the plugins page (`apoc.version`, the two settings) and file locations page (`labs` holds APOC Core). Removed: the version-matching claim.
Method: documentation only; no commands were run.
