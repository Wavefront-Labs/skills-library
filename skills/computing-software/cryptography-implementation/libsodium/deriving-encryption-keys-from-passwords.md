---
id: computing-software.cryptography-implementation.libsodium.deriving-encryption-keys-from-passwords
name: deriving-encryption-keys-from-passwords
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, crypto-pwhash, pwhash-key-derivation, argon2id, password-based-encryption, salt-storage, key-wrapping, crypto-pwhash-alg-argon2id13]
level: advanced
status: verified
description: "Derive a key from a passphrase with crypto_pwhash: store salt and limits, wrap a random data key instead of using the password key, change-password flow."
sources: ["https://doc.libsodium.org/password_hashing/default_phf#key-derivation", "https://datatracker.ietf.org/doc/html/rfc9106"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deriving encryption keys from passwords

`crypto_pwhash` (not `_str`) outputs raw key bytes from a password, salt and
cost parameters. Use it for password-protected files, vaults and local
databases.

```c
unsigned char salt[crypto_pwhash_SALTBYTES];      /* 16 */
randombytes_buf(salt, sizeof salt);
unsigned char kek[crypto_secretbox_KEYBYTES];
if (crypto_pwhash(kek, sizeof kek, pw, strlen(pw), salt,
                  crypto_pwhash_OPSLIMIT_SENSITIVE, crypto_pwhash_MEMLIMIT_SENSITIVE,
                  crypto_pwhash_ALG_ARGON2ID13) != 0) { /* out of memory */ }
```

## Store parameters with the ciphertext

The decryptor needs: algorithm id, opslimit, memlimit, salt. Libsodium does
not store them for you in raw mode. Header example:

```
magic "MYVAULT1" | alg (1) | opslimit (8, LE) | memlimit (8, LE) | salt (16) | nonce (24) | wrapped DEK (32+16)
```

Authenticate the header as associated data (XChaCha20-Poly1305 AEAD) so
parameters cannot be downgraded to cheap values by an attacker who can edit
the file.

## Wrap a random data key; do not encrypt data with the password key

1. Generate a random DEK (`crypto_aead_xchacha20poly1305_ietf_keygen`).
2. Encrypt data with the DEK.
3. Encrypt (wrap) the DEK with the password-derived KEK.

Benefits: changing the password re-wraps 48 bytes instead of re-encrypting all
data; several passwords or a recovery key can each wrap the same DEK; the
KDF runs once per unlock, not per item.

## Parameters

Interactive unlock of a local vault can afford SENSITIVE (1 GiB, slow: 2.2 s on the review host, PyNaCl `argon2id.kdf` with ops 4)
on desktops; mobile and browsers need MODERATE or tuned values. Raising
parameters later = re-wrap the DEK with new salt/limits at the next unlock.

## Pitfalls

- A key derived from a weak password is weak, whatever the KDF. Enforce
  length or offer passphrase generation.
- Same salt for two files with the same password gives the same KEK; use a
  fresh salt per vault (and per password change).
- Never store the derived key; store only salt/params and wrapped DEK.

## Verify

- [ ] Header stores alg, limits and salt, and is authenticated as AD.
- [ ] Password change re-wraps the DEK without touching data.
- [ ] Downgrading opslimit in the header causes decryption failure.
