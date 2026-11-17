---
id: computing-software.cryptography-implementation.libsodium.libsodium-hkdf-sha256-sha512
name: libsodium-hkdf-sha256-sha512
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, crypto-kdf, crypto-kdf-hkdf, hkdf, rfc5869, hkdf-sha256, key-derivation, interop]
level: advanced
status: docs-checked
description: "Use libsodium's HKDF (crypto_kdf_hkdf_sha256/sha512, 1.0.19+): extract/expand API, when to prefer it over crypto_kdf, output limits, and matching other libraries' HKDF output."
sources: ["https://doc.libsodium.org/key_derivation/hkdf", "https://datatracker.ietf.org/doc/html/rfc5869", "https://github.com/jedisct1/libsodium/blob/master/src/libsodium/crypto_kdf/hkdf/kdf_hkdf_sha256.c"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HKDF in libsodium

libsodium 1.0.19 added standard HKDF (RFC 5869) with SHA-256 and SHA-512.
`crypto_kdf_derive_from_key` (BLAKE2b-based, 8-char context, 64-bit subkey id)
remains the simplest choice inside libsodium-only systems; use HKDF when you
must interoperate with other implementations of standard protocols that use HKDF, need contexts longer than 8 characters, or
derive from input keying material that is not uniform.

## API

```c
unsigned char prk[crypto_kdf_hkdf_sha256_KEYBYTES];          /* 32 */
crypto_kdf_hkdf_sha256_extract(prk, salt, saltlen, ikm, ikmlen);
unsigned char okm[32];
crypto_kdf_hkdf_sha256_expand(okm, sizeof okm, "myapp v1 enc key", 16, prk);
sodium_memzero(prk, sizeof prk);

/* multi-part extract for large or segmented IKM */
crypto_kdf_hkdf_sha256_state st;
crypto_kdf_hkdf_sha256_extract_init(&st, salt, saltlen);
crypto_kdf_hkdf_sha256_extract_update(&st, part1, len1);
crypto_kdf_hkdf_sha256_extract_final(&st, prk);
```

`crypto_kdf_hkdf_sha512_*` mirrors this by replacing the prefix; the docs say SHA-256 is generally recommended and SHA-512 has no practical security benefit.

## Limits and rules

- Max output per expand: 255 * hash length (8160 bytes for SHA-256);
  `crypto_kdf_hkdf_sha256_BYTES_MAX`. Expand returns -1 (errno EINVAL) if exceeded - check it.
- Extract when the IKM is not uniform: the salt is optional (it may be NULL, has no minimum length, and can be a public unique protocol or application identifier); the IKM needs some entropy because extract only packs it. If a uniformly random key of the right size is already available (the docs say a `crypto_kx_*` output qualifies), skip extract and use it as the PRK.
- The context argument (`info`) need not be secret but must differ per derived key; include protocol
  name, version and purpose. Unlike `crypto_kdf_derive_from_key`, it can be any length (the docs note expand is slower).
- Output from libsodium HKDF equals any RFC 5869 implementation for identical
  salt/ikm/info; `crypto_kdf_derive_from_key` output does not (different
  construction).

## Verify

- [ ] RFC 5869 test vectors reproduce with the SHA-256 functions.
- [ ] Return values checked; output length within BYTES_MAX.
- [ ] Each derived key uses a distinct info string.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: HKDF added in 1.0.19, extract/expand/incremental extract signatures, KEYBYTES and BYTES_MAX (255 times the HMAC output), expand returning -1 with EINVAL above the maximum (source), salt optional, SHA-256 recommended over SHA-512, relation to crypto_kdf. Removed an unconfirmed list of interoperating protocols and a claim that DH output always needs extract.

Method: documentation only; no commands were run.
