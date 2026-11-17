---
id: computing-software.cryptography-implementation.libsodium.crypto-kdf-context-strings-and-subkey-ids
name: crypto-kdf-context-strings-and-subkey-ids
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, kdf-context-string, crypto-kdf, crypto-kdf-derive, libsodium, subkeys, key-hierarchy, blake2b]
level: practitioner
status: verified
description: "Derive subkeys with crypto_kdf_derive_from_key: 8-byte context strings, subkey id allocation, subkey lengths 16-64, versioning, and when to use HKDF instead."
sources: ["https://doc.libsodium.org/key_derivation", "https://doc.libsodium.org/key_derivation#deriving-keys-from-a-single-high-entropy-key", "https://doc.libsodium.org/key_derivation/hkdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# crypto_kdf context strings and subkey ids

```c
unsigned char master[crypto_kdf_KEYBYTES];          /* 32 bytes, from crypto_kdf_keygen or a KMS */
unsigned char k_enc[32], k_mac[32];
crypto_kdf_derive_from_key(k_enc, sizeof k_enc, 1, "ORDERS__", master);
crypto_kdf_derive_from_key(k_mac, sizeof k_mac, 2, "ORDERS__", master);
```
- `ctx` is exactly `crypto_kdf_CONTEXTBYTES` (8) bytes; it does not need to be secret or NUL-terminated. Pad
  shorter names deliberately ("ORDERS__").
- `subkey_id` is a 64-bit integer; up to 2^64 subkeys per (master, context).
- Subkey length between `crypto_kdf_BYTES_MIN` (16) and `crypto_kdf_BYTES_MAX` (64).
- Built on BLAKE2b with the master key as key, subkey id (8 bytes little-endian, zero padded to 16) as salt and context (zero padded to 16) as personalisation: `hashlib.blake2b(b'', digest_size=32, key=master, salt=id_le8+bytes(8), person=ctx+bytes(8))` equals libsodium.js's `crypto_kdf_derive_from_key`. A 6-byte context was rejected (`invalid ctx length`).

## Allocating ids
- Keep a table in code: `1 = record encryption`, `2 = record MAC`, `3 = search index`. Never reuse an id for a new
  purpose; deprecate and add.
- For per-entity keys, use the entity's numeric id as `subkey_id` under a dedicated context (`"USERKEYS"`), so a
  user's key is derivable on demand and never stored.
- Version by context: `"ORDERSv2"` changes every subkey.

## Limits and alternatives
- Inputs must be a uniformly random 32-byte master key; not a password (use `crypto_pwhash` first) and not a raw DH
  output (use `crypto_kx` or HKDF).
- Need longer info strings, standard interop, or arbitrary output length: `crypto_kdf_hkdf_sha256_*` (libsodium
  1.0.19+).

## Verify
- [ ] Different ids and contexts yield different subkeys (unit test).
- [ ] Id table is documented and append-only.
