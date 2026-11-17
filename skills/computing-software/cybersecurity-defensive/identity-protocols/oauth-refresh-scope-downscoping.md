---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-refresh-scope-downscoping
name: oauth-refresh-scope-downscoping
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-refresh-scope-downscoping, oauth-refresh-tokens, refresh_token, scope, downscope, grant_type-refresh_token, identity-protocols]
level: practitioner
status: docs-checked
description: "Request narrower scope on refresh, understand that scope may not exceed the original grant, and how the AS returns scope and expiry."
sources:
  - https://www.rfc-editor.org/rfc/rfc6749
  - https://www.rfc-editor.org/rfc/rfc9700
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Refresh requests and scope downscoping

Goal: get least-privilege access tokens from one grant.

Method (RFC 6749 Section 6): POST to the token endpoint with `grant_type=refresh_token`, the `refresh_token`, and optionally `scope`, plus client authentication if the client is confidential or was issued credentials. The requested `scope` MUST NOT include any scope not originally granted by the resource owner; if omitted it is treated as equal to the scope originally granted. The AS MAY issue a new refresh token, in which case the client MUST discard the old one, and the new refresh token's scope MUST be identical to the old one's; if no new token is issued the client keeps using the old one. If the issued access token scope differs from the one requested, the AS MUST include the `scope` response parameter. `invalid_scope` is the token endpoint error for a requested scope that is invalid, unknown or malformed (Section 5.2).

Gotchas:
- Refresh tokens are bound to the client to which they were issued; RFC 9700 Section 2.2: refresh tokens for public clients MUST be sender-constrained or use refresh token rotation.
- RFC 9700 notes the AS MAY revoke refresh tokens automatically on a security event.

Verify: request a scope beyond the original grant and expect the request to be rejected.

## Checked

Date: 2026-11-02. Confirmed in RFC 6749 Sections 5.2 and 6 and Section 3.3 (scope response parameter), and RFC 9700 Section 2.2. Removed as not stated there: "use narrow tokens per API", "the AS must check account state at refresh", and the claim that a scope beyond the grant returns exactly `invalid_scope`.

Method: documentation only; no commands were run.
