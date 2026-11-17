---
id: computing-software.cryptography-implementation.crypto-libraries.web-crypto-derivekey-pbkdf2-hkdf-ecdh
name: web-crypto-derivekey-pbkdf2-hkdf-ecdh
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, web-crypto, subtle-crypto, subtle-derivekey, pbkdf2, hkdf, ecdh, x25519]
level: advanced
status: verified
description: "Derive keys in Web Crypto: PBKDF2 from passwords with modern iteration counts, HKDF with salt and info, ECDH/X25519 deriveBits then HKDF, and Argon2 alternatives."
sources: ["https://www.w3.org/TR/WebCryptoAPI/#SubtleCrypto-method-deriveKey", "https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/deriveKey", "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# deriveKey and deriveBits with PBKDF2, HKDF and ECDH

## Password to AES key (PBKDF2)
```js
const enc = new TextEncoder();
const base = await crypto.subtle.importKey("raw", enc.encode(password), "PBKDF2", false, ["deriveKey"]);
const salt = crypto.getRandomValues(new Uint8Array(16));        // store with the ciphertext
const key = await crypto.subtle.deriveKey(
  { name: "PBKDF2", salt, iterations: 600_000, hash: "SHA-256" },
  base, { name: "AES-GCM", length: 256 }, false, ["encrypt", "decrypt"]);
```
- 600,000 iterations for PBKDF2-HMAC-SHA256 (OWASP Password Storage Cheat Sheet); 220,000 for SHA-512 (the cheat sheet's current figure). Store salt, iteration
  count and hash with the data so you can raise them later.
- PBKDF2/HKDF base keys must be imported with `extractable: false` (`true` threw `SyntaxError` in Node).
- Web Crypto has no Argon2 or scrypt. For password-protected client-side vaults prefer Argon2id
  via WASM (the `libsodium-wrappers` npm package for libsodium.js `crypto_pwhash`, or `hash-wasm`; both exist on npm), which resists GPU attacks far better.

## Key material to keys (HKDF)
```js
const ikm = await crypto.subtle.importKey("raw", secretBytes, "HKDF", false, ["deriveKey", "deriveBits"]);
const encKey = await crypto.subtle.deriveKey(
  { name: "HKDF", hash: "SHA-256", salt, info: enc.encode("app v1 enc") },
  ikm, { name: "AES-GCM", length: 256 }, false, ["encrypt", "decrypt"]);
const macKey = await crypto.subtle.deriveKey(
  { name: "HKDF", hash: "SHA-256", salt, info: enc.encode("app v1 mac") },
  ikm, { name: "HMAC", hash: "SHA-256", length: 256 }, false, ["sign", "verify"]);
```
`salt` and `info` are required members (omitting either threw `TypeError`; empty `new Uint8Array()` is allowed). Distinct `info`
strings give independent keys from one secret.

## Key agreement (ECDH / X25519) then HKDF
```js
const mine = await crypto.subtle.generateKey({ name: "X25519" }, false, ["deriveBits"]);
const shared = await crypto.subtle.deriveBits({ name: "X25519", public: peerPublicKey },
                                              mine.privateKey, 256);
const ikm = await crypto.subtle.importKey("raw", shared, "HKDF", false, ["deriveKey"]);
// deriveKey HKDF with info = protocol label || both public keys
```
- Use `deriveBits` + HKDF rather than `deriveKey` straight from ECDH: the raw shared secret is not a
  uniformly random key, and HKDF lets you bind context (both public keys, protocol version).
- P-256: `{ name: "ECDH", namedCurve: "P-256" }` and `{ name: "ECDH", public: peer }`; an off-curve
  peer point is rejected at import (`DataError` in Node).
- Unauthenticated ECDH is open to man-in-the-middle; authenticate public keys (signatures, a
  server you trust, or out-of-band comparison).

## deriveBits length
Length is in **bits** and must be a multiple of 8 (252 threw `OperationError`). For PBKDF2/HKDF ask for what you need (256).

## Verify
- [ ] Salt and parameters are stored and read back on decrypt.
- [ ] Two different `info` labels give different keys (unit test).
- [ ] Peer public keys are authenticated before use.
