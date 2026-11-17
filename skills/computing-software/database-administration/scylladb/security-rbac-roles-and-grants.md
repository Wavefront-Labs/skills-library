---
id: computing-software.database-administration.scylladb.security-rbac-roles-and-grants
name: security-rbac-roles-and-grants
category: computing-software
field: database-administration
product: scylladb
tags: [rbac, roles, grant, permissions, least-privilege]
level: practitioner
status: docs-checked
description: "ScyllaDB role-based access control: roles versus users, inheritance, GRANT syntax, resource types, and onboarding or offboarding through roles."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/security/rbac-usecase.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# RBAC: roles, users and grants

Roles generalise users: a role can be granted to another role, which then inherits its permissions. A role that can log in is a user; every user is a role, but not every role is a user. Grant permissions to group-representing roles (for example Guest, Engineer, QA, DB Administrator) rather than to individuals, so access changes do not affect other people.

Build it by creating roles and their permissions, then granting roles to users. Inheritance is hierarchical: a role has the permissions of every role granted to it.

Syntax:
```
GRANT (permission | ALL PERMISSIONS) ON resource TO role;
```
Resources: `<ks>.<tab>` (an unqualified table uses the current keyspace), `KEYSPACE <ks>`, `ALL KEYSPACES`, `ROLE <role>`, `ALL ROLES`. Materialized views and CDC logs cannot be granted separate permissions; they follow the base table.

Example lifecycle:
- New engineer: `CREATE ROLE alice WITH PASSWORD = '<pw>' AND LOGIN = true; GRANT engineer TO alice;` and alice inherits everything the engineer role has.
- Leaves the company: revoke the role or grant a non-employee role such as Guest.
- Changes position: grant the new role and `REVOKE` roles no longer needed.

Roles can also be attached to Service Levels with Workload Prioritization, to allocate resources per role. Start from zero permissions and add the minimum each role needs.

## Checked

2026-11-09. Confirmed roles versus users, inheritance, GRANT syntax and resources, the materialized view and CDC log rule, the onboarding and offboarding flow and Workload Prioritization against the ScyllaDB RBAC page (read in full). The least-privilege advice comes from the security checklist page.

Method: docs-checked 2026-11-09 against the ScyllaDB docs pages operating-scylla/security/rbac-usecase.rst and security-checklist.rst
