---
id: computing-software.cryptography-implementation.libsodium.libsodium-keygen-helpers-and-key-sizes
name: libsodium-keygen-helpers-and-key-sizes
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, secretbox, sodium-keygen, key-sizes, keybytes-constants, crypto-secretbox-keygen, key-generation, size-checks]
level: practitioner
status: docs-checked
description: "Generate and size libsodium keys correctly: the *_keygen helpers, *_KEYBYTES/NONCEBYTES constants, checking lengths when importing keys, and storing keys from bindings."
sources: ["https://doc.libsodium.org/secret-key_cryptography/secretbox", "https://doc.libsodium.org/key_derivation", "https://doc.libsodium.org/helpers", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/include/sodium/crypto_secretbox_xsalsa20poly1305.h", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/include/sodium/crypto_aead_aegis256.h", "https://github.com/pyca/pynacl/blob/main/src/nacl/secret.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# libsodium keygen helpers and key sizes

Every libsodium secret-key construction has a `*_keygen()` that fills a
buffer of `*_KEYBYTES` from the CSPRNG. Use them instead of hand-sizing
`randombytes_buf` calls, so key sizes follow the construction.

## Helpers and sizes

| Construction | Keygen | Key | Nonce |
|---|---|---|---|
| `crypto_secretbox` | `crypto_secretbox_keygen` | 32 | 24 |
| `crypto_aead_xchacha20poly1305_ietf` | `..._keygen` | 32 | 24 |
| `crypto_aead_aegis256` | `..._keygen` | 32 | 32 |
| `crypto_secretstream_xchacha20poly1305` | `..._keygen` | 32 | header 24 |
| `crypto_auth` | `crypto_auth_keygen` | 32 | - |
| `crypto_generichash` | `crypto_generichash_keygen` | 32 (16-64 allowed) | - |
| `crypto_kdf` | `crypto_kdf_keygen` | 32 | - |
| `crypto_shorthash` | `crypto_shorthash_keygen` | 16 | - |
| Public-key pairs | `crypto_box_keypair`, `crypto_sign_keypair`, `crypto_kx_keypair` | 32 pk / 32 or 64 sk | - |

Always size buffers with the constants (`crypto_secretbox_KEYBYTES`), never
literal numbers; constants document intent and survive construction changes.

## Importing keys

Keys arriving from configuration, KMS unwraps, or other languages must be
length-checked before use:

```c
if (sodium_base642bin(key, sizeof key, b64, strlen(b64), NULL, &len, NULL,
                      sodium_base64_VARIANT_ORIGINAL) != 0 || len != crypto_secretbox_KEYBYTES) {
    /* reject: wrong encoding or size */
}
```

Bindings: PyNaCl `nacl.secret.SecretBox(key)` raises `ValueError` when the key is not exactly
`SecretBox.KEY_SIZE` (32) bytes. A common bug is passing a
hex or base64 string (64/44 chars) where 32 raw bytes are expected.

## Storage

- Keep keys in `sodium_malloc` buffers for long-lived secrets; `sodium_memzero`
  stack copies after use.
- Serialise with `sodium_bin2hex`/`sodium_hex2bin`, which the docs describe as constant time for a given size (the docs make no such statement for the base64 helpers).
- Derive per-purpose subkeys from one stored master key with `crypto_kdf`
  instead of storing many keys.

## Verify

- [ ] All key buffers sized from `*_KEYBYTES` constants.
- [ ] Imported keys length-checked after decoding.
- [ ] Keys generated with `*_keygen`/`randombytes_buf`, never from passwords without `crypto_pwhash`.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed from the C headers: key and nonce sizes for secretbox (32/24), XChaCha20-Poly1305 IETF (32/24), AEGIS-256 (32/32), secretstream header (24, the XChaCha20 nonce size), crypto_auth (32), crypto_kdf (32), generichash (32, 16 to 64), shorthash key (16); crypto_box keys 32 and Ed25519 secret key 64; sodium_base642bin signature and constant-time hex and base64 helpers (docs); PyNaCl SecretBox KEY_SIZE and ValueError on wrong length. Removed an unconfirmed libsodium.js error message and a claim about wrappers truncating keys.

Method: documentation only; no commands were run.
