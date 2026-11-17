---
id: computing-software.cryptography-implementation.libsodium.ristretto255-hash-to-group-and-oprf
name: ristretto255-hash-to-group-and-oprf
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, hash-to-group, ristretto255, crypto-core-ristretto255, oprf, rfc-9497, rfc-9496, libsodium, blinding]
level: sme
status: docs-checked
description: "Build OPRF and blind-signature style protocols on libsodium ristretto255: from_hash with domain-separated input, scalar ops, blinding and unblinding, validity checks."
sources: ["https://doc.libsodium.org/advanced/ristretto", "https://www.rfc-editor.org/rfc/rfc9496", "https://www.rfc-editor.org/rfc/rfc9497"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ristretto255 hash-to-group and OPRF

ristretto255 (RFC 9496) gives a prime-order group on Curve25519 with no cofactor pitfalls; libsodium exposes it for
building protocols such as OPRFs (RFC 9497), PAKEs and anonymous credentials.

## Hash to group
```c
unsigned char h[crypto_core_ristretto255_HASHBYTES];      /* 64 bytes */
unsigned char P[crypto_core_ristretto255_BYTES];          /* 32 bytes */
crypto_generichash_state st;                              /* domain-separate the input */
crypto_generichash_init(&st, NULL, 0, sizeof h);
crypto_generichash_update(&st, (const unsigned char *)"example-oprf-v1", 15);
crypto_generichash_update(&st, input, input_len);
crypto_generichash_final(&st, h, sizeof h);
crypto_core_ristretto255_from_hash(P, h);
```
`from_hash` takes a 64-byte vector, usually a hash output; a hash with a protocol-specific prefix is a reasonable way to produce it. For strict RFC
9497 interop, implement `HashToGroup` as the RFC defines: `hash_to_ristretto255` from RFC 9380 with `expand_message_xmd` (SHA-512) and the DST `"HashToGroup-"` followed by the context string `"OPRFV1-"`, the mode byte, `"-ristretto255-SHA512"`.

## OPRF flow (client input x, server key k)
```c
/* client: blind */
crypto_core_ristretto255_scalar_random(r);
crypto_scalarmult_ristretto255(B, r, P);                 /* B = r * H(x), send B */
/* server: evaluate */
if (crypto_scalarmult_ristretto255(Z, k, B) != 0) reject();   /* -1 if result is the identity or B is invalid */
/* client: unblind */
crypto_core_ristretto255_scalar_invert(rinv, r);
crypto_scalarmult_ristretto255(N, rinv, Z);              /* N = k * H(x) */
/* output = Hash(x || N) with a finalisation label */
```

## Checks
- Validate received points: `crypto_core_ristretto255_is_valid_point(B)` before use (scalarmult returns -1 for an undecodable point). `is_valid_point` only checks canonical form.
- Reject the identity element (`crypto_scalarmult_ristretto255` returns -1 when the result is the identity).
- Server key `k` from `crypto_core_ristretto255_scalar_random` (range 0 to L exclusive, so never zero).

## Gotchas
- In RFC 9497's OPRF mode the client cannot verify which key the server used; the verifiable (VOPRF) mode adds a proof that the key matches the public key the client already has. Use it if that matters.
- Use an existing OPRF or OPAQUE library when one exists for your language; this is for when you must build on
  primitives.

## Verify
- [ ] Unblinded result equals a direct `k * H(x)` computed in a test.
- [ ] Identity and invalid points are rejected.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: libsodium ristretto255 function behaviour (docs and scalarmult_ristretto255_ref10.c); RFC 9497 title (Oblivious Pseudorandom Functions Using Prime-Order Groups), the ristretto255-SHA512 HashToGroup definition and DST construction, the OPRF versus VOPRF distinction; RFC 9496 title. The sources entry for the libsodium page used a wrong path and is replaced.

Method: documentation only; no commands were run.
