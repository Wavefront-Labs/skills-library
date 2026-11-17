---
id: computing-software.cryptography-implementation.crypto-libraries.gcm-iv-and-tag-placement-across-libraries
name: gcm-iv-and-tag-placement-across-libraries
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, gcm-tag-placement, aes-gcm, interop, ciphertext-format, auth-tag, java, nodejs, web-crypto, dotnet, golang]
level: practitioner
status: verified
description: "Lay out AES-GCM nonce, ciphertext and tag consistently across Java, Node, Web Crypto, pyca, Go, .NET and OpenSSL, which append or separate the tag."
sources: ["https://csrc.nist.gov/pubs/sp/800/38/d/final", "https://nodejs.org/api/crypto.html#ciphergetauthtag", "https://learn.microsoft.com/en-us/dotnet/api/system.security.cryptography.aesgcm?view=net-9.0"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GCM IV and tag placement across libraries

## Who appends the tag
| Library | Encrypt output | Decrypt input |
|---|---|---|
| Java `Cipher` "AES/GCM/NoPadding" | ciphertext || tag | ciphertext || tag |
| Web Crypto `encrypt` | ciphertext || tag | ciphertext || tag |
| pyca `AESGCM.encrypt` | ciphertext || tag | ciphertext || tag |
| Go `aead.Seal(dst, nonce, pt, ad)` | dst || ciphertext || tag (pass nonce as dst to prepend it) | ciphertext || tag |
| Node `createCipheriv` | ciphertext; tag via `cipher.getAuthTag()` | `setAuthTag(tag)` before `final()` |
| .NET `AesGcm.Encrypt` | separate `ciphertext` and `tag` spans | separate |
| OpenSSL EVP | ciphertext; tag via `EVP_CTRL_AEAD_GET_TAG` | `EVP_CTRL_AEAD_SET_TAG` before final |

Run here: pyca (a Go-produced `nonce || ct || tag` blob decrypted with `AESGCM.decrypt(blob[:12], blob[12:], aad)`), Node
(`getAuthTag()` is 16 bytes, `crypto.subtle` output equals body || tag) and Go. Java (Cipher Javadoc: tag appended; Java 8 gave 21 bytes for 5 bytes of plaintext), .NET (Learn
page) and OpenSSL (3.5 `EVP_EncryptInit` page) rows were read from the docs, not run.

## Pick one wire format and document it
Recommended: `version (1) || nonce (12) || ciphertext || tag (16)`.

Node:
```js
const iv = crypto.randomBytes(12);
const c = crypto.createCipheriv("aes-256-gcm", key, iv);
c.setAAD(aad);
const body = Buffer.concat([c.update(pt), c.final()]);
const out = Buffer.concat([Buffer.from([1]), iv, body, c.getAuthTag()]);
// decrypt: slice iv = out[1:13], tag = last 16, body = middle; d.setAuthTag(tag) then update/final
```
.NET: construct `new AesGcm(key, 16)` and call `Encrypt(nonce, pt, ct, tag, aad)` with separate `ct` and 16-byte `tag`
buffers, then write version || nonce || ct || tag. The constructors taking a tag size are in the Learn API page; the
constructors without one are marked `Obsolete` (SYSLIB0053) in the dotnet-api-docs source. No .NET SDK was available, so
this was not compiled.

## Gotchas
- Node: forgetting `setAuthTag` before `final()` throws "Unsupported state or unable to authenticate data" (checked on
  Node 24.22); also pass `authTagLength` when using tags shorter than 16 bytes (avoid short tags).
- Tag length must match: Java `GCMParameterSpec(128, iv)` means 128 **bits** (Javadoc: `tLen` is in bits, allowed values 128, 120, 112, 104, 96, or 64 and 32 for certain applications).
- AAD must be identical bytes on both sides; encode strings as UTF-8 explicitly.

## Verify
- [ ] A golden vector (fixed key, nonce, aad, plaintext) produces identical bytes in every library you use.
