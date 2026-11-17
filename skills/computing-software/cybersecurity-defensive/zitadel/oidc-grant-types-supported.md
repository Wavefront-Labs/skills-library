---
id: computing-software.cybersecurity-defensive.zitadel.oidc-grant-types-supported
name: oidc-grant-types-supported
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, oauth, grant-types, pkce, device-authorization, token-exchange]
level: intro
status: docs-checked
description: "See which OAuth 2.0 and OIDC grant types ZITADEL supports and which it deliberately does not, such as password credentials."
sources:
  - https://zitadel.com/docs/apis/openidoauth/grant-types
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
ZITADEL's supported grant types:

- Authorization Code: yes
- Authorization Code with PKCE: yes
- Client Credentials: yes
- Device Authorization: yes
- Implicit: yes
- JSON Web Token (JWT) Profile: yes
- Refresh Token: yes
- Token Exchange: yes
- Resource Owner Password Credentials: no
- SAML 2.0 Profile: no

The password grant is not supported: the page says this is due to growing security concerns and that OAuth 2.1 looks like it will remove the grant.

The specifications behind the grants are RFC 6749 (authorization code, implicit, client credentials, refresh token), RFC 7636 (PKCE), RFC 7523 (JWT profile), RFC 8693 (token exchange) and RFC 8628 (device authorization).

The JWT profile is how service accounts authenticate with a downloaded key: create or use a service account, create a key and download it, generate a JWT signed with that key, send the JWT Base64 encoded to the token endpoint, and use the access token you receive. The JWT needs `iss`, `sub`, `aud` (which must include ZITADEL's issuing domain), `exp` and `iat` (not older than 1 hour), plus a `kid` header carrying the `keyId` from the key JSON.

## Checked

2026-11-08. Confirmed against the Grant Types page (source mdx in the zitadel repo): the support table, the spec links, the JWT profile steps and claim requirements, and the password grant note. Removed: the practical-choices list, the claim about refresh tokens needing offline_access on this page, and the MFA and lockout remark, none of which the page states.

Method: documentation only; no commands were run.
