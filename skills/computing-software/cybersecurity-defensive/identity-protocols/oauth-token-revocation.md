---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-token-revocation
name: oauth-token-revocation
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-token-revocation, oauth-introspection-revocation, revocation, rfc7009, revoke, logout, token_type_hint, identity-protocols]
level: practitioner
status: docs-checked
description: "Revoke access or refresh tokens at the revocation endpoint, the effect on related tokens and the 200 response even for unknown tokens."
sources:
  - https://www.rfc-editor.org/rfc/rfc7662
  - https://www.rfc-editor.org/rfc/rfc7009
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Token revocation (RFC 7009)

Goal: let clients invalidate tokens on logout or compromise.

Method: POST `token=<value>&token_type_hint=refresh_token` with client authentication to `revocation_endpoint`. Success is HTTP 200, also when the client submitted an invalid token (the client ignores the response body). Revoking a refresh token SHOULD also invalidate access tokens based on the same grant (if the AS supports revoking them); revoking an access token MAY also revoke the refresh token.

Gotchas:
- Error `unsupported_token_type` if the AS cannot revoke that type.
- An invalid `token_type_hint` is ignored by the AS and does not influence the revocation response.
- Revocation is meant for events such as logout, an identity change or uninstalling the app (RFC 7009 introduction).
- There can be a propagation delay across servers; clients must not use the token after a 200 response.

Verify: revoke and then refresh with the same token; expect invalid_grant.

## Checked

2026-11-02. Confirmed against RFC 7009 sections 1, 2.1 and 2.2 (request, 200 for invalid tokens, cascade behaviour, hint handling, propagation delay) and RFC 6749 (`invalid_grant`). Removed: the empty-body claim, the JWT and introspection remark and the extended list of revocation triggers.
Method: documentation only; no commands were run.
