---
id: computing-software.database-administration.neo4j.rbac-privileges
name: rbac-privileges
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, create-role, grant-privilege, deny-privilege, neo4j-rbac, auth-providers, encryption, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Roles and privileges"
sources:
  - https://neo4j.com/docs/operations-manual/current/authentication-authorization/manage-privileges/
  - https://neo4j.com/docs/operations-manual/current/authentication-authorization/manage-users/
  - https://neo4j.com/docs/operations-manual/current/authentication-authorization/property-based-access-control/
  - https://neo4j.com/docs/operations-manual/current/configuration/set-initial-password/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Role-based access control

Goal: control access.
- Example: `CREATE USER ann SET PASSWORD '<PASSWORD>' CHANGE NOT REQUIRED; CREATE ROLE analyst; GRANT MATCH {*} ON GRAPH sales NODES Person TO analyst;`.
- Property-based access control has its own documentation page; check the edition label there before relying on it.
- Set the initial `neo4j` password before the first start with `neo4j-admin dbms set-initial-password`; otherwise it defaults to `neo4j` and must be changed at first login.
Verify: login as ann cannot write.

## Checked

2026-11-02. Confirmed in the Cypher manual access control pages (`CREATE USER ... CHANGE NOT REQUIRED`, `GRANT MATCH {*} ON GRAPH`) and the set-initial-password page. Removed: the claim that property-level privileges are Enterprise only (not confirmed).
Method: documentation only; no commands were run.
