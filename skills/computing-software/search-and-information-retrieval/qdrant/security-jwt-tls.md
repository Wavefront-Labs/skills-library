---
id: computing-software.search-and-information-retrieval.qdrant.security-jwt-tls
name: security-jwt-tls
category: computing-software
field: search-and-information-retrieval
product: qdrant
tags: [jwt-rbac, tls, verify-client-certificate, access-control, sec-jwt-tls]
level: advanced
status: docs-checked
description: "Grant granular access with JWT RBAC and encrypt traffic with TLS, optionally verifying client certificates."
sources:
  - "https://qdrant.tech/documentation/production-operations/access-control/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Role-based access control uses JWTs signed with the API key. Enable it:

```yaml
service:
  api_key: <secret>
  jwt_rbac: true
```

A token carries claims describing what the holder may do, such as read or write on specific collections, so applications and users get only the access they need. The access-control guide shows how to build the claims, including restricting a token to one collection and attaching payload filters.

TLS settings:

```yaml
service:
  enable_tls: true
tls:
  cert: ./tls/cert.pem
  key: ./tls/key.pem
  ca_cert: ./tls/cacert.pem
  verify_https_client_certificate: true
```

`verify_https_client_certificate` requires clients to present a certificate signed by the CA. Cluster internal traffic can use TLS too, and from v1.20.0 the API key is enforced on the internal port by default.

Tokens are signed with the admin `api_key`, so anyone who knows that key can authorize a token, and JWTs must be re-created after the key is switched. The `exp` claim is a Unix timestamp in seconds, checked with 30 seconds of leeway.

## Checked

2026-11-03. Confirmed on the Qdrant security and access-control pages: `jwt_rbac: true`, tokens signed with the `api_key`, `exp` semantics, the TLS settings block, `verify_https_client_certificate`, internal authentication enforced by default from v1.20.0. Removed the unconfirmed design advice and testing tip.

Method: documentation only; no commands were run.
