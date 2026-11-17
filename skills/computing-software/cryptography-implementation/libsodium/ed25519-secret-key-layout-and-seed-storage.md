---
id: computing-software.cryptography-implementation.libsodium.ed25519-secret-key-layout-and-seed-storage
name: ed25519-secret-key-layout-and-seed-storage
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, crypto-sign-ed25519-sk-to-pk, ed25519-seed-storage, crypto-sign, ed25519, libsodium, key-storage, double-public-key-attack]
level: practitioner
status: docs-checked
description: "Handle libsodium Ed25519 64-byte secret keys: seed versus seed||pk layout, sk_to_seed and sk_to_pk, store only seeds, and avoid the mismatched public key oracle."
sources: ["https://doc.libsodium.org/public-key_cryptography/public-key_signatures", "https://www.rfc-editor.org/rfc/rfc8410", "https://github.com/golang/go/blob/master/src/crypto/ed25519/ed25519.go", "https://github.com/MystenLabs/ed25519-unsafe-libs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ed25519 secret key layout and seed storage

## Layout
libsodium's `crypto_sign_SECRETKEYBYTES` (64) secret key is the 32-byte seed followed by the 32-byte public key. The docs note the public key is stored because precomputing it saves signing CPU cycles. RFC 8032 defines the
private key as just the 32-byte seed; the expanded scalar and prefix are derived from SHA-512(seed) at signing time.
```c
unsigned char seed[crypto_sign_SEEDBYTES], pk[crypto_sign_PUBLICKEYBYTES], sk[crypto_sign_SECRETKEYBYTES];
crypto_sign_ed25519_sk_to_seed(seed, sk);
crypto_sign_ed25519_sk_to_pk(pk, sk);
crypto_sign_seed_keypair(pk, sk, seed);     /* regenerate from the seed */
```

## Store the seed only
- 32 bytes to protect, back up, wrap with a KMS, or derive from a KDF.
- Regenerating the public key from the seed guarantees they match.

## Formats elsewhere
| System | Private key representation |
|---|---|
| RFC 8410 PKCS#8 (OpenSSL) | 32-byte seed |
| Go `ed25519.PrivateKey` | 64 bytes, seed then public key; `ed25519.NewKeyFromSeed(seed)` |

## The mismatched public key oracle
Some libraries accept the public key as a separate signing argument (or trust the second half of a 64-byte sk). If an
attacker can get signatures over the same message with the right seed but a **different** public key, they can
recover the private scalar. The MystenLabs ed25519-unsafe-libs list, reported in 2022, counted 45 affected libraries as of May 2023. libsodium's `crypto_sign_detached` and `crypto_sign` take only the secret key, so no separate public key argument exists. Rules:
- Never let callers supply the public key separately from the secret key at signing time.
- If you load 64-byte keys from storage, recompute the public key from the seed and compare.

## Verify
- [ ] Persisted key material is 32-byte seeds (wrapped/encrypted at rest).
- [ ] Loading a 64-byte key with a tampered public half is rejected.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: libsodium secret key contains the seed and public key, extraction via sk_to_seed and sk_to_pk, signing functions take only sk; Go layout and NewKeyFromSeed; RFC 8410 seed-only PKCS#8; the MystenLabs list (45 libraries, updated May 2023). Removed unconfirmed JWK, PyNaCl, TweetNaCl and OpenSSH rows. The RFC 8032 seed statement is supported by the Go source comment that seeds are the private key representation used by RFC 8032.

Method: documentation only; no commands were run.
