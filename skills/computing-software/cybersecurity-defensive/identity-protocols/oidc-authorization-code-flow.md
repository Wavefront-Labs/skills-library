---
id: computing-software.cybersecurity-defensive.identity-protocols.oidc-authorization-code-flow
name: oidc-authorization-code-flow
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oidc-authorization-code-flow, oidc-core-flows, oidc, authorization-code, openid-scope, token-endpoint, response_type-code, identity-protocols]
level: practitioner
status: docs-checked
description: "Run the OIDC code flow: scope=openid request, code exchange at the token endpoint, ID token plus access token response and the checks in order."
sources:
  - https://openid.net/specs/openid-connect-core-1_0.html
  - https://www.rfc-editor.org/rfc/rfc7636.txt
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Authorization Code flow with ID token

Goal: authenticate a user and get an ID token safely.

Method:
1. Redirect to the authorization endpoint with `response_type=code&scope=openid profile email&client_id=...&redirect_uri=...&state=...&nonce=...`, plus a PKCE `code_challenge` (RFC 7636).
2. On callback verify `state`, then POST (form-encoded) to the token endpoint: `grant_type=authorization_code&code=...&redirect_uri=...&code_verifier=...`. A confidential client must authenticate with the method registered for its `client_id`.
3. The response includes `access_token`, `token_type` (Bearer) and `id_token` (and a refresh token if one is issued, for example after `offline_access` consent). It carries `Cache-Control: no-store`.
4. Validate the ID Token before creating a session.

Gotchas:
- The `openid` scope is mandatory in an OpenID Connect request; without it the request may still be valid OAuth 2.0 but is not OpenID Connect.
- The `redirect_uri` at the token step must be identical to the one in the authorization request.
- The server must verify the code was issued to the authenticating client, and, if possible, that it was not previously used.
- `state` is RECOMMENDED and is typically bound to a browser cookie to mitigate CSRF.

Verify: decode the ID token and confirm `nonce` equals the value you sent.

## Checked
2026-11-02. Confirmed against OpenID Connect Core 1.0 sections 3.1.2.1, 3.1.2.2, 3.1.3.1 to 3.1.3.3 and 11, and RFC 7636 (`code_challenge`, `code_verifier`). Removed: "reuse should revoke tokens issued from it" (Core only says to verify non-reuse if possible).
Method: documentation only; no commands were run.
