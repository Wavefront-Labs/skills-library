---
id: computing-software.cybersecurity-defensive.identity-protocols.fapi2-security-profile
name: fapi2-security-profile
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [fapi2-security-profile, fapi2, fapi, open-banking, par, pkce, sender-constrained, identity-protocols]
level: sme
status: docs-checked
description: "Implement the FAPI Security Profile 2.0 final: code flow with PAR, PKCE S256, sender-constrained tokens, private_key_jwt or mTLS, algorithm limits."
sources:
  - https://openid.net/specs/fapi-security-profile-2_0.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# FAPI Security Profile 2.0 requirements

Goal: meet the high-assurance API profile used in open banking. The spec is titled "FAPI Security Profile 2.0" (Final, 22 February 2025); the old URL fapi-2_0-security-profile.html now only redirects to it.

Authorization server (section 5.3.2):
- Only confidential clients; reject the resource owner password credentials grant.
- Only issue sender-constrained access tokens, using MTLS (RFC 8705) or DPoP (RFC 9449). With DPoP it must support authorization code binding to the DPoP key.
- Authenticate clients with MTLS (RFC 8705 section 2) or `private_key_jwt` (OIDC Core section 9).
- Require `response_type=code`; reject authorization requests not sent via PAR (RFC 9126); reject PAR requests without client authentication; require `redirect_uri` in PAR requests.
- Require PKCE (RFC 7636) with `S256`.
- Return the `iss` response parameter (RFC 9207); authorization codes live at most 60 seconds; PAR `request_uri` `expires_in` below 600 seconds.
- No refresh token rotation except in extraordinary circumstances (see the spec's Note 1); do not use HTTP 307 when redirecting a request that contains user credentials (303 is preferred for redirecting the user agent); no open redirectors.
- Publish discovery metadata (RFC 8414); accept `iat`/`nbf` up to 10 seconds in the future for clock offset.

Client (5.3.3): use the authorization code grant with PAR and PKCE S256, check `iss` in the response, send only `client_id` and `request_uri` to the authorization endpoint, and fetch AS metadata only from the discovery document, checking the issuer matches.

Resource server (5.3.4): accept tokens only in the Authorization header (not query parameters) and verify sender-constraining.

Crypto and transport: TLS 1.2 or later per BCP 195 (cipher suite limits for TLS 1.2); sign JWTs with PS256, ES256 or EdDSA (Ed25519), never `none`; RSA keys at least 2048 bits, EC keys at least 224 bits; follow RFC 8725 for JWTs.

Gotchas:
- The spec says deployments should use certified implementations; run the OpenID FAPI conformance tests early.
- Message signing is a separate document (FAPI Message Signing 2.0).

Verify: test that a plain authorization request without PAR, a request without S256 PKCE, and a bearer-only token are all rejected.

## Checked

Method: 2026-11-09 docs-only; fetched fapi-security-profile-2_0.html and read sections 5.2 to 5.4 requirement lists (grep of shall/should items, not every paragraph). Dropped the message-signing URL (not read here), the "RS256 not allowed" wording (spec lists permitted algorithms instead), and the unsourced "short-lived access tokens" claim.
