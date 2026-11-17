---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-token-exchange-request
name: oauth-token-exchange-request
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-token-exchange-request, oauth-token-exchange, rfc8693, token-exchange, subject_token, actor_token, requested_token_type, audience, identity-protocols]
level: advanced
status: docs-checked
description: "Exchange one token for another with grant_type token-exchange: subject_token, actor_token, requested_token_type, audience, resource and scope."
sources:
  - https://www.rfc-editor.org/rfc/rfc8693
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Token exchange request and response

Goal: get a token for a downstream service from an inbound token.

Method: POST (form-encoded) to the token endpoint with `grant_type=urn:ietf:params:oauth:grant-type:token-exchange`, `subject_token` and `subject_token_type` (required; types include `urn:ietf:params:oauth:token-type:access_token`, `:refresh_token`, `:id_token`, `:saml1`, `:saml2` and `urn:ietf:params:oauth:token-type:jwt`), optional `actor_token` with `actor_token_type` (required when `actor_token` is present, forbidden otherwise), `requested_token_type`, `resource` (absolute URI, no fragment), `audience` (logical name), `scope`. The client authenticates by the normal OAuth mechanisms. Response (200, JSON): `access_token`, `issued_token_type`, `token_type` (`N_A` if the token is not usable as an access token), recommended `expires_in`, `scope` (required if different from the request), optional `refresh_token`.

Gotchas:
- Whether to allow unauthenticated clients and which entities may exchange for which targets are authorization server policy; omitting client authentication lets anyone holding a compromised token exchange it.
- Multiple `resource` or `audience` values request a token usable at all of them (the Cartesian product of scopes and targets); very broad requests are more likely to fail and the server can answer `invalid_target`.
- An invalid request or unacceptable `subject_token` or `actor_token` returns `invalid_request`; an unwilling or unable server for a target SHOULD return `invalid_target`.
- The exchange does not itself invalidate the subject token.
- Tokens may carry privacy-sensitive data and MUST only travel over TLS; limit scope and lifetime to mitigate abuse.

Verify: exchange a token for an unauthorised audience and expect rejection.

## Checked
2026-11-02. Confirmed against RFC 8693 sections 1.1, 2.1, 2.1.1, 2.2, 3, 5 and 6. Removed: "define allowed subject/audience pairs" and "keep chain length limited, log subject and actor" (not stated), and the narrowing of `invalid_request` to bad token types (RFC: any invalid request or token).
Method: documentation only; no commands were run.
