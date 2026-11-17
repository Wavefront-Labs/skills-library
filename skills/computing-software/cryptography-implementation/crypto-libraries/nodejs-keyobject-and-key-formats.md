---
id: computing-software.cryptography-implementation.crypto-libraries.nodejs-keyobject-and-key-formats
name: nodejs-keyobject-and-key-formats
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, node-crypto, keyobject, createprivatekey, createpublickey, jwk, pem, der, pkcs8, spki, nodejs]
level: practitioner
status: verified
description: "Handle keys in Node.js with KeyObject: createPrivateKey/createPublicKey/createSecretKey, PEM/DER/JWK import-export, encrypted PKCS#8, and converting to Web Crypto CryptoKey."
sources: ["https://nodejs.org/api/crypto.html#class-keyobject", "https://nodejs.org/api/crypto.html#cryptocreateprivatekeykey", "https://nodejs.org/api/crypto.html#keyobjectexportoptions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node.js KeyObject and key formats

`KeyObject` is Node's typed key handle. Parsing a key once into a KeyObject
validates it, avoids re-parsing PEM on every operation, and keeps you from
mixing secret, public and private keys.

## Create

```js
const { createPrivateKey, createPublicKey, createSecretKey, generateKeyPairSync } = require('node:crypto');
const priv = createPrivateKey({ key: pemString, format: 'pem', passphrase: process.env.KEY_PASS });
const pub  = createPublicKey(priv);                    // derive public from private
const pub2 = createPublicKey({ key: jwkObj, format: 'jwk' });
const sec  = createSecretKey(Buffer.from(hexKey, 'hex'));   // HMAC/AES keys
const { publicKey, privateKey } = generateKeyPairSync('ed25519');
priv.asymmetricKeyType;   // 'rsa' | 'rsa-pss' | 'ec' | 'ed25519' | 'x25519' | ...
priv.asymmetricKeyDetails; // { namedCurve: 'prime256v1' } or { modulusLength: 3072, publicExponent: 65537n }
```

Check `asymmetricKeyType` and details at load time against what the code
expects (e.g. reject RSA < 2048, require `ec` with `prime256v1`).

## Export

```js
privateKey.export({ type: 'pkcs8', format: 'pem',
                    cipher: 'aes-256-cbc', passphrase: pass });   // encrypted PKCS#8 (PBES2)
publicKey.export({ type: 'spki', format: 'der' });
publicKey.export({ format: 'jwk' });                              // { kty:'OKP', crv:'Ed25519', x:'...' }
sec.export();                                                      // Buffer (secret keys)
```

Use `pkcs8` (private) and `spki` (public), not the legacy `pkcs1`/`sec1`
types, unless a peer needs them.

## Web Crypto interop

```js
const cryptoKey = priv.toCryptoKey({ name: 'ECDSA', namedCurve: 'P-256' }, false, ['sign']); // Node 23.0+ / 22.10+ (docs); undefined on Node 20
const ko = KeyObject.from(cryptoKey);                                                         // back (v15+; v26 deprecates passing a non-extractable CryptoKey)
```

On older Node, export to JWK and `crypto.subtle.importKey('jwk', ...)`.

## Pitfalls

- Passing PEM strings directly to `crypto.sign` works but re-parses each call
  and accepts whatever key type the PEM holds.
- JWK private keys contain `d`; never log `export({format:'jwk'})` output.
- Encrypted PEM with the old `Proc-Type: 4,ENCRYPTED` header (what `openssl genrsa -traditional -aes256` writes) is the legacy
  traditional format; re-encrypt as PKCS#8 (`ENCRYPTED PRIVATE KEY`). `createPrivateKey` without the passphrase fails (`ERR_OSSL_CRYPTO_INTERRUPTED_OR_CANCELLED` on Node 20).

## Verify

- [ ] Keys loaded once at startup into KeyObjects; type/size asserted.
- [ ] Private keys at rest are encrypted PKCS#8 or in a KMS.
- [ ] JWK round-trip (export then import) yields an equal public key (`pub.equals(pub2)`).
