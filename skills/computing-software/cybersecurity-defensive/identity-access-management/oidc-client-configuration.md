---
id: computing-software.cybersecurity-defensive.identity-access-management.oidc-client-configuration
name: oidc-client-configuration
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [sso, oidc-client-configuration, openid-connect, oauth2, pkce, redirect-uris, token-validation, oidc-rp-configuration, oidc-rp-configuration]
level: practitioner
status: docs-checked
description: "Configure OpenID Connect clients securely: app registration, authorization code with PKCE, redirect URIs, scopes, token validation and credentials."
sources: ["https://openid.net/specs/openid-connect-core-1_0.html", "https://datatracker.ietf.org/doc/html/rfc9700", "https://learn.microsoft.com/en-us/entra/identity-platform/v2-protocols-oidc"]
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# OIDC client configuration

**Goal:** an application signs users in with OpenID Connect using the current best-practice
flow, validates tokens properly, and keeps its credentials safe.

## Registration at the IdP
- Client type: **confidential** (server-side web app, can hold a credential) or **public**
  (SPA, mobile, desktop; cannot keep secrets).
- **Redirect URIs:** exact HTTPS URLs; no wildcards; `localhost` only for development
  registrations. Separate registrations per environment.
- Grant types: authorization code only (with PKCE). Disable implicit flow and resource owner
  password grant (deprecated in OAuth 2.0 Security BCP, RFC 9700).
- Credentials for confidential clients: prefer **certificate / private_key_jwt** over client
  secrets; if secrets, short expiry and rotation via a vault.
- Scopes: `openid profile email` plus only the API scopes needed.

## Flow (authorization code + PKCE)
1. App creates `code_verifier` (random 43-128 chars) and `code_challenge = BASE64URL-ENCODE(SHA256(ASCII(code_verifier)))` (RFC 7636),
   plus `state` (CSRF) and `nonce` (replay), and redirects to the authorise endpoint.
2. User authenticates; IdP redirects back with `code` and `state`.
3. App verifies `state`, exchanges `code` + `code_verifier` (+ client credential) at the
   token endpoint for ID token, access token, refresh token.

## Validate the ID token
- Signature with keys from the IdP's `jwks_uri` (from discovery document
  `/.well-known/openid-configuration`); allow only expected algorithms and never unsecured `{"alg":"none"}` tokens.
- `iss` equals the expected issuer; `aud` contains your client ID; `exp`/`iat` within skew;
  `nonce` matches.
- Use a maintained library; do not hand-roll.

## Sessions and tokens
- Store tokens server-side (confidential apps) or in memory (SPAs; or use a BFF pattern so
  tokens never reach the browser).
- Refresh token rotation for public clients; revoke on logout; implement front/back-channel
  logout if the IdP supports it.
- Map identity by the stable subject, together with the issuer (OWASP: use `iss` and `sub`, not `sub` alone), not by email (emails change and
  can be reused).

## Gotchas
- Multi-tenant apps accepting any tenant's tokens without checking the issuer allow sign-in
  from attacker tenants.
- Access tokens are for APIs; do not use them as proof of authentication in the client.
- Open redirects after login (a post-login return-URL parameter) enable phishing; allowlist.

## Verify
Tamper tests: modified ID token signature rejected, wrong `aud` rejected, replayed `state`
rejected; the registration shows no implicit grant and only exact redirect URIs.

## Checked

2026-10-28. Confirmed: OpenID Connect Core (`aud` must contain the client ID, ID Token signed with JWS); RFC 7636 (43-128 character verifier); RFC 9700 (implicit and ROPC discussion, nonce); Microsoft Entra OIDC page (`/.well-known/openid-configuration`, `jwks_uri`); OWASP (`alg: none`, `iss` plus `sub`). Removed: the `S256` shorthand formula (replaced with the RFC form), RS256/ES256 named algorithms, library names, `oid`/`tid` claim names and the `returnUrl` parameter name.
Method: documentation only; no commands were run.
