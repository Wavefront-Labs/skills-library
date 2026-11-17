---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-token-introspection
name: oauth-token-introspection
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-token-introspection, oauth-introspection-revocation, introspection, rfc7662, active, opaque-token, token_type_hint, identity-protocols]
level: practitioner
status: docs-checked
description: "Call the introspection endpoint to check opaque tokens: authenticated POST, active flag, claims returned, caching and token_type_hint."
sources:
  - https://www.rfc-editor.org/rfc/rfc7662
  - https://www.rfc-editor.org/rfc/rfc7009
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Token introspection (RFC 7662)

Goal: let a resource server validate opaque tokens.

Method: RS authenticates (client credentials or a bearer token) and POSTs `token=<value>&token_type_hint=access_token` to the introspection endpoint. Response JSON: `active` (boolean, required), and when active `scope`, `client_id`, `username`, `token_type`, `exp`, `iat`, `nbf`, `sub`, `aud`, `iss`, `jti`. Inactive tokens return only `{"active": false}` with 200.

Gotchas:
- Check `active` first, then use `scope`, `aud` and the other returned fields in the authorization decision.
- A resource server MAY cache the response; a cached response must not be used beyond the token's `exp`, and a longer cache trades network traffic against the risk of stale data (RFC 7662 section 4).
- The endpoint must require authorization of the caller (the AS MUST require authentication of protected resources), otherwise anyone can probe token validity.

Verify: introspect a revoked token and expect active=false.

## Checked

2026-11-02. Confirmed against RFC 7662 sections 2 and 4 (caller authorization, request and response members, `active`, caching and its limits, endpoint protection). Removed: the latency remark.
Method: documentation only; no commands were run.
