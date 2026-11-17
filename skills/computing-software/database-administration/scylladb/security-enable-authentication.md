---
id: computing-software.database-administration.scylladb.security-enable-authentication
name: security-enable-authentication
category: computing-software
field: database-administration
product: scylladb
tags: [authentication, passwordauthenticator, scylla-yaml, maintenance-socket, superuser]
level: practitioner
status: docs-checked
description: "Enable ScyllaDB password authentication with PasswordAuthenticator, create the first superuser via the maintenance socket, and note client downtime."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/security/authentication.rst", "https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/security/create-superuser.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Enable authentication and create a superuser

Authentication is internal to ScyllaDB (users and passwords are kept in ScyllaDB itself). The plain procedure suits clusters without running applications: once enabled, every client (all drivers) stops working until reconfigured with credentials. If that downtime is not acceptable use the runtime procedure (see the runtime authentication skill).

1. On each node edit `/etc/scylla/scylla.yaml`:
```
authenticator: PasswordAuthenticator
```
(the default is `AllowAllAuthenticator`).
2. Restart ScyllaDB.
3. Create a superuser. There is no default superuser role. On a new cluster use the maintenance socket (it must be enabled on the node):
```
cqlsh <maintenance_socket_path>
CREATE ROLE <new_superuser> WITH SUPERUSER = true AND LOGIN = true AND PASSWORD = '<password>';
```
Use the socket path configured in `scylla.yaml`. Then check login with `cqlsh -u <new_superuser>` and `LIST ROLES;`.
4. With an existing superuser you can alternatively log in with `cqlsh -u <existing_superuser>` and run the same `CREATE ROLE`.

Superusers have full access and can run any CQL command, so create a named superuser for yourself and keep the credentials in a secret manager. Next step: authorization (roles and permissions) and, optionally, LDAP or certificate authenticators.

## Checked

2026-11-09. Confirmed the authenticator change, restart, client downtime warning, absence of a default superuser, maintenance socket procedure and verification steps against the ScyllaDB authentication and superuser pages (both read in full).

Method: docs-checked 2026-11-09 against the ScyllaDB docs pages operating-scylla/security/authentication.rst and create-superuser.rst
