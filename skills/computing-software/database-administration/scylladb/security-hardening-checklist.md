---
id: computing-software.database-administration.scylladb.security-hardening-checklist
name: security-hardening-checklist
category: computing-software
field: database-administration
product: scylladb
tags: [security, checklist, authentication, authorization, tls, audit]
level: practitioner
status: docs-checked
description: "ScyllaDB security checklist: authentication, authorization, least-privilege RBAC, TLS in transit, encryption at rest, port exposure, auditing and keeping versions patched."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/security/security-checklist.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ScyllaDB security checklist

Work through these areas for every cluster:

1. **Authentication**: require every client to prove identity (set the `authenticator` in `scylla.yaml` to `PasswordAuthenticator`, LDAP via saslauthd, or certificate authentication).
2. **Authorization**: set `authorizer: CassandraAuthorizer` so permissions on keyspaces and tables are checked.
3. **RBAC with least privilege**: define roles per keyspace or table. Start by granting no permissions to any role, then add read only for roles that read and write only for roles that write. More, narrower roles are better than few broad ones.
4. **Encryption in transit**: TLS/SSL for client-to-node (`client_encryption_options`) and node-to-node (`server_encryption_options`). ScyllaDB can run on FIPS-enabled Ubuntu, which uses FIPS 140-2 certified libraries (OpenSSL, GnuTLS) with the kernel in FIPS mode.
5. **Encryption at rest**: protects data persisted in storage or backups and helps meet regulatory requirements.
6. **Reduce network exposure**: run in a trusted network, keep a list of the ports ScyllaDB uses (most are configurable in `scylla.yaml`), monitor them and periodically check that only those ports are open, and only to the relevant IPs. ScyllaDB Manager has its own ports.
7. **Audit**: use the auditing feature to record who did, looked at or changed what and when.
8. **General**: run the latest ScyllaDB version and keep the operating system and libraries updated.

Auditing requires authentication and authorization to be enabled first.

## Checked

2026-11-09. Confirmed each checklist area, the least-privilege advice, FIPS note, port advice and general recommendations against the ScyllaDB security checklist; option names against the client and node encryption pages; authenticator values against the authentication and LDAP pages. Removed the unsupported at-rest detail and the TLS rollout ordering advice.

Method: docs-checked 2026-11-09 against the ScyllaDB docs pages operating-scylla/security/security-checklist.rst, auditing.rst, authentication.rst, client-node-encryption.rst and node-node-encryption.rst
