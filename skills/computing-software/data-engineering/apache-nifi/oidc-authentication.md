---
id: computing-software.data-engineering.apache-nifi.oidc-authentication
name: oidc-authentication
category: computing-software
field: data-engineering
product: apache-nifi
tags: [data-engineering, apache-nifi, openid-connect, oidc, sso, authentication, nifi-properties]
level: practitioner
status: docs-checked
description: "OpenID Connect login for NiFi: discovery URL, client id and secret, claims for user and groups, scopes, timeouts, JWS algorithm and truststore strategy."
sources:
  - https://nifi.apache.org/docs/nifi-docs/html/administration-guide.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OpenID Connect in nifi.properties

- `nifi.security.user.oidc.discovery.url`, `.client.id`, `.client.secret` (the table lists no defaults).
- `nifi.security.user.oidc.connect.timeout` and `.read.timeout`: 5 secs.
- `nifi.security.user.oidc.preferred.jwsalgorithm`: blank means RS256.
- `nifi.security.user.oidc.additional.scopes`: added to `openid` and `email`; include `offline_access` to get refresh tokens.
- `nifi.security.user.oidc.claim.identifying.user`: `email`; `.fallback.claims.identifying.user` for alternates.
- `nifi.security.user.oidc.claim.groups`: `groups`.
- `nifi.security.user.oidc.truststore.strategy`: `JDK` (or `NIFI`).
- `nifi.security.user.oidc.token.refresh.window`: 60 secs.

Group names from the ID token claim are used for authorization only when a User Group Provider supplies groups with matching names.

Verify: the login page redirects to the IdP and returns with the user identified by the configured claim.

## Checked

Checked against the NiFi Administration Guide, OpenID Connect property table: keys, 5 sec timeouts, RS256 for a blank JWS algorithm, default scopes `openid` and `email` plus `offline_access` for refresh tokens, claim defaults (`email`, `groups`), truststore strategy `JDK` and the 60 sec refresh window match. Reworded the authorization sentence to the page's group-claim statement.

Method: docs-only read of cited pages, 2026-11-08
