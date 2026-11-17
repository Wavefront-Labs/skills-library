---
id: computing-software.web-development.frontend-development.web-crypto-subtlecrypto
name: web-crypto-subtlecrypto
category: computing-software
field: web-development
product: frontend-development
tags: [web-crypto-api, subtlecrypto, aes-gcm, pbkdf2, getrandomvalues, client-side-encryption]
level: advanced
status: verified
description: "Using the Web Crypto API: secure randomness, SHA-256 digests, AES-GCM encryption with unique IVs, PBKDF2/HKDF key derivation, non-extractable keys in IndexedDB."
sources:
  - https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto
  - https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/encrypt#aes-gcm
  - https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#pbkdf2
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web Crypto (SubtleCrypto)

Available as `crypto.subtle` in secure contexts (HTTPS, localhost) in browsers, workers and Node (`globalThis.crypto`).

## 1. Randomness and hashing
```js
crypto.randomUUID();                                   // v4 UUID
const bytes = crypto.getRandomValues(new Uint8Array(32));   // never Math.random for secrets
const hash = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
const hex = [...new Uint8Array(hash)].map(b => b.toString(16).padStart(2, "0")).join("");
```

## 2. AES-GCM encrypt / decrypt
```js
const key = await crypto.subtle.generateKey({ name: "AES-GCM", length: 256 }, false, ["encrypt", "decrypt"]);
const iv = crypto.getRandomValues(new Uint8Array(12));     // 96-bit, UNIQUE per message with this key
const ct = await crypto.subtle.encrypt({ name: "AES-GCM", iv }, key, data);
const pt = await crypto.subtle.decrypt({ name: "AES-GCM", iv }, key, ct);   // throws OperationError if tampered
```
Store `iv` alongside the ciphertext (it is not secret). Reusing an IV with the same key breaks GCM completely.

## 3. Key from a passphrase
```js
const base = await crypto.subtle.importKey("raw", new TextEncoder().encode(pass), "PBKDF2", false, ["deriveKey"]);
const key = await crypto.subtle.deriveKey(
  { name: "PBKDF2", salt, iterations: 600_000, hash: "SHA-256" },
  base, { name: "AES-GCM", length: 256 }, false, ["encrypt", "decrypt"]);
```
The OWASP Password Storage Cheat Sheet recommends 600,000 iterations for PBKDF2-HMAC-SHA256 (about 160 ms in Node 20 on this machine). Use HKDF to derive several keys from one high-entropy secret. Argon2 is not in Web Crypto (`importKey(..., "Argon2id")` threw `NotSupportedError` in Node 20; use a WASM library if you need it).

## 4. Keeping keys
`CryptoKey` objects with `extractable: false` can be stored in IndexedDB (structured clone) and used later, but their raw bytes cannot be read by JS, even by XSS. XSS can still *use* the key while the page is compromised.

## 5. Signatures and HMAC
`{ name: "HMAC", hash: "SHA-256" }` for webhook-style MACs; `ECDSA` P-256 or `Ed25519` (newer engines) for signatures; verify with `crypto.subtle.verify`. Compare MACs with `verify`, not string equality.

## Gotchas
- Client-side encryption protects data at rest/in transit to a server you do not trust; it does not protect against a compromised page.
- `crypto.subtle` is `undefined` on plain HTTP origins (except localhost).
- Base64 helpers: `Uint8Array.prototype.toBase64` / `Uint8Array.fromBase64` in newer engines (MDN compat: Chrome 140, Firefox 133, Safari 18.2; both `undefined` in Node 20); otherwise `btoa(String.fromCharCode(...bytes))` for small buffers.

Run in Node 20: SHA-256 of `abc` gave `ba7816bf...15ad`, AES-GCM round-trip worked (ciphertext = plaintext + 16-byte tag), a flipped byte threw `OperationError`, non-extractable keys refused `exportKey`, and HMAC, ECDSA P-256, Ed25519 and HKDF all worked.

## Verify
- [ ] Decrypting a ciphertext with one flipped byte throws.
- [ ] Unit test checks no IV is reused across 10k encryptions.
