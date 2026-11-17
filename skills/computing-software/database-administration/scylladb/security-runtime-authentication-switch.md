---
id: computing-software.database-administration.scylladb.security-runtime-authentication-switch
name: security-runtime-authentication-switch
category: computing-software
field: database-administration
product: scylladb
tags: [authentication, transitionalauthenticator, rolling-restart, zero-downtime, maintenance-socket]
level: advanced
status: docs-checked
description: "Enable or disable ScyllaDB authentication without downtime using com.scylladb.auth.TransitionalAuthenticator as an intermediate state with rolling restarts."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/security/runtime-authentication.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Enable or disable authentication without downtime

The transitional authenticator lets clients with and without credentials work during the migration.

**Enable**
1. On all nodes set in `scylla.yaml`:
```
authenticator: com.scylladb.auth.TransitionalAuthenticator
```
2. On each node run `nodetool drain` and restart, one node at a time.
3. Connect over the maintenance socket and create an authenticated superuser with a strong password:
```
cqlsh /path/to/maintenance/socket/cql.m
CREATE ROLE scylla WITH PASSWORD = '<strong password>' AND LOGIN = true AND SUPERUSER = true;
LIST ROLES;
GRANT scylla TO myuser;
```
4. Roll out credentials to all client applications while the transitional authenticator is still active.
5. Change the setting on all nodes to `authenticator: PasswordAuthenticator` and restart nodes one by one.
6. Verify that all client applications still work with authentication enforced.

**Disable**
1. Change `PasswordAuthenticator` to `com.scylladb.auth.TransitionalAuthenticator` on all nodes and restart one by one.
2. Remove credentials from clients as needed, then switch to `AllowAllAuthenticator` with another rolling restart.
Disabling authentication means you must re-enable it wherever required.

Do not skip the transitional step: moving straight to PasswordAuthenticator breaks unmodified clients immediately.

## Checked

2026-11-09. Confirmed the authenticator values, drain and one-by-one restarts, maintenance socket superuser step, enable and disable sequences and the client warning against the ScyllaDB runtime authentication and authentication pages (read in full).

Method: docs-checked 2026-11-09 against the ScyllaDB docs pages operating-scylla/security/runtime-authentication.rst and authentication.rst
