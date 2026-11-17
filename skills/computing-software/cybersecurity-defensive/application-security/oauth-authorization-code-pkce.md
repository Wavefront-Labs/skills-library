---
id: computing-software.cybersecurity-defensive.application-security.oauth-authorization-code-pkce
name: oauth-authorization-code-pkce
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [session-management, oauth-pkce, pkce, oauth-2-1, authorization-code-flow, spa-security, redirect-uri]
level: advanced
status: docs-checked
description: "Implement the OAuth 2.0 authorisation code flow with PKCE for SPAs, mobile and server apps: S256 challenges, state and nonce, exact redirect URIs and secure token storage."
sources: ["https://datatracker.ietf.org/doc/html/rfc7636", "https://datatracker.ietf.org/doc/html/rfc9700", "https://datatracker.ietf.org/doc/html/rfc9449", "https://datatracker.ietf.org/doc/html/rfc8252"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# OAuth authorisation code with PKCE

**Goal:** clients obtain tokens without implicit flow or leaked codes; intercepted authorisation codes are useless.

## Flow
1. Client creates `code_verifier` = 43-128 chars of high-entropy random (e.g. 32 random bytes base64url).
2. `code_challenge = BASE64URL(SHA256(code_verifier))`, `code_challenge_method=S256` (RFC 9700: use a method that does not expose the verifier; avoid `plain`).
3. Redirect to `/authorize?response_type=code&client_id=..&redirect_uri=..&scope=openid%20profile&state=<random>&nonce=<random>&code_challenge=..&code_challenge_method=S256`.
4. On callback, compare `state` with the stored value (CSRF), then POST `/token` with `grant_type=authorization_code`, `code`, `redirect_uri`, `code_verifier`.
5. If using OpenID Connect, validate the ID token as that specification requires.

## Server-side (authorisation server) settings
- Require PKCE for public clients (RFC 9700: MUST) and use it for confidential clients too (RFC 9700: RECOMMENDED).
- Exact string matching of registered redirect URIs; no wildcards.
- Do not use the resource owner password credentials grant (RFC 9700: MUST NOT); avoid the implicit grant (RFC 9700 section 2.1.2).
- Short-lived, single-use authorization codes; on reuse, revoke the tokens issued from the code.
- Refresh token rotation with reuse detection for public clients, or sender-constrained tokens (DPoP, RFC 9449).

## Client types
- **SPA:** authorization code flow with PKCE; do not use the implicit flow.
- **Mobile/native:** external user-agent (system browser), not embedded WebViews (RFC 8252).
- **Server web app:** confidential client with client authentication plus PKCE.

## Gotchas
- Accepting `code_challenge_method=plain` downgrade.
- Open redirects on the client's redirect URI host can leak codes.

## Verify
- [ ] Token request without or with a wrong `code_verifier` fails.
- [ ] Mismatched `state` is rejected by the client.
- [ ] Authorisation server rejects unregistered redirect URI variants (trailing path, different port).

## Checked
2026-10-28. Confirmed against official pages: verifier length 43-128 characters (RFC 7636), PKCE MUST for public and RECOMMENDED for confidential clients, exact redirect URI matching, ROPC MUST NOT, refresh tokens sender-constrained or rotated for public clients, DPoP (RFC 9449), external user-agents (RFC 8252).
Removed or rewritten: the 60 s code lifetime, BFF and storage advice, ASWebAuthenticationSession, private_key_jwt and the localStorage gotcha (not in the fetched pages); non-URL sources replaced with RFC pages.
Method: documentation only; no commands were run.
