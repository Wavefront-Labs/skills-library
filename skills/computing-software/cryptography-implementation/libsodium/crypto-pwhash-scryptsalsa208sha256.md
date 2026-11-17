---
id: computing-software.cryptography-implementation.libsodium.crypto-pwhash-scryptsalsa208sha256
name: crypto-pwhash-scryptsalsa208sha256
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, crypto-pwhash-scryptsalsa208sha256, scrypt, libsodium, password-hashing, argon2id]
level: practitioner
status: verified
description: "Handle libsodium's scrypt API crypto_pwhash_scryptsalsa208sha256 for legacy hashes: parameters, str format, migrating to Argon2id via needs_rehash, and minimal builds."
sources: ["https://doc.libsodium.org/advanced/scrypt", "https://doc.libsodium.org/password_hashing/default_phf", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/Makefile.am"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crypto_pwhash_scryptsalsa208sha256

## Status
libsodium's default `crypto_pwhash` is Argon2id. The scrypt API remains for compatibility with existing hashes
and other systems; it is excluded from `--enable-minimal` builds (Makefile.am lists the scrypt sources under `if !MINIMAL`).

## API
```c
char out[crypto_pwhash_scryptsalsa208sha256_STRBYTES];
crypto_pwhash_scryptsalsa208sha256_str(out, pw, pwlen,
    crypto_pwhash_scryptsalsa208sha256_OPSLIMIT_INTERACTIVE,
    crypto_pwhash_scryptsalsa208sha256_MEMLIMIT_INTERACTIVE);   /* 524288 ops, 16 MiB */
crypto_pwhash_scryptsalsa208sha256_str_verify(out, pw, pwlen);  /* 0 on match */
```
`_SENSITIVE` limits use 1 GiB (memlimit 1073741824, opslimit 33554432). A generated string started with `$7$` and was 101 characters (STRBYTES 102 includes the NUL); other libraries use other string formats, so test cross-library verification before relying on it. The salt for the raw KDF is 32 bytes (`crypto_pwhash_scryptsalsa208sha256_SALTBYTES`).

## Migration to Argon2id
```c
if (crypto_pwhash_scryptsalsa208sha256_str_verify(stored, pw, pwlen) == 0) {
    crypto_pwhash_str(newh, pw, pwlen, OPSLIMIT, MEMLIMIT);   /* store newh */
}
```
Detect old hashes by prefix (`$7$` vs `$argon2id$`): `crypto_pwhash_str_verify` returned false for a `$7$` string, so the dispatch is yours. `crypto_pwhash_str_needs_rehash` is documented for the current default algorithm (returns 1, 0, or -1 on error); it reported nonzero for a `$7$` string.

## Key derivation
`crypto_pwhash_scryptsalsa208sha256(key, keylen, pw, pwlen, salt, ops, mem)` with a 32-byte salt; prefer
`crypto_pwhash` with Argon2id for new formats.

## Verify
- [ ] Legacy hashes verify; next login rewrites them as Argon2id.
