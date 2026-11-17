---
id: computing-software.cryptography-implementation.applied-cryptography.x25519-key-agreement
name: x25519-key-agreement
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, key-agreement, ecdh, x25519-key-agreement, x25519, curve25519, rfc7748, all-zero-check, contributory-behaviour, hkdf]
level: advanced
status: docs-checked
description: "Do X25519 key agreement correctly: scalar clamping, the optional all-zero shared secret check, deriving keys with a KDF over K and both public keys."
sources: ["https://www.rfc-editor.org/rfc/rfc7748"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# X25519 key agreement

X25519 (RFC 7748) is an ECDH function over Curve25519 with 32-byte scalars and
u-coordinates; non-canonical u values must be accepted and reduced.

## Steps

1. Generate 32 random bytes from the CSPRNG; scalar decoding clears bits 0,1,2
   and 255 and sets bit 254 (RFC 7748 section 5), giving 2^254 plus eight times
   a value below 2^251. Do not clamp yourself unless you implement the primitive.
2. Exchange 32-byte public keys.
3. `K = X25519(my_private, peer_public)`.
4. **Consider rejecting an all-zero K.** A peer point of small order (order
   dividing the cofactor, 8 for Curve25519) forces the output to zero and
   removes your private key's contribution. RFC 7748 section 6.1 says both
   sides MAY check for all-zero (OR all bytes together, so the check does not
   leak timing) and abort; section 7 says designers must not assume
   contributory behaviour. The RFC notes many implementations do not check, so
   test your library.
5. **Derive keys with a KDF** that includes K, K_A and K_B (RFC 7748 section
   6.1) rather than using K directly. Including both public keys matters
   because several public keys are equivalent and produce the same shared
   secret (section 7).

## Gotchas

- Order the public keys canonically (initiator first, or sorted) so both sides
  compute the same `info`.
- X25519 has no authentication. Ephemeral-ephemeral X25519 alone is
  vulnerable to man-in-the-middle; authenticate the public keys (signatures,
  static keys in a Noise pattern, or a PAKE).
- X25519 public keys are u-coordinates only; Ed25519 uses a birationally
  equivalent twisted Edwards curve with different encodings. Prefer separate
  keys for signing and key agreement.
- Check regulatory approval of X25519 separately for FIPS deployments.

## Verify

- [ ] RFC 7748 section 5.2 and 6.1 vectors pass.
- [ ] Behaviour on a low-order point (e.g. all-zero public key) is known and handled.
- [ ] Session key derived via a KDF with K and both public keys.
- [ ] Public keys are authenticated by some mechanism.

## Checked

2026-11-01: RFC 7748 sections 5, 6.1 and 7 read. Confirmed: scalar bit decoding, optional all-zero check and its rationale, KDF over K, K_A and K_B, no contributory-behaviour assumption, equivalent public keys, birational equivalence to the Edwards curve. Removed: pyca, libsodium and Go behaviours, code sample, FIPS claims, library function names.
Method: documentation only; no commands were run.
