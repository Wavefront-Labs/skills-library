---
id: computing-software.cybersecurity-defensive.zitadel.client-authentication-methods
name: client-authentication-methods
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, client-authentication, client-secret-basic, private-key-jwt, oidc]
level: advanced
status: docs-checked
description: "Build client_secret_basic headers and private_key_jwt assertions for ZITADEL's token and introspection endpoints."
sources:
  - https://zitadel.com/docs/apis/openidoauth/authn-methods
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Client secret basic: send an `Authorization` header with `Basic ` followed by the base64 of the form-URL-encoded client id, a colon and the form-URL-encoded client secret. Encode each part before joining, because client ids can contain characters such as `@` that must be encoded.

Private key JWT (`urn:ietf:params:oauth:client-assertion-type:jwt-bearer`): download the application key. The JSON holds `type` (`application`), `keyId`, `key` (the RSA private key, which cannot be regenerated), `clientId` and `appId`. Build a JWT with these claims:

- `iss` and `sub`: the `clientId`
- `aud`: must include ZITADEL's issuing domain
- `exp`: expiry as a Unix timestamp
- `iat`: signing time, which must not be older than one hour

Put `kid` set to the `keyId` in the JWT header, with `alg` RS256, so ZITADEL can identify the key. Send the signed JWT as `client_assertion`, with `client_assertion_type` set to the value above.

Store the downloaded key in a secrets manager at once. The private key is returned only when generated, so losing it means creating a new key.

The same two methods apply to the introspection endpoint. Private key JWT is the recommended way to authenticate an API calling introspection.

## Checked
2026-11-08. Confirmed against the ZITADEL authentication methods page (Basic header construction, key JSON fields, JWT claims, one-hour iat limit, kid header, RS256) and the token introspection guide (JWT profile recommended). Fixed the source URL list.
Method: documentation only; no commands were run.
