---
id: computing-software.cryptography-implementation.crypto-libraries.web-crypto-importkey-and-exportkey-formats
name: web-crypto-importkey-and-exportkey-formats
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, web-crypto, subtle-crypto, subtle-importkey, jwk, spki, pkcs8, key-usages]
level: practitioner
status: verified
description: "Import and export keys with SubtleCrypto: raw, spki, pkcs8 and jwk formats per algorithm, PEM to DER, usages and extractable rules, and fixing SyntaxError and DataError."
sources: ["https://www.w3.org/TR/WebCryptoAPI/#SubtleCrypto-method-importKey", "https://developer.mozilla.org/en-US/docs/Web/API/SubtleCrypto/importKey", "https://www.rfc-editor.org/rfc/rfc7517"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# importKey and exportKey formats

## Which format for which key
| Key | raw | spki | pkcs8 | jwk |
|---|---|---|---|---|
| AES / HMAC secret | yes | | | yes |
| EC (ECDSA/ECDH) public | yes (uncompressed point) | yes | | yes |
| EC private | | | yes | yes |
| RSA public / private | | yes / | / yes | yes |
| Ed25519 / X25519 public | yes (32 B) | yes | | yes |
| Ed25519 / X25519 private | | | yes | yes |
| PBKDF2 / HKDF base | yes | | | |
Ed25519/X25519 generate, import and export in all four formats above on Node 20 (checked; Ed25519/X25519 private keys refuse `raw`); check browser support for your targets with a try/catch on `generateKey`.

## PEM to DER
Web Crypto takes DER, not PEM:
```js
function pemToDer(pem) {
  const b64 = pem.replace(/-----(BEGIN|END)[^-]+-----/g, "").replace(/\s+/g, "");
  return Uint8Array.from(atob(b64), c => c.charCodeAt(0));
}
const pub = await crypto.subtle.importKey("spki", pemToDer(pubPem),
  { name: "ECDSA", namedCurve: "P-256" }, false, ["verify"]);
```
`BEGIN PUBLIC KEY` = spki, `BEGIN PRIVATE KEY` = pkcs8. `BEGIN RSA PRIVATE KEY` (PKCS#1) and
`BEGIN EC PRIVATE KEY` (SEC1) are not accepted: convert with `openssl pkey` first.

## Algorithm parameters on import
- RSA: `{ name: "RSA-OAEP", hash: "SHA-256" }` or `{ name: "RSA-PSS", hash: "SHA-256" }`. The hash is
  bound to the key; MGF1 uses the same hash.
- EC: `{ name: "ECDSA" | "ECDH", namedCurve: "P-256" | "P-384" | "P-521" }`.
- AES: `{ name: "AES-GCM" }` (length comes from the bytes); HMAC: `{ name: "HMAC", hash: "SHA-256" }`.

## Usages and extractable
- ECDH/X25519 **public** keys take usages `[]`; private keys `["deriveKey", "deriveBits"]`.
  Other combinations throw `SyntaxError` (Node 20 words it "Unsupported key usage for a ECDH key"; browsers differ). Importing a public key with `["deriveBits"]` threw.
- Signing: private `["sign"]`, public `["verify"]`. RSA-OAEP: public `["encrypt", "wrapKey"]`,
  private `["decrypt", "unwrapKey"]`.
- `extractable: false` on import means you can never export it again from this context. Public
  keys can stay extractable; private and secret keys should not be.
- JWK `key_ops`/`use`/`ext` must be compatible with the usages and extractable flag you request,
  otherwise `DataError` (checked for a mismatched `key_ops` and for `ext: false` with `extractable: true`).

## Export
```js
const spki = new Uint8Array(await crypto.subtle.exportKey("spki", pubKey));
const jwk = await crypto.subtle.exportKey("jwk", pubKey);   // { kty: "EC", crv: "P-256", x, y, ... }
```
JWK uses base64url without padding; `raw` EC export is the 65-byte uncompressed point
(`0x04 || X || Y`; checked). Some servers want the 33-byte compressed form. Node's import accepted a compressed P-256 point, but browser behaviour was not checked, so send uncompressed.

## Verify
- [ ] Keys exported in one runtime import in the other (browser to server and back).
- [ ] Private/secret keys are imported non-extractable.
- [ ] Wrong-format input fails with a handled error, not an unhandled promise rejection.
