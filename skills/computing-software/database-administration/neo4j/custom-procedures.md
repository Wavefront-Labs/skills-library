---
id: computing-software.database-administration.neo4j.custom-procedures
name: custom-procedures
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, procedure-jar, unrestricted-procedures, allowlist, user-defined-procedures, java-extension, sandboxing, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Write, test and deploy Neo4j user-defined procedures and functions as a jar in plugins, with the unrestricted and allowlist settings."
sources: ["https://neo4j.com/docs/java-reference/current/extending-neo4j/procedures-and-functions/", "https://neo4j.com/docs/operations-manual/current/configuration/plugins/", "https://neo4j.com/docs/operations-manual/current/procedures/show-procedures/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom procedures and functions

Goal: extend the server safely.
- Write Java classes with `@Procedure` methods (procedures) or `@UserFunction` methods (read-only functions returning one value). Procedures that must run on the system database also need `@SystemProcedure`.
- Test with Neo4j Harness and JUnit: start an in-process server with `Neo4jBuilders.newInProcessBuilder().withProcedure(...)` and run queries over Bolt.
- Package a jar and put it in the `plugins` directory. In a cluster, install it on each server. Installed plugins load at every start, so keep the set small.
- Allow it in `neo4j.conf`: add the procedure namespace to `dbms.security.procedures.unrestricted` where it needs unrestricted access, and to `dbms.security.procedures.allowlist` if that setting is in use (by default all procedures are loaded).
- To pick up a replaced jar without a restart, call `dbms.reloadProcedures()`; an invalid jar makes the reload fail and the previously loaded plugins keep serving.
Verify: `SHOW PROCEDURES` lists the extension (use `YIELD name` and a `WHERE` filter).

## Checked

2026-11-09. Confirmed against the Java Reference page on user-defined procedures and functions (docs-java-reference), the operations manual Configure plugins page and the SHOW PROCEDURES page (docs-operations). Removed: the draft disclaimer and nothing else; added the harness builder, system-procedure annotation, per-server install, and reload behaviour from the pages.

Method: documentation only; no commands were run.
