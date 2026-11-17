---
id: computing-software.cryptography-implementation.libsodium.blake2b-salt-and-personalisation
name: blake2b-salt-and-personalisation
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, blake2b-personal, blake2b, libsodium, domain-separation, crypto-generichash]
level: advanced
status: verified
description: "Use BLAKE2b salt and personalisation parameters in libsodium for domain separation: crypto_generichash_blake2b_salt_personal, sizes, and key derivation uses."
sources: ["https://doc.libsodium.org/hashing/generic_hashing", "https://www.rfc-editor.org/rfc/rfc7693", "https://www.blake2.net/blake2.pdf", "https://zips.z.cash/zip-0143"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BLAKE2b salt and personalisation

BLAKE2b's parameter block includes a 16-byte salt and 16-byte personalisation field. Different values give
independent hash functions, a cheap form of domain separation.

## API
```c
unsigned char out[32];
unsigned char salt[crypto_generichash_blake2b_SALTBYTES] = {0};          /* 16 */
unsigned char personal[crypto_generichash_blake2b_PERSONALBYTES] = "myapp-v1-idhash"; /* 16, zero padded */
crypto_generichash_blake2b_salt_personal(out, sizeof out, in, inlen,
                                         key, keylen,            /* may be NULL, 0 */
                                         salt, personal);
```
Multi-part: `crypto_generichash_blake2b_init_salt_personal`.

## Uses
- Domain-separate hashes of the same input for different purposes (Zcash uses personalisation strings
  extensively, e.g. `ZcashPrevoutHash` in ZIP 143).
- libsodium's `crypto_kdf_derive_from_key` uses BLAKE2b keyed with the master key, the 8-byte little-endian subkey ID as salt and the context as personalisation (reproduced with `hashlib.blake2b`).
- Keyed BLAKE2b with personalisation as a MAC per protocol message type.

## Rules
- Fields are fixed 16 bytes; shorter strings are zero padded, so `"abc"` and `"abc\0"` collide. Use fixed-length
  labels.
- Salt here is not a password salt; for passwords use `crypto_pwhash`.
- RFC 7693 does not define these fields (it calls salting and personalisation optional features not defined there), so
  check the peer library can set them (Python `hashlib.blake2b(salt=..., person=...)` can).

## Verify
- [ ] Python `hashlib.blake2b(data, digest_size=32, salt=s, person=p)` matches libsodium output (checked against PyNaCl 1.6.2 `crypto_generichash_blake2b_salt_personal`; short labels are zero padded, so `b'abc'` and `b'abc\0'` give the same hash).
