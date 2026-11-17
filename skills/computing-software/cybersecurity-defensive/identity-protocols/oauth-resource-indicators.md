---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-resource-indicators
name: oauth-resource-indicators
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-resource-indicators, oauth-jwt-access-tokens, rfc8707, resource-indicator, audience, resource-parameter, identity-protocols]
level: advanced
status: docs-checked
description: "Use the resource parameter (RFC 8707) to request tokens for one API, so audience-restricted tokens are not replayable at other resource servers."
sources:
  - https://www.rfc-editor.org/rfc/rfc8707
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Resource indicators and audience restriction

Goal: bind tokens to a single intended API.

Method: add a `resource` parameter, for example `resource=https://api.example.com/app/`, to the authorization request and the token request. The value MUST be an absolute URI without a fragment (and SHOULD NOT contain a query); use the most specific base URI of the API. The authorization server SHOULD audience-restrict issued access tokens to the indicated resource(s), carried as `aud` in a JWT or as the top-level `aud` member of an introspection response; it may use the exact value or map it to a more general identifier. Multiple `resource` parameters MAY be used. In the code flow the resource applies to the whole authorization grant. Errors use `invalid_target`.

Gotchas:
- If `resource` is omitted, the server MAY use no specific resource or a default, or MAY require it and fail with `invalid_target`.
- Using a single `resource` is encouraged: a token with several audiences can be used by any one of those resources against the others, and the server may refuse multi-resource requests.
- On multi-tenant servers include the tenant-identifying part of the URI (such as a path component) in the resource value so tokens cannot cross tenants.
- The server should downscope the token's `scope` to what the resource needs and report the effective `scope` when it differs from the request.

Verify: request with two resources and check the returned `aud`.

## Checked
2026-11-02. Confirmed against RFC 8707 sections 2, 2.1, 2.2 and 3. Removed: the claim that "many AS issue a token for a default audience", the Entra and Auth0 specifics, and the sender-constraining pairing advice. RFC 9068 was dropped from sources because no claim rests on it.
Method: documentation only; no commands were run.
