---
id: computing-software.cryptography-implementation.crypto-libraries.web-crypto-sign-and-verify
name: web-crypto-sign-and-verify
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, subtle-sign, web-crypto, subtle-crypto, ecdsa, ed25519, rsa-pss, signature-format, javascript, browser]
level: practitioner
status: verified
description: "Sign and verify with SubtleCrypto: ECDSA P-256 raw r||s output, Ed25519 support, RSA-PSS salt length, key import, and converting signatures for server libraries."
sources: ["https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/sign", "https://w3c.github.io/webcrypto/#ecdsa", "https://wicg.github.io/webcrypto-secure-curves/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Web Crypto sign and verify

## ECDSA P-256
```js
const { privateKey, publicKey } = await crypto.subtle.generateKey(
  { name: "ECDSA", namedCurve: "P-256" }, false, ["sign", "verify"]);
const data = new TextEncoder().encode("message");
const sig = await crypto.subtle.sign({ name: "ECDSA", hash: "SHA-256" }, privateKey, data);   // 64 bytes r||s
const ok = await crypto.subtle.verify({ name: "ECDSA", hash: "SHA-256" }, publicKey, sig, data);
```
**Signature format:** Web Crypto returns raw `r || s` (IEEE P1363, 64 bytes for P-256; checked), not DER; a DER signature passed to `subtle.verify` returned `false`, and Node's `crypto.verify` with `dsaEncoding: 'ieee-p1363'` accepted the Web Crypto signature. Java (`SHA256withECDSA`), OpenSSL and Go
`ecdsa.VerifyASN1` expect DER; convert, or use `SHA256withECDSAinP1363Format` (listed in the Java security standard algorithm names) / Go's `ecdsa.Verify` with split r, s (`ecdsa.VerifyASN1` exists for DER).
JOSE ES256 uses the raw format directly.

## Ed25519
```js
const kp = await crypto.subtle.generateKey({ name: "Ed25519" }, false, ["sign", "verify"]);
const sig = await crypto.subtle.sign({ name: "Ed25519" }, kp.privateKey, data);   // 64 bytes
```
Works on Node 20 (checked, 64-byte signatures); check browser support for your targets with a try/catch around `generateKey`.

## RSA-PSS
```js
await crypto.subtle.sign({ name: "RSA-PSS", saltLength: 32 }, rsaPrivateKey, data);
```
The hash is fixed by the key (`hash: "SHA-256"` at generate/import time). Salt length must match the verifier (checked: a `saltLength: 32` signature verified with 32 and failed with 20).

## Importing a server's public key
```js
const spki = Uint8Array.from(atob(b64), c => c.charCodeAt(0));
const pub = await crypto.subtle.importKey("spki", spki, { name: "ECDSA", namedCurve: "P-256" }, false, ["verify"]);
```
JWK import works too (`"jwk"` with `{kty:"EC", crv:"P-256", x, y}`).

## Gotchas
- `verify` returns `false` for bad signatures; it throws only for wrong key types or usages (`InvalidAccessError` when given a private key).
- Non-extractable private keys (`extractable: false`) can still be used by any script on the origin; XSS can sign.
- Hash the same bytes on both sides; encode strings with TextEncoder (UTF-8), not `charCodeAt`.

## Verify
- [ ] Browser-produced signature verifies on the server after format conversion.
- [ ] Tampered data returns false.
