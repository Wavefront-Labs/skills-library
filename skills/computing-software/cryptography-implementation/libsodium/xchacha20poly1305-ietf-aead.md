---
id: computing-software.cryptography-implementation.libsodium.xchacha20poly1305-ietf-aead
name: xchacha20poly1305-ietf-aead
category: computing-software
field: cryptography-implementation
product: libsodium
tags: [cryptography-implementation, libsodium, crypto-aead, xchacha20poly1305-ietf, xchacha20-poly1305, aead, random-nonce, associated-data, crypto-aead-xchacha20poly1305-ietf-encrypt]
level: practitioner
status: docs-checked
description: "Encrypt with libsodium's crypto_aead_xchacha20poly1305_ietf: sizes, random 24-byte nonces, additional data, ciphertext layout, decrypt failure handling, and interop names."
sources: ["https://github.com/jedisct1/libsodium-doc/blob/master/secret-key_cryptography/xchacha20-poly1305_construction.md", "https://doc.libsodium.org/secret-key_cryptography/aead", "https://github.com/pyca/pynacl/blob/main/src/nacl/bindings/crypto_aead.py"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# XChaCha20-Poly1305-IETF in libsodium

The libsodium docs call this the recommended AEAD construction when interoperability with other libraries is not a concern: 256-bit key, 192-bit nonce (random nonces are safe because the collision probability is negligible, as long as the PRNG output is indistinguishable from random), 128-bit tag. It is not standardised but widely implemented.

## Sizes

| Constant | Bytes |
|---|---|
| `crypto_aead_xchacha20poly1305_ietf_KEYBYTES` | 32 |
| `crypto_aead_xchacha20poly1305_ietf_NPUBBYTES` | 24 |
| `crypto_aead_xchacha20poly1305_ietf_ABYTES` | 16 |
| `..._MESSAGEBYTES_MAX` | the docs give about 2^64 bytes per (key, nonce), no practical limit |

## C

```c
unsigned char key[crypto_aead_xchacha20poly1305_ietf_KEYBYTES];
unsigned char nonce[crypto_aead_xchacha20poly1305_ietf_NPUBBYTES];
crypto_aead_xchacha20poly1305_ietf_keygen(key);
randombytes_buf(nonce, sizeof nonce);
unsigned long long clen;
crypto_aead_xchacha20poly1305_ietf_encrypt(c, &clen, m, mlen, ad, adlen,
                                           NULL /* nsec, always NULL */, nonce, key);
/* store nonce || c (clen = mlen + ABYTES) */
if (crypto_aead_xchacha20poly1305_ietf_decrypt(m2, &mlen2, NULL, c, clen,
                                               ad, adlen, nonce, key) != 0) {
    /* forged or corrupted: reject, do not use m2 */
}
```

## Python (PyNaCl) and JS

```python
from nacl.bindings import crypto_aead_xchacha20poly1305_ietf_encrypt as enc, \
    crypto_aead_xchacha20poly1305_ietf_decrypt as dec
from nacl.utils import random
ct = enc(msg, aad, nonce := random(24), key)
pt = dec(ct, aad, nonce, key)   # raises nacl.exceptions.CryptoError ("Decryption failed.") on failure
```

libsodium.js: `sodium.crypto_aead_xchacha20poly1305_ietf_encrypt(msg, ad, null, nonce, key)`.

## Rules

- `nsec` is unused; pass NULL.
- Nonce: random per message is fine (a counter is also fine per the docs); it must never repeat for a key. Store it with the ciphertext (prefix).
- Put context (record id, version, user id) in `ad`; it is authenticated, not
  encrypted, not stored inside the ciphertext - the decryptor must supply the
  same bytes.
- Do not confuse with `crypto_aead_chacha20poly1305_ietf` (12-byte nonce; the docs allow 2^32 messages with random nonces) or the original `crypto_aead_chacha20poly1305`
  (8-byte nonce; 2^16 messages with random nonces).
- For large files/streams use `crypto_secretstream_xchacha20poly1305`, not one
  giant AEAD call.

## Verify

- [ ] Nonce length 24 and generated per message from `randombytes_buf`.
- [ ] Changing one byte of ad, nonce, ciphertext or tag makes decrypt return -1.
- [ ] Published XChaCha20-Poly1305 test vectors reproduce.

## Checked

2026-10-26, libsodium documentation (libsodium-doc, master) and libsodium source at 1.0.22 era master. Confirmed: encrypt and decrypt signatures, nsec NULL, ciphertext length up to mlen plus ABYTES, keygen since 1.0.12, random nonces acceptable for this construction, counters also fine, recommended AEAD when interoperability is not a concern, KEYBYTES 32, NPUBBYTES 24 and ABYTES 16 (docs and headers), message limit about 2^64 bytes, random-nonce limits for the other variants; PyNaCl bindings signature (message, aad, nonce, key) and CryptoError on failure. Removed unconfirmed speed and constant-time wording, an output-buffer remark and an IRTF draft vector reference; the source URL for the construction page is now the page's path in the documentation repository.

Method: documentation only; no commands were run.
