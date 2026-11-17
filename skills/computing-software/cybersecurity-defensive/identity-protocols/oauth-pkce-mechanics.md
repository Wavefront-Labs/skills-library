---
id: computing-software.cybersecurity-defensive.identity-protocols.oauth-pkce-mechanics
name: oauth-pkce-mechanics
category: computing-software
field: cybersecurity-defensive
product: identity-protocols
tags: [oauth-pkce-mechanics, oauth-pkce, pkce, code_verifier, code_challenge, s256, rfc7636, identity-protocols]
level: practitioner
status: docs-checked
description: "Generate code_verifier (43-128 chars from unreserved set), derive code_challenge with S256, send both at authorization and token requests."
sources:
  - https://www.rfc-editor.org/rfc/rfc7636
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PKCE verifier, challenge and S256

Goal: bind the code to the client instance that asked.

Method:
1. Generate `code_verifier`: 32 random bytes, base64url without padding (43 chars); allowed chars `A-Z a-z 0-9 - . _ ~`, length 43 to 128.
2. `code_challenge = BASE64URL(SHA256(ASCII(code_verifier)))`, `code_challenge_method=S256`.
3. Send challenge in the authorization request; send `code_verifier` in the token request.
4. The AS recomputes and compares; on mismatch return `invalid_grant`.


Gotchas:
- Use a cryptographically secure random generator for the verifier.
- Create a new verifier per authorization request (the challenge must be transaction-specific, RFC 9700).
- The challenge is the base64url encoding (no padding) of the raw SHA-256 digest bytes.

Verify: compare against RFC 7636 Appendix B test vector.

## Checked

2026-11-02. Confirmed against RFC 7636 sections 4.1 to 4.6, 7.1 and Appendix B (verifier alphabet and 43 to 128 length, 32 random octets giving a 43 character string, S256 transform, `invalid_grant` on mismatch) and RFC 9700 (transaction-specific challenge). Removed: the openssl shell example and the Math.random and hex remarks (not in the RFC).
Method: documentation only; no commands were run.
