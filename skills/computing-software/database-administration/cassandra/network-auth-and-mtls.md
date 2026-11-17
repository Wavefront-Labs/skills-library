---
id: computing-software.database-administration.cassandra.network-auth-and-mtls
name: network-auth-and-mtls
category: computing-software
field: database-administration
product: cassandra
tags: [cassandra, cidr-authorizer, network-authorizer, mutual-tls-auth, nosql, wide-column, cql]
level: practitioner
status: docs-checked
description: "Restricting where roles connect"
sources: ["https://cassandra.apache.org/doc/latest/cassandra/developing/cql/security.html", "https://github.com/apache/cassandra/blob/trunk/conf/cassandra.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network and mTLS authorizers

Goal: restrict connections beyond passwords.
- `CassandraNetworkAuthorizer` (the `network_authorizer` setting in cassandra.yaml) stores permissions in `system_auth.network_permissions`; restrict a role with `ACCESS TO DATACENTERS {'DC1', 'DC3'}` in CREATE ROLE.
- cassandra.yaml documents `MutualTlsAuthenticator` for certificate-based identities.
- With a `cidr_authorizer` configured, roles can be limited with `ACCESS FROM CIDRS {...}` (CIDR groups).
- Combine with firewalls; do not expose the native transport port publicly.
Verify: connection from a disallowed DC or CIDR is refused.

## Checked

2026-11-03. Confirmed against the Apache Cassandra documentation: `ACCESS TO DATACENTERS`, `ACCESS FROM CIDRS`, `network_authorizer`, `MutualTlsAuthenticator` (CQL security page, cassandra.yaml). Removed: the port number 9042 and the version claim about 5.0.

Method: documentation only; no commands were run.
