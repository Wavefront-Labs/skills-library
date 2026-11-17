---
id: computing-software.cryptography-implementation.crypto-libraries.web-crypto-wrapkey-and-unwrapkey
name: web-crypto-wrapkey-and-unwrapkey
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, subtle-wrapkey, web-crypto, wrapkey, unwrapkey, aes-kw, key-wrapping]
level: advanced
status: verified
description: "Wrap and unwrap keys with Web Crypto: generateKey for AES-KW and RSA-OAEP wrapping keys, wrapKey formats, unwrapKey into non-extractable keys, and AES-GCM wrapping."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/wrapKey", "https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/unwrapKey", "https://w3c.github.io/webcrypto/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web Crypto wrapKey and unwrapKey

## Generate a wrapping key
```js
const kek = await crypto.subtle.generateKey({ name: "AES-KW", length: 256 }, false, ["wrapKey", "unwrapKey"]);
const dek = await crypto.subtle.generateKey({ name: "AES-GCM", length: 256 }, true, ["encrypt", "decrypt"]);
```
The key being wrapped must be `extractable: true`; the KEK can be non-extractable.

## Wrap and unwrap
```js
const wrapped = await crypto.subtle.wrapKey("raw", dek, kek, "AES-KW");     // 40 bytes for a 256-bit key
const dek2 = await crypto.subtle.unwrapKey("raw", wrapped, kek, "AES-KW",
    { name: "AES-GCM", length: 256 }, false, ["encrypt", "decrypt"]);       // non-extractable result
```
- AES-KW (RFC 3394) needs the exported key's length to be a multiple of 8 bytes: a raw AES key worked, a raw 20-byte HMAC key and a P-256 `pkcs8` key (138 bytes) threw `OperationError`, a P-256 `jwk` happened to work. To wrap `pkcs8` private keys use AES-GCM:
  `wrapKey("pkcs8", privKey, kek, { name: "AES-GCM", iv })` (store the iv; 154 bytes for P-256).
- RSA-OAEP wrapping: `wrapKey("raw", dek, rsaPublicKey, { name: "RSA-OAEP" })` to send a key to a key holder.
- `jwk` format wraps JSON; ensure the wrapping algorithm handles its length (AES-GCM does).

## Uses
- Storing per-user DEKs encrypted under a KEK derived from a password (`deriveKey` PBKDF2 -> AES-KW; derivation to AES-KW checked).
- Sending keys to a server HSM public key.

## Pitfalls
- Unwrapped keys default to whatever `extractable` you pass; pass `false` unless export is needed.
- Usages must match the algorithm (`wrapKey` usage on the KEK), otherwise `InvalidAccessError` (checked). Wrapping a non-extractable key also fails.

## Verify
- [ ] Wrapped blob round-trips; unwrap with wrong KEK throws `OperationError` (checked; the RSA-OAEP raw wrap of a 256-bit key gave a 256-byte blob for a 2048-bit key).
