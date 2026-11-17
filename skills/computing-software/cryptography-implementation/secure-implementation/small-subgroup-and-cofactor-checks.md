---
id: computing-software.cryptography-implementation.secure-implementation.small-subgroup-and-cofactor-checks
name: small-subgroup-and-cofactor-checks
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [cryptography-implementation, secure-implementation, point-validation, small-subgroup-attack, cofactor, x25519, finite-field-dh, ed25519]
level: advanced
status: gated
description: "Defend against small-subgroup and cofactor attacks: FFDH subgroup checks, X25519 all-zero output, Ed25519 cofactored verification, and using prime-order groups like ristretto255."
sources: ["https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-56Ar3.pdf", "https://www.rfc-editor.org/rfc/rfc7748#section-6.1", "https://www.rfc-editor.org/rfc/rfc2785", "https://hdevalence.ca/blog/2020-10-04-its-25519am", "https://www.rfc-editor.org/rfc/rfc9496"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Small-subgroup and cofactor checks

A small-subgroup attack sends a public value of small order. The victim's shared secret then
takes one of a few values, leaking the private key modulo that order; repeated with static
keys, the whole key falls out (Lim-Lee (gated: unconfirmed, source is paywalled or blocked)). Cofactor issues are the same root cause on curves
whose group order is h * q with h > 1.

## Finite-field DH (SP 800-56A 5.6.2.3.1, RFC 2785)
For peer value y in group (p, q, g):
1. `2 <= y <= p - 2` (rejects 0, 1, p-1).
2. `pow(y, q, p) == 1` (y is in the order-q subgroup).
In safe-prime groups (RFC 7919 ffdhe*, RFC 3526) q = (p-1)/2, so after check 1 the only leak
is one bit (order q vs 2q); RFC 7919 section 5.1 requires `1 < Y < p-1` for its named groups (which also guards the 2-element subgroup). DSA-style groups
with a small q and large cofactor need check 2 always. Prefer RFC 7919 groups and ephemeral keys.

## X25519 / X448 (RFC 7748)
- The function clamps scalars (clears the low 3 bits), so small-order points cannot leak key bits.
- Small-order inputs still yield an all-zero shared secret. Check for it and abort
  (RFC 7748 section 6.1 "MAY", RFC 8446 TLS 1.3 "MUST check ... all-zero"). Run here with five small-order points: pyca raises `ValueError`, PyNaCl's `crypto_scalarmult` (libsodium returns -1) raises `RuntimeError`, Go 1.22 `ecdh.X25519` returns "low order point".
- Contributory behaviour: protocols that assume both parties influence the secret must also
  hash both public keys into the KDF (as Noise and HPKE do).

## NIST prime curves (P-256/384/521)
Cofactor 1, so no small subgroup - but the invalid-curve attack applies: validate the point is
on the curve (see ECDH public key validation). Libraries do this on decode; hand-rolled
point parsing must too.

## Ed25519 signatures
- Cofactor 8. Libraries disagree on cofactored vs cofactorless verification and on accepting
  small-order or non-canonical points, which breaks consensus systems and batch verification.
- Use ZIP 215 rules (specified for Zcash consensus) or strict rules (dalek `verify_strict`; libsodium `open.c` rejects non-canonical and small-order A and R) consistently across all nodes. Pin one library where agreement matters.

## Prime-order abstractions
Building a new protocol (PAKE, VOPRF, threshold) over Curve25519: use ristretto255 (RFC 9496),
which exposes a prime-order group and removes cofactor reasoning entirely.

## Verify
- [ ] Tests feed every small-order X25519 point (RFC 7748 and libsodium blocklist) and expect rejection.
- [ ] FFDH code rejects 0, 1, p-1 and an element of a small subgroup.
- [ ] Ed25519 verification rules are documented and identical across services.
