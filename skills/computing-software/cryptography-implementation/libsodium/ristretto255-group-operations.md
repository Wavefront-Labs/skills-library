---
id: computing-software.cryptography-implementation.libsodium.ristretto255-group-operations
name: ristretto255-group-operations
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, libsodium-advanced, ristretto255, prime-order-group, crypto-core-ristretto255, oprf, pake, rfc9496, cofactor]
level: sme
status: docs-checked
description: "Build protocols on ristretto255 in libsodium: prime-order group API, hash-to-group, scalar ops, point validation, and when you need it (OPRFs, PAKEs, blind signatures)."
sources: ["https://doc.libsodium.org/advanced/ristretto", "https://www.rfc-editor.org/rfc/rfc9496", "https://www.rfc-editor.org/rfc/rfc9497", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/crypto_scalarmult/ristretto255/ref10/scalarmult_ristretto255_ref10.c"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ristretto255 group operations

Curve25519 has cofactor 8; protocols that need a prime-order group (OPRFs,
PAKEs like OPAQUE, zero-knowledge proofs, threshold schemes) break in subtle
ways on it. ristretto255 (RFC 9496) encodes a prime-order group on top of
Curve25519 so every valid encoding is a group element of order L and
encodings are canonical.

## API (libsodium 1.0.18 and later)

```c
unsigned char p[crypto_core_ristretto255_BYTES];            /* 32 */
unsigned char r[crypto_core_ristretto255_SCALARBYTES];      /* 32 */
unsigned char h[crypto_core_ristretto255_HASHBYTES];        /* 64 */

crypto_core_ristretto255_scalar_random(r);
crypto_scalarmult_ristretto255_base(p, r);                  /* p = r*G */
crypto_core_ristretto255_from_hash(p, h);                   /* hash-to-group from 64 uniform bytes */
crypto_core_ristretto255_is_valid_point(p);                 /* 1 if canonical (docs: only checks canonical form) */
crypto_core_ristretto255_add(out, p, q);
crypto_core_ristretto255_scalar_invert(rinv, r);            /* for blinding/unblinding */
if (crypto_scalarmult_ristretto255(out, r, p) != 0) { /* result is identity: reject */ }
```

`from_hash` maps a 64-byte vector, usually the output of a hash function: derive it from the
input and a domain separation tag (`crypto_generichash` with 64-byte output,
or the RFC 9380 `expand_message_xmd` with SHA-512 if you need interop with RFC 9497 OPRFs).

## Rules

- Validate every received point with `is_valid_point` (or rely on functions
  that return -1: `add` and `sub` return -1 for invalid encodings, and `crypto_scalarmult_ristretto255` fails when the point does not decode or the result is the identity) before use.
- Reject the identity element where the protocol requires non-trivial values.
- Do not mix ristretto255 encodings with Ed25519/X25519 encodings; they are
  different byte strings for related points.
- Scalars must be in the range 0 to L-1; use `crypto_core_ristretto255_scalar_reduce` on 64-byte (`crypto_core_ristretto255_NONREDUCEDSCALARBYTES`) values, which should be sampled from an interval of at least 317 bits for near-uniformity. The top bit of an encoding is unused (the docs say applications may use it for extra data or reject it).

## Example: blinded evaluation (OPRF core)

Client: `B = r * H(x)`; server: `Z = k * B`; client: `N = r^-1 * Z = k * H(x)`.
The server never sees `x`; the client learns `k*H(x)` without learning `k`.
(The libsodium docs show a different blinding example that computes `p(x) * g^r` with `crypto_core_ristretto255_add`.)
For production use an RFC 9497 implementation (adds proofs and domain
separation) rather than this sketch.

## Verify

- [ ] RFC 9496 Appendix A vectors (multiples of the generator, invalid encodings, group elements from uniform byte strings) reproduce.
- [ ] Invalid/non-canonical encodings rejected.
- [ ] Protocol uses an existing standard (OPAQUE, OPRF) where one fits.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: ristretto255 added in 1.0.18; function names and return values (is_valid_point checks canonical form only, from_hash takes 64 bytes, scalarmult returns -1 for identity, add and sub return -1 for invalid encodings, scalar_reduce with a 317-bit note, scalar_random in the open interval 0 to L); scalarmult failing on undecodable points (source); RFC 9496 title, group order and Appendix A contents; RFC 9497 ristretto255-SHA512 using RFC 9380 hash_to_ristretto255 with expand_message_xmd and SHA-512. The doc page URL for the ristretto page replaces a wrong path in sources.

Method: documentation only; no commands were run.
