---
id: computing-software.cryptography-implementation.libsodium.deterministic-keypairs-from-seeds
name: deterministic-keypairs-from-seeds
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, crypto-sign, crypto-sign-seed-keypair, crypto-box-seed-keypair, seed, key-derivation, crypto-kdf, backup-phrase, deterministic-keys]
level: advanced
status: docs-checked
description: "Derive Ed25519/X25519 key pairs from 32-byte seeds with crypto_sign_seed_keypair and crypto_box_seed_keypair: deriving seeds with crypto_kdf, storing seeds, and recovery uses."
sources: ["https://doc.libsodium.org/public-key_cryptography/public-key_signatures", "https://doc.libsodium.org/public-key_cryptography/authenticated_encryption", "https://doc.libsodium.org/key_exchange", "https://doc.libsodium.org/key_derivation", "https://doc.libsodium.org/quickstart"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deterministic key pairs from seeds

libsodium can build a key pair from a 32-byte seed:

```c
crypto_sign_seed_keypair(pk, sk, seed);   /* Ed25519; seed = first 32 bytes of sk */
crypto_box_seed_keypair(pk, sk, seed);    /* X25519 */
crypto_kx_seed_keypair(pk, sk, seed);
crypto_sign_ed25519_sk_to_seed(seed, sk); /* recover the seed from a signing key */
```

## Uses

- **Compact storage**: store 32 bytes instead of the 64-byte signing key.
- **Many keys from one root**: derive per-purpose or per-device seeds from a
  master key, so only the master needs backup.
- **Recovery phrases**: a high-entropy secret encoded as words can regenerate the
  identity keys.

## Deriving seeds properly

```c
unsigned char master[crypto_kdf_KEYBYTES];        /* 32 random bytes, backed up */
unsigned char seed[32];
crypto_kdf_derive_from_key(seed, sizeof seed, /*subkey_id*/ 1, "SIGNKEY_", master);
crypto_sign_seed_keypair(pk, sk, seed);
sodium_memzero(seed, sizeof seed);
```

- Context is an 8-character string (`crypto_kdf_CONTEXTBYTES`); subkey ids go up to 2^64-1 and subkey
  lengths run from `crypto_kdf_BYTES_MIN` to `crypto_kdf_BYTES_MAX` (16 to 64 bytes); different
  contexts/ids give independent seeds.
- Never derive seeds from passwords directly. If a human secret is the root,
  stretch it with `crypto_pwhash` (Argon2id, high limits, random stored
  salt) to get the master key; accept that the identity is then only as strong
  as the passphrase.
- Prefer separate seeds for signing and encryption keys, derived with different
  subkey ids. (The libsodium FAQ notes `crypto_sign_seed_keypair` and
  `crypto_kx_seed_keypair` can both derive from one 32-byte seed; separate seeds keep the keys independent.)

## Pitfalls

- The seed **is** the private key: protect it exactly like `sk`
  (`sodium_malloc`, `sodium_memzero`, no logging).
- Deterministic derivation means compromise of the master compromises all
  derived keys at once; rotate by changing the master and re-registering
  public keys.
- Libraries differ in what they call the "private key": libsodium's 64-byte
  `sk` vs other libraries' 32-byte seed. Convert via the seed, not by
  truncating arbitrary formats.

## Verify

- [ ] Same seed reproduces the same public key across restarts.
- [ ] Seeds come from `crypto_kdf`/`randombytes_buf`/`crypto_pwhash`, never raw passwords.
- [ ] Different purposes use different subkey ids/contexts.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: seed_keypair functions for sign, box and kx; sk holds seed and public key with sk_to_seed available; crypto_kdf context of 8 characters, subkey id up to 2^64-1, subkey length 16 to 64 bytes. Removed an unconfirmed claim about how crypto_box derives its key from the seed and a test-vector reference.

Method: documentation only; no commands were run.
