---
id: computing-software.cryptography-implementation.libsodium.ed25519-to-curve25519-conversion
name: ed25519-to-curve25519-conversion
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, crypto-sign, ed25519-to-curve25519, crypto-sign-ed25519-pk-to-curve25519, x25519, key-reuse, ssh-keys, age]
level: advanced
status: docs-checked
description: "Convert Ed25519 keys to X25519 with libsodium (crypto_sign_ed25519_pk_to_curve25519 / sk_to_curve25519): when it is acceptable, cross-protocol risks, and better alternatives."
sources: ["https://doc.libsodium.org/advanced/ed25519-curve25519", "https://eprint.iacr.org/2021/509", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/crypto_sign/ed25519/ref10/keypair.c"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ed25519 to Curve25519 conversion

Ed25519 (signatures) and X25519 (key exchange) use birationally equivalent
curves, so an Ed25519 key pair can be mapped to an X25519 key pair:

```c
unsigned char x_pk[crypto_scalarmult_curve25519_BYTES];
unsigned char x_sk[crypto_scalarmult_curve25519_BYTES];
if (crypto_sign_ed25519_pk_to_curve25519(x_pk, ed_pk) != 0) { /* rejected key */ }
crypto_sign_ed25519_sk_to_curve25519(x_sk, ed_sk);
```

## When it is reasonable

- You only have users' Ed25519 identity keys (for example a published signing
  key) and need to encrypt to them.
- Legacy protocols already deployed with one key pair.

## Why to avoid it in new designs

- **Key reuse across protocols**: the same secret is used for signing and for
  DH. Proofs for each scheme assume independent keys; joint security of
  Ed25519 + X25519 with one key is analysed in Thormarker 2021 (cited by the libsodium docs),
  which also closes off future changes and
  complicates rotation (rotating encryption rotates identity). The libsodium docs still recommend distinct keys
  if you can afford them: signing keys are usually long-term, key-exchange keys ideally ephemeral.
- The public-key conversion returns -1 for an invalid point, a small-order point, or a point outside the main subgroup (per the source of `crypto_sign_ed25519_pk_to_curve25519`); handle the error.
- `crypto_sign_ed25519_sk_to_curve25519` reads only the first 32 bytes (the seed) of the 64-byte secret key.
- Compromise of one use compromises both.

## Better

Generate separate X25519 keys and **sign** them with the Ed25519 identity key.
Recipients verify the signature, then encrypt
to the X25519 key. You get independent rotation and clean separation.
Another option from the docs: do the ECDH over the Edwards curve with `crypto_scalarmult_ed25519()` and skip the conversion.

## Verify

- [ ] Conversion return values checked.
- [ ] Design document notes why one key pair is reused, or uses signed X25519 keys instead.
- [ ] Encryption to converted keys round-trips with the converted secret key.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed against the doc page and keypair.c: function names and signatures, return -1 conditions, sk conversion reading only the 32-byte seed, the distinct-keys recommendation, the scalarmult_ed25519 alternative and the Thormarker reference. Removed unconfirmed claims about PyNaCl, age, minisign and Signal.

Method: documentation only; no commands were run.
