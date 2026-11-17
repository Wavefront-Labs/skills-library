---
id: computing-software.database-administration.scylladb.security-enable-authorization
name: security-enable-authorization
category: computing-software
field: database-administration
product: scylladb
tags: [authorization]
level: practitioner
status: docs-checked
description: "Enable ScyllaDB authorization with CassandraAuthorizer: whitelist permission model, superuser first, then roles and GRANT statements."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/security/enable-authorization.rst", "https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/security/rbac-usecase.rst", "https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/security/security-checklist.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Enable authorization

Authorization is internal and set by the `authorizer` option in `scylla.yaml`. Authentication must already be enabled (see enable authentication).
- `AllowAllAuthorizer` (default): no checks, grants all permissions to all roles. Required if `AllowAllAuthenticator` is the authenticator.
- `CassandraAuthorizer`: manages permissions and stores them in system tables.

Permissions are a whitelist: a role has no access to any resource unless granted. Once enabled on a node, all requests are rejected until the required permissions are granted, so do the initial setup on a node that is not serving client traffic. All users must then connect with a user and password.

Procedure:
1. On the chosen node, set `authorizer: CassandraAuthorizer` and restart it.
2. Create a superuser first (none exists by default).
3. Log in as the superuser (`cqlsh -u dba`) and create roles and grants, for example:
```
CREATE ROLE db_user WITH PASSWORD = '<password>' AND LOGIN = true;
CREATE ROLE client;
GRANT SELECT ON ks.t1 TO client;
GRANT client TO db_user;
```
4. Restart the remaining nodes; permissions are enforced as each node restarts and clients reconnect. Confirm each user can connect with the new credentials.
5. To remove a permission from a role or user, use `REVOKE`.

Role design (RBAC): set roles per keyspace or table, start by granting nothing, then grant `SELECT` to roles that read and `MODIFY` to roles that write. Assign roles to users with `GRANT <role> TO <user>`. A more detailed example is in the RBAC skill.

## Checked

2026-11-09. Confirmed authorizer values, whitelist behaviour, node preparation advice, superuser requirement, example grants, restart behaviour and REVOKE against the ScyllaDB enable-authorization page; role-design advice against the RBAC and security checklist pages (all read in full). Replaced the keyspace-level example with the page's own example, replaced the unrelated garbage sources, and rewrote the description.

Method: docs-checked 2026-11-09 against the ScyllaDB docs pages operating-scylla/security/enable-authorization.rst, rbac-usecase.rst and security-checklist.rst
