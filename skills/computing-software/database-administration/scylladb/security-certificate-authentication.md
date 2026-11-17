---
id: computing-software.database-administration.scylladb.security-certificate-authentication
name: security-certificate-authentication
category: computing-software
field: database-administration
product: scylladb
tags: [certificate-authentication]
level: advanced
status: docs-checked
description: "ScyllaDB certificate authentication: CertificateAuthenticator, require_client_auth TLS and auth_certificate_role_queries regexes mapping certs to roles."
sources: ["https://github.com/scylladb/scylladb/blob/master/docs/operating-scylla/security/certificate-authentication.rst"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Certificate-based authentication

Instead of user/password pairs, ScyllaDB maps the verified client certificate Subject or Alt information to a defined role.

1. Enable authentication and define the authorised roles as in the authentication procedure.
2. Enable CQL TLS with client certificate verification on each node:
```
client_encryption_options:
    enabled: True
    certificate: <server cert>
    keyfile: <server key>
    truststore: <shared trust>
    require_client_auth: True
```
Issue each client certificate so it designates the intended login role; typically the subject common name equals the role name. All client certificates must be verifiable by system trust or the configured truststore.
3. Configure the authenticator on each node:
```
authenticator: com.scylladb.auth.CertificateAuthenticator
auth_certificate_role_queries:
  - source: SUBJECT
    query: CN=([^,\s]+)
```
Each query is a regular expression with a single match group. `source` is `SUBJECT` (the distinguished name) or `ALTNAME` (subject extensions). Several expressions can be listed; the first match is used.
4. Restart the cluster.

Combine with the authorization skill so each role has only the permissions it needs.

## Checked

2026-11-09. Confirmed the three configuration steps, option values, source types, first-match rule and restart against the ScyllaDB certificate-based authentication page (read in full). Removed the unsupported claim about unmatched certificates and the example role statement, replaced the unrelated garbage sources, and rewrote the description.

Method: docs-checked 2026-11-09 against the ScyllaDB docs page operating-scylla/security/certificate-authentication.rst
