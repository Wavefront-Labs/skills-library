---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-jwt-introspection-response
name: oauth-jwt-introspection-response
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-jwt-introspection-response, oauth-introspection-revocation, rfc9701, introspection-jwt, signed-introspection, token-introspection+jwt, identity-protocols]
level: sme
status: docs-checked
description: "Request signed JWT introspection responses (RFC 9701) with application/token-introspection+jwt, and validate iss, aud, iat and the token_introspection claim."
sources:
  - https://www.rfc-editor.org/rfc/rfc9701
  - https://www.rfc-editor.org/rfc/rfc7662
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JWT introspection responses

Goal: get an integrity-protected introspection answer.

Method (RFC 9701, "JSON Web Token (JWT) Response for OAuth Token Introspection"): the RS sends the introspection request with `Accept: application/token-introspection+jwt`. The endpoint responds with that content type and a JWT whose `typ` header is `token-introspection+jwt`. The JWT MUST include `iss` (issuer URL of the authorization server), `iat`, `aud` and a `token_introspection` claim that holds the normal introspection response members. If the token is invalid, expired, revoked or not intended for the calling RS, `active` in `token_introspection` MUST be false and no other members are included. The RS verifies the JWT signature and checks that `aud` identifies itself.

Gotchas:
- The AS MUST authenticate the caller at the introspection endpoint and MUST be able to determine whether the RS is the audience of the token.
- Client metadata `introspection_signed_response_alg` selects the signing algorithm (default RS256 when omitted).
- The JWT SHOULD NOT include `sub` and `exp`, to prevent misuse of the introspection JWT as an access token; do not use `exp` of this JWT as a caching hint.

Verify: decode the JWT and confirm `aud` equals the RS identifier.

## Checked

Date: 2026-11-02. Confirmed in RFC 9701 (now an RFC, not a draft) and RFC 7662 as cited above. Removed as not stated there: FAPI message-signing and "regulated deployments" advice, "plain JSON is fine in a trusted network", caching by `exp`/`iat`, and the earlier RFC 7009 source (revocation).

Method: documentation only; no commands were run.
