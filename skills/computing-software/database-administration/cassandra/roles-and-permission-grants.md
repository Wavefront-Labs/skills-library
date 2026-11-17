---
id: computing-software.database-administration.cassandra.roles-and-permission-grants
name: roles-and-permission-grants
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, role-hierarchy, grant-permission, resource-hierarchy, grant-revoke, list-permissions, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Permissions model"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/developing/cql/security.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Roles, grants and resource scopes

Goal: design role structure.
- Permissions: `CREATE`, `ALTER`, `DROP`, `SELECT`, `MODIFY`, `AUTHORIZE`, `DESCRIBE`, `EXECUTE`, plus `UNMASK` and `SELECT_MASKED`; not every permission applies to every resource.
- Resource hierarchies: `ALL KEYSPACES` -> `KEYSPACE` -> `TABLE`; `ALL FUNCTIONS` -> `KEYSPACE` -> `FUNCTION`; `ALL ROLES` -> `ROLE`; `ALL MBEANS` -> `MBEAN`. A grant flows down the hierarchy.
- Roles can be granted to roles (`GRANT ROLE report_writer TO alice`); the grantee acquires the role's permissions.
- Permission changes are visible to existing sessions.
Verify: `LIST ROLES` and `LIST ALL PERMISSIONS` match the design.

## Checked

2026-11-02. Checked against the CQL security page (permission list, resource hierarchies, GRANT ROLE, permissions visible to existing sessions). Removed: the 'superuser is global, keep few' remark and the exact LIST statement text (not confirmed).

Method: documentation only; no commands were run.
