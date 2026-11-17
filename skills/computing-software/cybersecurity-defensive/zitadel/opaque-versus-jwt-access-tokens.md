---
id: computing-software.cybersecurity-defensive.zitadel.opaque-versus-jwt-access-tokens
name: opaque-versus-jwt-access-tokens
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, opaque-tokens, jwt, access-token, token-validation]
level: intro
status: docs-checked
description: "Compare ZITADEL's default opaque access tokens with JWTs and decide how your API should validate them."
sources:
  - https://zitadel.com/docs/concepts/knowledge/opaque-tokens
  - https://zitadel.com/docs/guides/integrate/token-introspection
  - https://zitadel.com/docs/guides/integrate/service-accounts/client-credentials
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Opaque tokens are the default token type in ZITADEL. Unlike a self-contained JWT they do not reveal user information. They are references to session data held on the authorization server.

Flow: ZITADEL generates a unique opaque token tied to the user's session, the client presents it with requests, and the resource server calls ZITADEL to validate it and learn about the session.

Documented benefits:

- Less exposure: nothing sensitive is readable from the token.
- Server-side control: validation happens at the authorization server, which gives administrators control and monitoring.
- Protection against tampering with token contents.

JWTs can be verified locally with public keys (see the JWKS skill), which can be faster and more scalable but needs key distribution and management. Opaque tokens always need a call to the authorization server. The introspection endpoint validates either type and ensures the token is not revoked.

You do not need to decide in the API. A client may send either type, and the API simply introspects.

Client credentials tokens for service accounts are opaque by default.

## Checked

2026-11-08. Read in full: the opaque tokens concept page, the token introspection overview and the client credentials guide. Replaced the unsupported revocation detail with what the pages state; removed the advice on when local validation is acceptable.

Method: documentation only; no commands were run.
