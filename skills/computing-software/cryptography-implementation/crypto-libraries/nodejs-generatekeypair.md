---
id: computing-software.cryptography-implementation.crypto-libraries.nodejs-generatekeypair
name: nodejs-generatekeypair
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, node-generatekeypair, nodejs, key-generation, keyobject, ed25519, rsa]
level: practitioner
status: gated
description: "Generate key pairs in Node.js with crypto.generateKeyPair: RSA, EC, Ed25519 and X25519 options, PEM and DER encodings, encrypted private key output and KeyObjects."
sources: ["https://nodejs.org/api/crypto.html#cryptogeneratekeypairtype-options-callback", "https://nodejs.org/api/crypto.html#class-keyobject"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Node.js generateKeyPair

## KeyObjects (preferred)
```js
const { generateKeyPair } = require('node:crypto');
const { promisify } = require('node:util');
const { publicKey, privateKey } = await promisify(generateKeyPair)('ed25519');
const ec  = await promisify(generateKeyPair)('ec', { namedCurve: 'P-256' });
const rsa = await promisify(generateKeyPair)('rsa', { modulusLength: 3072, publicExponent: 0x10001 });
```
Returns `KeyObject`s, usable directly with `crypto.sign`, `createSign`, `diffieHellman`.

## Encoded output
```js
const { publicKey, privateKey } = await promisify(generateKeyPair)('ec', {
  namedCurve: 'P-384',
  publicKeyEncoding:  { type: 'spki',  format: 'pem' },
  privateKeyEncoding: { type: 'pkcs8', format: 'pem', cipher: 'aes-256-cbc', passphrase: process.env.KEY_PASS },
});
```
- `type`: `spki`/`pkcs1` (RSA) for public; `pkcs8`, `pkcs1` (RSA), `sec1` (EC) for private. Prefer spki/pkcs8.
- `format: 'jwk'` is accepted in `publicKeyEncoding`/`privateKeyEncoding` and returns an object (checked on Node 20: keys `kty,x,y,crv`); `KeyObject.export({ format: 'jwk' })` gives the same.
- Other types: `rsa-pss`, `dsa`, `dh`, `x25519`, `x448`, `ed448`; `ml-kem-512/768/1024`, `ml-dsa-44/65/87` and `slh-dsa-*` are listed in the current Node docs (the 24.x release that added each key type and its OpenSSL requirement are unconfirmed) and Node 20 rejects `ml-kem-768` (checked). KEMs use `crypto.encapsulate(key)` / `crypto.decapsulate(key, ciphertext)` (added in v24.7.0 per the docs), and the docs list a `'raw-seed'` key format (the seed length is unconfirmed, no ML-KEM build available) (gated: unconfirmed, source is paywalled or blocked).

## Pitfalls
- `generateKeyPairSync` for RSA 4096 blocks the event loop (about 1.7 s here).
- Hard-coded passphrases in code; read from secrets.
- `modulusLength` below 2048 is accepted by Node (a 1024-bit key was generated); enforce minimums yourself.

## Verify
- [ ] Generated key exported and re-imported with `createPrivateKey`; sign/verify test passes.
