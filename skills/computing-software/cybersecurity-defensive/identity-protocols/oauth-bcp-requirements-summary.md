---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-bcp-requirements-summary
name: oauth-bcp-requirements-summary
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-bcp-requirements-summary, oauth-security-bcp, rfc9700, security-bcp, checklist, audit, oauth-security, identity-protocols]
level: advanced
status: docs-checked
description: "Audit an OAuth deployment against the RFC 9700 recommendations: PKCE, exact redirects, no implicit, no password grant, sender-constrained tokens and refresh handling."
sources:
  - https://www.rfc-editor.org/rfc/rfc9700
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RFC 9700 requirements checklist

Goal: turn the BCP into an audit.

Checks:
1. Redirect URIs compared with exact string matching (only the port of a native-app localhost URI may vary).
2. Authorization code flow; public clients MUST use PKCE and it is RECOMMENDED for confidential clients (S256, the only method that does not expose the verifier); the implicit grant (`token` response type) SHOULD NOT be used.
3. Resource owner password credentials grant not used.
4. Access tokens audience-restricted and sender-constrained (DPoP or mTLS) where possible; privileges kept to the minimum.
5. Refresh tokens sender-constrained or rotated for public clients.
6. Mix-up defences (`iss` parameter, distinct redirect URIs).
7. Client authentication enforced where feasible; asymmetric methods (mTLS, `private_key_jwt`) RECOMMENDED.
8. AS does not automatically redirect on an invalid `client_id` and `redirect_uri` combination.
9. No open redirectors on the AS or client; CORS MUST NOT be supported at the authorization endpoint.
10. Authorization codes short-lived and single use; resource owner password credentials grant not used (item 3); CSRF prevented with PKCE, nonce or `state`.

Gotchas:

Verify: score each item per AS and client in a spreadsheet.

## Checked

2026-11-02. Confirmed against RFC 9700 sections 2.1 to 2.6 (exact matching, PKCE rules, implicit, sender-constraining, refresh tokens for public clients, audience restriction, password grant, client authentication, CORS, mix-up defences) and RFC 6749 section 4.1.2.1. Removed: the policy-exception and SaaS gotchas (opinion, not in the RFC) and the wording on public clients identified by redirect.
Method: documentation only; no commands were run.
