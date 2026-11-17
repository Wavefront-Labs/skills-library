---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-refresh-token-rotation
name: oauth-refresh-token-rotation
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-refresh-token-rotation, oauth-refresh-tokens, refresh-token, rotation, reuse-detection, token-family, public-client, identity-protocols]
level: advanced
status: docs-checked
description: "Rotate refresh tokens on each use, detect reuse of an old token and revoke the whole token family, with grace windows for network retries."
sources:
  - https://www.rfc-editor.org/rfc/rfc9700
  - https://www.rfc-editor.org/rfc/rfc6749
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Refresh token rotation and reuse detection

Goal: limit damage when a refresh token leaks from a public client.

Method (RFC 9700 Sections 2.2 and 4.14.2): refresh tokens for public clients MUST be sender-constrained or use refresh token rotation. With rotation the AS issues a new refresh token with every access token refresh response and invalidates the previous one, but retains information about the relationship. If a token was compromised and used by both attacker and legitimate client, one of them will present an invalidated token, which informs the AS of the breach. The AS cannot tell which party it was, but it revokes the active refresh token. This stops the attack at the cost of forcing the legitimate client to obtain a fresh authorization grant. The grant a refresh token belongs to may be encoded in the token so all related tokens can be found and revoked; the AS MUST then ensure the token's integrity, for example with signatures.

Gotchas:
- The client MUST discard the old refresh token when it receives a new one (RFC 6749 Section 6).
- Sender-constrained refresh tokens (for example DPoP or mutual TLS) are the RFC 9700 alternative to rotation for public clients.
- RFC 9700 does not specify grace windows, token-family identifiers, absolute lifetimes or idle timeouts; those are deployment choices to document yourself.

Verify: use an old refresh token a second time and confirm the active token is revoked.

## Checked

Date: 2026-11-02. Confirmed in RFC 9700 Sections 2.2 and 4.14.2 and RFC 6749 Section 6. Removed as not stated there: "family ID" wording, the grace-window figure, concurrent-tab locking advice, the 30-90 day lifetime example.

Method: documentation only; no commands were run.
