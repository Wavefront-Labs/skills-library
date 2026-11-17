---
id: computing-software.database-administration.cassandra.authentication-authorization
name: authentication-authorization
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, password-authenticator, cassandra-authorizer, create-role, cassandra-security, roles, tls-encryption, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Roles and permissions"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/managing/operating/security.html", "https://cassandra.apache.org/doc/latest/cassandra/developing/cql/security.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authentication and authorization

Goal: lock down access.
- `authenticator: PasswordAuthenticator`, `authorizer: CassandraAuthorizer`, `role_manager: CassandraRoleManager`; the defaults are `AllowAllAuthenticator` and `AllowAllAuthorizer`.
- The default `cassandra` superuser has password `cassandra`: create another superuser, log in as it, then `ALTER ROLE cassandra WITH SUPERUSER = false AND LOGIN = false;`.
- `CREATE ROLE dba WITH SUPERUSER = true AND LOGIN = true AND PASSWORD = '<PASSWORD>';` is the documented form; grant permissions with `GRANT SELECT ON ALL KEYSPACES TO data_reader;` or `GRANT MODIFY ON KEYSPACE keyspace1 TO data_writer;`.
- Raise the `system_auth` keyspace replication, for example `ALTER KEYSPACE system_auth WITH replication = {'class': 'NetworkTopologyStrategy', 'DC1': 3, 'DC2': 3};`.
Verify: the app role logs in and is denied outside its grants.

## Checked

2026-11-02. Checked against security (managing) and CQL security: AllowAllAuthenticator/AllowAllAuthorizer defaults, PasswordAuthenticator, CassandraAuthorizer, CassandraRoleManager, default cassandra superuser and password, create-another-superuser then ALTER ROLE cassandra procedure, system_auth ALTER KEYSPACE example, GRANT examples. Removed: the `roles_validity` and `permissions_validity` tuning advice (not stated in the pages).

Method: documentation only; no commands were run.
