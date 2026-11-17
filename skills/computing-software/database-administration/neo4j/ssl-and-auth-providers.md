---
id: computing-software.database-administration.neo4j.ssl-and-auth-providers
name: ssl-and-auth-providers
category: computing-software
field: database-administration
product: neo4j
tags: [neo4j, ssl-policy, ldap-auth, oidc-sso, graph-database, cypher, nosql]
level: practitioner
status: docs-checked
description: "Securing transport"
sources: ["https://neo4j.com/docs/operations-manual/current/security/ssl-framework/", "https://neo4j.com/docs/operations-manual/current/authentication-authorization/ldap-integration/", "https://neo4j.com/docs/operations-manual/current/authentication-authorization/sso-integration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TLS and external auth providers

Goal: secure connections.
- SSL policies are set per scope, including `bolt` (port 7687), `https` (7473) and `cluster` (6000, 7000, 7688).
- Certificates must be X.509 and PEM-encoded and issued by a CA; the default `base_directory` is `certificates/<scope>`, for example `dbms.ssl.policy.bolt.base_directory=certificates/bolt`.
- LDAP integration and OpenID Connect (OIDC) single sign-on (for example Okta, Microsoft Entra ID, Google) are Enterprise Edition features.
Verify: `cypher-shell -a neo4j+s://<host>` connects with a CA-signed certificate.

## Checked

2026-11-02. Confirmed in the SSL framework page, LDAP integration page (Enterprise Edition) and SSO integration page. Removed: 'disable the HTTP port' and 'plain bolt fails' (not on those pages).
Method: documentation only; no commands were run.
