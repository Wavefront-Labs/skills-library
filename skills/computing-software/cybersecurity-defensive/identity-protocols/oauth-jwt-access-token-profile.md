---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-jwt-access-token-profile
name: oauth-jwt-access-token-profile
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-jwt-access-token-profile, oauth-jwt-access-tokens, rfc9068, at+jwt, jwt-access-token, client_id, scope, jti, identity-protocols]
level: advanced
status: docs-checked
description: "Issue JWT access tokens with typ at+jwt, iss, exp, aud, sub, client_id, iat, jti and scope claims, and signing algorithm rules."
sources:
  - https://www.rfc-editor.org/rfc/rfc9068
  - https://www.rfc-editor.org/rfc/rfc8707
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JWT access token profile (RFC 9068)

Goal: standardise self-contained access tokens.

Required: header `typ: at+jwt` (or `application/at+jwt`), signed (an asymmetric algorithm is RECOMMENDED, `none` is forbidden, and RS256 must be supported); claims `iss`, `exp`, `aud`, `sub`, `client_id`, `iat`, `jti`. Optional: `scope` (space-separated string), `auth_time`, `acr`, `amr`, plus `roles`, `groups`, `entitlements` (SCIM-style values), and `cnf` for DPoP-bound tokens (RFC 9449).

Gotchas:
- `typ` prevents an ID token being accepted as an access token; enforce it at the RS.
- `sub` for a client-credentials token should be an identifier the AS uses for the client application (not necessarily `client_id`).
- Unencrypted JWT access tokens can be read by clients and users: encrypt the token or sensitive claims, omit them, or use opaque tokens (RFC 9068 section 6).
- Resource servers must verify the signature, reject `alg` `none`, and decrypt when encryption was negotiated (section 4).

Verify: decode a token and tick off each required claim.

## Checked

2026-11-02. Confirmed against RFC 9068 sections 2 to 6 (`at+jwt` typ, signing rules, claim list, optional claims, `sub` guidance, privacy) and RFC 9449 (`cnf`). Corrected: `sub` for client credentials is not required to equal `client_id`. Removed: the 5-15 minute lifetime figure and the claim that tokens cannot be revoked.
Method: documentation only; no commands were run.
