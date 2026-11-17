---
id: computing-software.cryptography-implementation.protocol-implementation.srp-6a-legacy-considerations
name: srp-6a-legacy-considerations
category: computing-software
field: cryptography-implementation
product: protocol-implementation
tags: [protocol-implementation, cryptography-implementation, srp-6a, srp, pake, rfc-5054, opaque, legacy-protocols]
level: advanced
status: docs-checked
description: "Maintain or migrate SRP-6a password authentication: verifier storage, group and hash choices, known implementation bugs, RFC 5054 TLS-SRP status, and moving to OPAQUE."
sources: ["http://srp.stanford.edu/design.html", "https://www.rfc-editor.org/rfc/rfc5054", "https://blog.cryptographyengineering.com/should-you-use-srp/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SRP-6a legacy considerations

SRP is an augmented PAKE (the server stores a verifier, not the password).
RFC 5054 defines its use in TLS (TLS-SRP).

## Core values (RFC 5054 form)
`x = SHA1(s | SHA1(I | ":" | P))`, `v = g^x % N`, `k = SHA1(N | PAD(g))`, client `A = g^a % N`,
server `B = k*v + g^b % N`, `u = SHA1(PAD(A) | PAD(B))`; the premaster secret is
`(B - (k * g^x)) ^ (a + (u * x)) % N` on the client and `(A * v^u) ^ b % N` on the server. `PAD()` left-pads the
integer with zeros to the length of N. Other SRP deployments pick their own hash, so match the peer's definition.

## Checks every implementation must make
- Server aborts the handshake (`illegal_parameter` alert in TLS) if `A % N = 0`; client aborts if `B % N = 0`.
- Take N and g from the RFC 5054 Appendix A groups (1024-, 1536- and 2048-bit groups are listed there) or from
  parameters you control; the RFC warns about an attacker supplying an N of special form, so do not accept
  arbitrary parameters from the peer.
- Padding: `PAD()` in the u and k computations; mismatched padding breaks interop silently.

## Weaknesses
- Cryptographic Engineering's review: SRP's original analysis contains no proof of security, the protocol leaks the
  salt to unauthenticated users by design, and it does not translate cleanly to elliptic curves.
- RFC 5054 computes `x` with SHA-1; the same review assumes the hash is a strong password hashing function such as
  scrypt, so if you control both sides use a slow KDF for `x`.

## Migration
Move to OPAQUE (RFC 9807): run SRP for login, and after successful SRP login register the user in OPAQUE, then
delete the verifier.

## Verify
- [ ] RFC 5054 Appendix B test vectors pass; tests with A % N = 0 and B % N = 0 abort.

## Checked

2026-11-01. Confirmed against RFC 5054 (x, v, k, A, B, u and premaster formulas, PAD() definition, abort conditions
and `illegal_parameter` alert, Appendix A groups, Appendix B test vectors, special-form N warning) and the Cryptographic
Engineering SRP review (no proof, salt leak, EC difficulty, scrypt assumption). Removed: vendor usage list (Apple, 1Password,
Cognito), the `u == 0` abort, the "at least 2048 bits" rule, the 1Password 2SKD reference, the claim that TLS-SRP is
absent from TLS 1.3, and the constant-time remark (not in the sources).
Method: documentation only; no commands were run.
