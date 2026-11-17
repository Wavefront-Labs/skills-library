---
id: computing-software.cryptography-implementation.key-management.aes-key-wrap-kw-kwp
name: aes-key-wrap-kw-kwp
category: computing-software
field: cryptography-implementation
product: key-management
tags: [cryptography-implementation, key-management, storage-encryption-modes, aes-key-wrap, aes-kw, aes-kwp, sp-800-38f, rfc3394, rfc5649, key-wrapping, kek, pkcs11-wrap]
level: advanced
status: verified
description: "Wrap keys under a KEK with AES-KW (RFC 3394) or AES-KWP (RFC 5649): when to pick each, library calls, HSM interop, and why not to use GCM or ECB for key wrapping."
sources: ["https://csrc.nist.gov/pubs/sp/800/38/f/final", "https://datatracker.ietf.org/doc/html/rfc3394", "https://datatracker.ietf.org/doc/html/rfc5649", "https://cryptography.io/en/latest/hazmat/primitives/keywrap/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AES key wrap (KW and KWP)

Key wrap is deterministic authenticated encryption designed for key material:
no nonce to manage, and integrity via an integrity check value. SP 800-38F
approves KW (RFC 3394) and KWP (RFC 5649, with padding).

| | AES-KW | AES-KWP |
|---|---|---|
| Input length | multiple of 8 bytes, >= 16 (the `cryptography` library enforces >= 16) | 1 byte up to (not including) 2^32 bytes (SP 800-38F 5.3.1) |
| Output | input + 8 bytes | padded to multiple of 8, + 8 bytes |
| Default IV | `A6A6A6A6A6A6A6A6` | `A65959A6` + 32-bit length |
| Typical use | wrapping AES keys | wrapping RSA/EC private keys (PKCS#8), odd lengths |

## Code

```python
from cryptography.hazmat.primitives.keywrap import aes_key_wrap, aes_key_unwrap, \
    aes_key_wrap_with_padding, aes_key_unwrap_with_padding, InvalidUnwrap
wrapped = aes_key_wrap(kek, dek)               # dek 16/24/32 bytes
dek = aes_key_unwrap(kek, wrapped)             # raises InvalidUnwrap on tamper
w = aes_key_wrap_with_padding(kek, pkcs8_der)  # KWP for private keys
```

OpenSSL 3: cipher `AES-256-WRAP` / `AES-256-WRAP-PAD` (also `id-aes256-wrap`; listed by `openssl enc -list`); in the C API
`EVP_CIPHER_CTX_set_flags(ctx, EVP_CIPHER_CTX_FLAG_WRAP_ALLOW)` was required on 1.1.x and is documented in 3.0 as legacy-only.
Java: `Cipher.getInstance("AESWrap")` / `"AESWrapPad"` (JDK 17+ also
`AES/KW/NoPadding`, `AES/KWP/NoPadding`) with `Cipher.WRAP_MODE`.
PKCS#11: `CKM_AES_KEY_WRAP` (RFC 3394 KW) and `CKM_AES_KEY_WRAP_KWP` (added in v3.0;
same results as RFC 5649). Do not confuse the padded variants: the older
`CKM_AES_KEY_WRAP_PAD` (already in v2.40) PKCS#7-pads the input and then applies plain KW, so its
output is not interoperable with KWP/RFC 5649. Check which mechanism the HSM implements before assuming interop.

## Rules

- KEK strength must be >= the wrapped key's strength (do not wrap AES-256
  keys or P-384 keys with an AES-128 KEK; SP 800-57 Part 1 Rev. 5 Table 2 comparable
  strengths).
- Deterministic: wrapping the same key twice gives the same output. Fine for
  keys (high entropy, unique), not for general data - do not use KW as a data
  encryption mode.
- A KEK is used only for wrapping, never also for data encryption.
- Store with the wrapped key: KEK identifier/version, algorithm, and what the
  key is for. KW has no associated-data input; if you need to bind context,
  use an AEAD wrap (e.g. AES-GCM with the key id as AAD, as JWE `A256GCMKW`
  does) or a KMS `encryption context`.
- Why not ECB: no integrity, and swapping blocks between wrapped keys goes
  undetected. Why not plain GCM: needs a unique nonce per wrap; KW avoids that
  failure mode.

## Verify

- [ ] RFC 3394 section 4 and RFC 5649 section 6 test vectors pass.
- [ ] Flipping one byte of a wrapped key raises the unwrap error.
- [ ] KEK size >= wrapped key strength; KEK used only for wrapping.
- [ ] Wrapped key record stores KEK id/version for rotation.
