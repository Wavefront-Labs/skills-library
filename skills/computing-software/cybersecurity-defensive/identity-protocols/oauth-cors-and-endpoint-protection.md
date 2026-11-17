---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-cors-and-endpoint-protection
name: oauth-cors-and-endpoint-protection
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-cors-and-endpoint-protection, oauth-security-bcp, cors, token-endpoint, identity-protocols]
level: practitioner
status: docs-checked
description: "Decide which OAuth endpoints may support CORS per RFC 9700: token, metadata, JWKS and registration may; the authorization endpoint must not."
sources:
  - https://www.rfc-editor.org/rfc/rfc9700
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CORS and endpoint exposure for OAuth servers

Goal: expose only what browser clients need.

Method (RFC 9700, OAuth 2.0 Security Best Current Practice, section 2.6 Other Recommendations):
- To support browser-based clients, the endpoints they access directly MAY support CORS: the Token Endpoint, the Authorization Server Metadata endpoint, the `jwks_uri` endpoint and the Dynamic Client Registration endpoint.
- CORS MUST NOT be supported at the authorization endpoint: the client does not access it directly, it redirects the user agent to it.
- If browser clients do not call an endpoint directly, leave CORS off for it.
- Use end-to-end TLS between client and resource server (RECOMMENDED); authorization responses MUST NOT travel over unencrypted connections, so `http` redirect URIs are forbidden except loopback redirection for native clients.

Gotchas:
- RFC 9700 says nothing about UserInfo, introspection, wildcard origins or preflight handling; apply the CORS standard (WHATWG Fetch) and your own risk assessment there, and prefer origin allow-lists over reflecting the request `Origin`.

Verify: send a cross-origin request from an unregistered origin to each endpoint and confirm the authorization endpoint never returns CORS headers.

## Checked

2026-11-09. Read RFC 9700 section 2.6 (the CORS paragraph and neighbouring TLS and redirect rules; the rest of the RFC was searched for CORS, rate limiting and brute force, with no further hits). Removed: per-endpoint rules for UserInfo and introspection, the ACAO wildcard rule for discovery and JWKS, rate limiting and lockout, DPoP preflight and CSRF claims, which the RFC does not state.
Method: documentation only; no commands were run.
