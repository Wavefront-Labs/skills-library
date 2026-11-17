---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-userinfo-endpoint
name: oidc-userinfo-endpoint
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-userinfo-endpoint, oidc-userinfo-claims, userinfo, bearer, sub-match, claims, endpoint, identity-protocols]
level: practitioner
status: docs-checked
description: "Call the UserInfo endpoint with a bearer token, verify the sub matches the ID token and handle signed or encrypted responses."
sources:
  - https://openid.net/specs/openid-connect-core-1_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# UserInfo endpoint

Goal: fetch profile claims.

Method: GET (recommended) or POST the `userinfo_endpoint` (from discovery) with `Authorization: Bearer <access_token>`, using an access token obtained through OpenID Connect authentication. The response is a JSON object (`application/json`), or a JWT (`application/jwt`) when signing or encryption was registered (for example `userinfo_signed_response_alg`); a signed response contains `iss` and `aud`. `sub` is always returned. Claims returned depend on scopes and any `claims` request; an OP may omit claims without error, and omitted claims should be absent rather than null.

Gotchas:
- The `sub` in the response must exactly match the `sub` in the ID Token; if not, do not use the UserInfo values (token substitution).
- Errors come as `WWW-Authenticate: Bearer error="invalid_token"` with HTTP 401 (RFC 6750 style).
- The endpoint must use TLS and should support CORS for browser clients.
- Verify the OP's TLS certificate; validate the signature of a signed response (should) and decrypt an encrypted one.

Verify: call with a token missing the `profile` scope and confirm the reduced claim set.

## Checked
2026-11-02. Confirmed against OpenID Connect Core 1.0 sections 5.3 and 5.4. Removed: "document which of ID token and UserInfo is authoritative", "large profile data belongs in UserInfo to avoid header size limits" and "cache briefly", none of which Core states.
Method: documentation only; no commands were run.
