---
id: computing-software.cryptography-implementation.crypto-libraries.ciphertext-byte-layout-across-libraries
name: ciphertext-byte-layout-across-libraries
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, interoperability, ciphertext-byte-layout, aes-gcm, aead, wire-format]
level: practitioner
status: verified
description: "Make AEAD ciphertext decrypt across Java, Go, Python, Node, .NET and Web Crypto: where each puts nonce and tag, a fixed versioned layout, and cross-language test vectors."
sources: ["https://www.rfc-editor.org/rfc/rfc5116", "https://docs.oracle.com/en/java/javase/21/docs/api/java.base/javax/crypto/Cipher.html", "https://pkg.go.dev/crypto/cipher#AEAD", "https://nodejs.org/api/crypto.html#class-cipher", "https://cryptography.io/en/latest/hazmat/primitives/aead/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ciphertext byte layout across libraries

Most "it decrypts in Java but not in Node" bugs are layout bugs, not crypto bugs. Fix the
layout in a written spec and test it with vectors.

## What each API gives you (AES-GCM, 16-byte tag)
| Library | encrypt output | tag | nonce |
|---|---|---|---|
| Java `Cipher` "AES/GCM/NoPadding" | `ct || tag` | appended | separate (`GCMParameterSpec(128, iv)`) |
| Go `aead.Seal(dst, nonce, pt, aad)` | `dst || ct || tag` | appended | separate; idiom `Seal(nonce, nonce, ...)` prepends it |
| Python pyca `AESGCM.encrypt` | `ct || tag` | appended | separate |
| Web Crypto `encrypt({name:"AES-GCM"})` | `ct || tag` | appended | separate (`iv`) |
| Node `createCipheriv` | `ct` only | `cipher.getAuthTag()` separately | separate |
| .NET `AesGcm.Encrypt` | `ct` | separate `tag` span | separate |
| libsodium `crypto_aead_*_encrypt` | `ct || tag` | appended | separate |
| OpenSSL EVP | `ct` | `EVP_CTRL_GCM_GET_TAG` | separate |

Node and .NET users must concatenate or split the tag themselves; on decrypt Node needs
`decipher.setAuthTag(tag)` before `final()`.

Checked: Java `Cipher` Javadoc says the GCM tag is appended to the ciphertext on encryption (Java 8 run: 5 bytes of plaintext gave 21 bytes); Node `createCipheriv` gave a
5-byte body for 5 bytes of plaintext and a 16-byte `getAuthTag()`, and `crypto.subtle.encrypt` AES-GCM returned exactly
body || tag; Go `Seal` and pyca `AESGCM` interop was run (Go blob `nonce || ct || tag` decrypted by pyca); PyNaCl's
libsodium ChaCha20-Poly1305 and XChaCha20-Poly1305 outputs were plaintext length + 16 (appended tag); the .NET `AesGcm`
and OpenSSL EVP rows are from Microsoft Learn (separate tag span) and the OpenSSL 3.5 `EVP_EncryptInit` page
(`EVP_CTRL_AEAD_GET_TAG` after final); no .NET SDK was available.

## Pick one layout and version it
```
byte 0      : format version (0x01)
byte 1      : key id length L, then L bytes key id   (or fixed 4-byte key version)
next 12     : nonce
rest        : ciphertext || 16-byte tag
AAD         : version || key id || caller context
```
- Include the header bytes in the AAD so they cannot be swapped.
- Fixed sizes: 12-byte nonce (not 16: Go's docs call `NewGCMWithNonceSize` slower and less misuse-resistant than `NewGCM`,
  and Node accepted a 16-byte IV, so mixed stacks can disagree), 16-byte tag.
- Never infer the layout from length; check the version byte first and reject unknown versions.

## Other mismatches to rule out
- Text encoding of the envelope: base64 standard vs url-safe, padding (see the base64 skill).
- Key bytes: hex string vs raw bytes vs base64; a 64-char hex string passed as a key is 64 bytes.
- AAD: empty vs absent is the same in GCM, but `"null"` as a string is not. (pyca: `None` and `b""` gave identical ciphertext; decrypting with `b"null"` raised `InvalidTag`.)
- CBC legacy data: PKCS7 padding vs none; IV prepended or derived (`openssl enc -aes-256-cbc -pbkdf2` output starts with the 8 bytes `Salted__` then an 8-byte salt: 5 bytes of plaintext gave a 32-byte file; checked).

## Test vectors
Generate a vector in each language (key, nonce, aad, pt, expected blob hex), commit them as JSON,
and have every implementation both produce and consume all of them in CI. Fixed-nonce vectors
are for tests only; production code must not accept a caller-supplied nonce.

## Verify
- [ ] Layout is written down with byte offsets and a version byte.
- [ ] CI decrypts every other language's vectors.
- [ ] Truncated input shorter than header + nonce + tag is rejected before decrypt.
