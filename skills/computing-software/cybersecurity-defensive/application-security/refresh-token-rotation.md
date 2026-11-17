---
id: computing-software.cybersecurity-defensive.application-security.refresh-token-rotation
name: refresh-token-rotation
category: computing-software
field: cybersecurity-defensive
product: application-security
tags: [refresh-token-rotation, oauth2, reuse-detection, token-binding, dpop, session-management]
level: advanced
status: docs-checked
description: "Implement OAuth refresh token rotation with reuse detection: token families, sender-constraining with DPoP or mTLS, expiry and revocation on security events."
sources: ["https://datatracker.ietf.org/doc/html/rfc9700", "https://datatracker.ietf.org/doc/html/rfc9449", "https://auth0.com/docs/secure/tokens/refresh-tokens/refresh-token-rotation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Refresh token rotation

A refresh token represents the full scope granted to a client and is not constrained to one resource, so a stolen
and replayed refresh token lets the attacker mint access tokens (RFC 9700 section 4.14.1). RFC 9700 (OAuth 2.0
Security Best Current Practice, section 4.14.2) requires authorization servers to use one of two methods to detect
refresh token replay for public clients.

## Option 1: rotation with reuse detection
1. Every refresh response returns a new access token and a new refresh token; the previous refresh token is
   invalidated, but the server keeps the relationship between them.
2. If a compromised token is used by both attacker and legitimate client, one of them presents an invalidated
   token. The server cannot tell which party it was, so it revokes the active refresh token. This stops the attack at
   the cost of forcing the legitimate client to obtain a fresh authorization grant.
3. Group tokens into a **family** (all refresh tokens descending from the original token). Auth0 invalidates the
   whole family on reuse, including the newest token, and requires re-authentication; it logs reuse events (for
   example `ferrt` for a failed exchange).
4. RFC 9700 implementation note: if the grant is encoded into the refresh token to find the family, the server must
   protect the token's integrity, for example with signatures.

## Option 2: sender-constrained refresh tokens
The authorization server cryptographically binds the refresh token to a client instance using mTLS (RFC 8705) or
DPoP (RFC 9449).
- DPoP: the client proves possession of a private key with a signed proof JWT on each request; a refresh token
  issued to a public client is bound to the public key of the DPoP proof. Access tokens carry the key thumbprint in
  `cnf` as the `jkt` member (a JWK SHA-256 thumbprint). The private key can be non-extractable when WebCrypto is
  used.

## Expiry, scope and revocation
- Authorization servers must decide by risk assessment whether to issue refresh tokens at all, and must bind them to
  the scope and resource servers the owner consented to.
- Refresh tokens should expire after the client has been inactive for some time; the duration is at the server's
  discretion (a global value or per client policy or grant).
- Servers may revoke refresh tokens on security events such as password change or logout at the authorization
  server.

## Verify
Refresh once (token A returns B), then present A again: the server rejects A and B stops working; the family needs
a fresh authorization grant.

## Checked
Method: docs-checked 2026-11-09 against RFC 9700 (section 4.14, read in full), RFC 9449 (the `jkt` confirmation
method, refresh-token binding and non-extractable key passages) and the Auth0 refresh token rotation page (read in
full). Removed unconfirmed claims: grace-period guidance, specific lifetimes, the stored-field names and
hash-only storage, mobile storage advice, BFF and RFC 7009 revocation guidance, and the browser-based-apps draft
source.
