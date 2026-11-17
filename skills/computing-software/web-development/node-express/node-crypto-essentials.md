---
id: computing-software.web-development.node-express.node-crypto-essentials
name: node-crypto-essentials
category: computing-software
field: web-development
product: node-express
tags: [node-crypto, randomuuid, timingsafeequal, hmac-sha256, scrypt, node]
level: practitioner
status: verified
description: "Using node:crypto correctly: secure random values, HMAC signing and constant-time comparison, hashing vs password hashing, AES-256-GCM encryption, key generation and webcrypto."
sources:
  - https://nodejs.org/api/crypto.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# node:crypto essentials

## 1. Randomness
```js
import crypto from "node:crypto";
crypto.randomUUID();                              // ids
crypto.randomBytes(32).toString("base64url");    // tokens, API keys, reset links
crypto.randomInt(100000, 1000000);               // 6-digit OTP without modulo bias
```
Never `Math.random()` for anything security-relevant.

## 2. HMAC and constant-time compare
```js
const sig = crypto.createHmac("sha256", secret).update(rawBody).digest("hex");
const a = Buffer.from(sig), b = Buffer.from(req.get("X-Signature") ?? "");
const ok = a.length === b.length && crypto.timingSafeEqual(a, b);   // throws if lengths differ, so check first
```
Sign the raw bytes (capture with `express.raw()` or the `verify` hook of `express.json`), not re-serialised JSON.

## 3. Hash vs password hash
- `crypto.createHash("sha256")` for integrity/fingerprints only.
- Passwords: Argon2id (`argon2` package) or bcrypt. If you must stay in core: `crypto.scrypt(password, salt, 64, { N: 2 ** 17, r: 8, p: 1, maxmem: 256 * 1024 * 1024 })` with a 16-byte random salt stored alongside.
- MD5/SHA-1 never for security.

## 4. Symmetric encryption (AES-256-GCM)
```js
function encrypt(key, plaintext) {                       // key: 32-byte Buffer from a KMS/secret store
  const iv = crypto.randomBytes(12);
  const c = crypto.createCipheriv("aes-256-gcm", key, iv);
  const ct = Buffer.concat([c.update(plaintext, "utf8"), c.final()]);
  return Buffer.concat([iv, c.getAuthTag(), ct]).toString("base64");
}
function decrypt(key, b64) {
  const buf = Buffer.from(b64, "base64");
  const d = crypto.createDecipheriv("aes-256-gcm", key, buf.subarray(0, 12));
  d.setAuthTag(buf.subarray(12, 28));
  return Buffer.concat([d.update(buf.subarray(28)), d.final()]).toString("utf8");   // throws if tampered
}
```
Unique IV per encryption; include a key id/version prefix to support rotation. Derive subkeys with `crypto.hkdfSync`.

## 5. Keys and signatures
`crypto.generateKeyPairSync("ed25519")`, `crypto.sign(null, data, privateKey)` / `crypto.verify`; `crypto.createPublicKey` from PEM/JWK. `crypto.webcrypto` / `globalThis.crypto.subtle` gives the browser-compatible API for isomorphic code.

## Verify
- [ ] Tests: tampered ciphertext fails to decrypt; wrong-length signatures return false without throwing; no `createCipher(` (removed in Node 22; still present but deprecated on Node 20) or `Math.random` in security code.

## Checked
- Node 24.22.0 and 20.20.2: `randomUUID`, `randomBytes(32).toString("base64url")` (43 characters), `randomInt` range; `timingSafeEqual` throws `ERR_CRYPTO_TIMING_SAFE_EQUAL_LENGTH` on different lengths and works on equal ones; `scrypt` with `N: 2 ** 17` fails with `ERR_CRYPTO_INVALID_SCRYPT_PARAMS` (memory limit exceeded) unless `maxmem` is raised to 256 MB, then returns 64 bytes; the AES-256-GCM helpers round-trip `héllo` and throw `Unsupported state or unable to authenticate data` for tampered data or a wrong key; `hkdfSync`, ed25519 `sign`/`verify` (wrong message false, wrong-length signature false, no throw), `webcrypto`; `crypto.createCipher` is still a function on Node 20 and `undefined` on Node 24 (the 22.0.0 changelog moved it to end of life). Argon2/bcrypt packages and the Express raw-body capture were not run.
