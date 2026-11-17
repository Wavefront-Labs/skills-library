---
id: computing-software.cybersecurity-defensive.keycloak.rpt-token-introspection
name: rpt-token-introspection
category: computing-software
field: cybersecurity-defensive
product: keycloak
tags: [cybersecurity-defensive, keycloak, rpt, token-introspection, authorization-services, resource-server]
level: practitioner
status: docs-checked
description: "Introspect a Keycloak RPT at the token introspect endpoint to enforce authorization decisions in a resource server without a built-in enforcer."
sources:
  - https://github.com/keycloak/keycloak/blob/main/docs/documentation/authorization_services/topics/service-rpt-token-introspection.adoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rpt token introspection
Introspect a requesting party token (RPT) to check its validity or obtain its permissions. Two use cases from the docs: client applications that need to know whether a token is valid before obtaining a new one with the same or additional permissions, and resource servers enforcing decisions themselves when no built-in policy enforcer fits.

The endpoint is an OAuth2 token introspection-compliant endpoint:
```
POST /realms/<realm>/protocol/openid-connect/token/introspect
Authorization: Basic <client id and secret>
Content-Type: application/x-www-form-urlencoded

token_type_hint=requesting_party_token&token=${RPT}
```
The docs example authenticates with HTTP Basic client credentials but any client authentication method supported by Keycloak can be used. Parameters: `token_type_hint` (use `requesting_party_token`) and `token` (the token string as returned during authorization). The response for an active RPT includes a `permissions` array (`resource_id`, `resource_name`), `exp`, `nbf`, `iat`, `aud` and `"active": true`; an inactive RPT returns `{"active": false}`.

You do not have to call the server every time: RPTs are JWTs, so you can decode and validate them locally, as the policy enforcers do. Validate the signature (realm public key) and check validity with the `exp`, `iat` and `aud` claims, then use the permissions in the token.

## Checked
2026-11-03. Confirmed against authorization_services/topics/service-rpt-token-introspection.adoc. Removed (not on the page): the revocation/short-lifetime rationale, caching and logging gotchas, and the Verify step.
Method: documentation only; no commands were run.
