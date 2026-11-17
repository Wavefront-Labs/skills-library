---
id: computing-software.cryptography-implementation.applied-cryptography.ed25519-verification-strictness
name: ed25519-verification-strictness
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, ed25519-verification-rules, ed25519, eddsa, zip-215, cofactor, signature-malleability, consensus, rfc-8032]
level: advanced
status: verified
description: "Handle Ed25519 verification differences: canonical S and point encodings, small-order keys, cofactored versus cofactorless equations, ZIP-215 consensus rules."
sources: ["https://www.rfc-editor.org/rfc/rfc8032#section-5.1.7", "https://zips.z.cash/zip-0215", "https://eprint.iacr.org/2020/1244"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ed25519 verification strictness

RFC 8032 leaves room for implementations to disagree on edge cases, so the same (message, signature, key) can verify
in one library and fail in another. "Taming the many EdDSAs" (Chalkias, Garillot, Nikolaenko, 2020) tested popular libraries and found a range of
behaviours.

## The edge cases
| Check | Strict (libsodium, verify_strict) | Lenient |
|---|---|---|
| S < L (group order) | Required; otherwise signatures are malleable | All modern libraries require this |
| Canonical encoding of R and A | Rejects non-canonical y >= p | Some accept |
| Small-order A or R | Rejected | Accepted (a small-order key verifies many messages) |
| Equation | Cofactorless `[S]B = R + [k]A` | Cofactored `[8][S]B = [8]R + [8][k]A` |

Cofactored and cofactorless verification disagree only on crafted signatures involving small-order components, but
that is enough to fork a consensus system.

## Picking a rule
- **Single verifier, ordinary app:** use your library's default and ensure S < L and small-order rejection
  (libsodium `crypto_sign_verify_detached` and ed25519-dalek `verify_strict` are the strict ones). Run here: the identity
  public key with signature R = identity, S = 0 verifies any message in pyca/cryptography (OpenSSL 3.2.3) and in Go
  1.26 `crypto/ed25519.Verify`, but libsodium rejects it, so Go and OpenSSL do not reject small-order keys on their own: add a
  small-order check if you need it. S + L is rejected by pyca and libsodium.
- **Consensus or multi-implementation systems (blockchains, transparency logs):** all nodes must agree exactly.
  ZIP-215 specifies: A and R are any encodings of curve points (not required canonical), S < L, and the cofactored
  equation [8][S]B = [8]R + [8][k]A; it forbids the cofactorless one. Use a
  library that implements ZIP-215 (crates `ed25519-zebra` 5.0.0, `ed25519-consensus` 2.1.0; Go `hdevalence/ed25519consensus`) everywhere.
- **Batch verification** needs the cofactored equation to agree with single verification.

## Malleability
With S < L enforced, an attacker cannot produce a second valid signature for the same message and key; but
signature uniqueness still should not be used as a transaction ID. Hash the message or use a separate ID.

## Verify
- [ ] Run the "Taming the many EdDSAs" test vectors (published with the paper) against your verifier.
- [ ] All implementations in a consensus system return identical results on those vectors.
