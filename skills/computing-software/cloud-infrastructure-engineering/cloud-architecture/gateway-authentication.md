---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.gateway-authentication
name: gateway-authentication
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, api-gateway-patterns, gateway-authentication, jwt-validation, oauth2-gateway, mtls-gateway, api-keys, token-exchange]
level: practitioner
status: docs-checked
description: "Authenticate at the API gateway: JWT checks (signature, issuer, audience, expiry), route scopes, algorithm pinning per RFC 8725 and separate rules per token kind."
sources: ["https://learn.microsoft.com/azure/api-management/validate-jwt-policy", "https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-jwt-authorizer.html", "https://www.rfc-editor.org/rfc/rfc8725", "https://www.rfc-editor.org/rfc/rfc8693"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authentication at the gateway

## What the gateway should do
1. **Validate tokens.** Example from the API Gateway HTTP API JWT authorizer: the `kid` header must match a
   key in the issuer's `jwks_uri`; `iss` must match the configured issuer; `aud` (or `client_id` only when
   `aud` is absent) must match a configured audience; `exp` must be after now and `nbf` before now, in UTC;
   `scope` or `scp` must include at least one scope of the route's `authorizationScopes`.
2. **Pin algorithms** (RFC 8725): libraries must let the caller specify the supported algorithm set and use
   no other, check that the `alg` header matches the algorithm used, and use each key with exactly one
   algorithm. An attacker can otherwise set the algorithm to `none` against libraries that then skip
   signature checks. RFC 8725 also covers validating issuer and subject (section 3.8) and audience (3.9).
3. **Separate token kinds.** When the same issuer issues several kinds of JWT, validation rules must be
   mutually exclusive so a token of the wrong kind is rejected (RFC 8725 section 3.12). API Gateway notes
   there is no standard way to tell access tokens from OpenID Connect ID tokens, so require scopes and
   configure issuers or audiences used only for access tokens.
4. **Coarse authorisation**: required scopes per route; backends still do fine-grained checks.
5. In Azure API Management the equivalent is the `validate-jwt` policy; read its page for the available
   checks.

## Passing identity to backends
- Forward the validated token, or exchange it for another token with reduced scope using OAuth 2.0 Token
  Exchange (RFC 8693).
- If you forward identity in headers, backends must accept traffic only from the gateway, and the gateway
  must strip incoming copies of those headers (design advice, not stated in the cited pages).

## Gotchas
- Accepting tokens for any audience from the same identity provider.
- Relying on gateway authentication while backends are also publicly reachable.

## Verify
- [ ] Tests with expired, wrong-audience, wrong-issuer and `alg=none` tokens are all rejected.
- [ ] A token missing the route's scope is denied.

## Checked
2026-11-01. Confirmed against the API Gateway HTTP API JWT authorizer page (claim checks) and RFC 8725
(sections 3.1, 3.8, 3.9, 3.12). RFC 8693 and the APIM `validate-jwt` page are cited for token exchange and
the policy's existence only. Removed: the pinned RS256/ES256 recommendation, the clock-skew figure, the
mTLS and API-key guidance and the list of other gateways' plugins, none of which were confirmed in these
pages. The header-stripping advice is design guidance, not a documented claim.
Method: documentation only; no commands were run.
