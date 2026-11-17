---
id: computing-software.cryptography-implementation.crypto-libraries.nodejs-sign-and-verify
name: nodejs-sign-and-verify
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, node-crypto, node-sign-verify, ed25519, ecdsa, rsa-pss, dsaencoding, ieee-p1363, nodejs]
level: practitioner
status: verified
description: "Sign and verify with Node.js crypto.sign/crypto.verify: algorithm argument per key type, RSA-PSS options, ECDSA DER vs ieee-p1363 encoding, and webhook-style HMAC alternatives."
sources: ["https://nodejs.org/api/crypto.html#cryptosignalgorithm-data-key-callback", "https://nodejs.org/api/crypto.html#cryptoverifyalgorithm-data-key-signature-callback"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node.js crypto.sign and crypto.verify

The one-shot functions (Node 12.0+ per the docs) cover every key type; prefer them over the
streaming `createSign` API unless you hash large streams.

```js
const crypto = require('node:crypto');

// Ed25519: algorithm must be null/undefined (hash is built in)
const sig = crypto.sign(null, data, edPrivateKey);
const ok  = crypto.verify(null, data, edPublicKey, sig);

// ECDSA P-256 with SHA-256, raw r||s (64 bytes) for JOSE/WebCrypto interop
const sig2 = crypto.sign('sha256', data, { key: ecPrivateKey, dsaEncoding: 'ieee-p1363' });
crypto.verify('sha256', data, { key: ecPublicKey, dsaEncoding: 'ieee-p1363' }, sig2);

// RSA-PSS
const sig3 = crypto.sign('sha256', data, {
  key: rsaPrivateKey, padding: crypto.constants.RSA_PKCS1_PSS_PADDING,
  saltLength: crypto.constants.RSA_PSS_SALTLEN_DIGEST });
```

## Details that cause failures

- **Algorithm argument**: `null` for Ed25519/Ed448; a digest name for RSA and
  ECDSA. Passing `'sha256'` with an Ed25519 key throws (`ERR_OSSL_INVALID_DIGEST` on Node 20).
- **ECDSA encoding**: default `dsaEncoding: 'der'` (ASN.1; 69-72 bytes seen for P-256 over 300 signatures, usually 70-72);
  JWS ES256 and Web Crypto use `'ieee-p1363'` (fixed 64 bytes). A signature
  from one fails verification in the other.
- **RSA padding**: default is PKCS#1 v1.5 for signing (acceptable but PSS
  preferred). `saltLength` defaults to `RSA_PSS_SALTLEN_MAX_SIGN` when signing
  with PSS (a default-signed signature verified with MAX_SIGN and AUTO but not with DIGEST) - set `RSA_PSS_SALTLEN_DIGEST` on both sides for interop and FIPS.
- **verify returns boolean**: it throws only on malformed keys/arguments (a garbage signature, tampered data or the wrong DSA encoding returned `false`; a malformed key threw). Treat
  `false` as rejection and do not catch-and-ignore exceptions.
- The docs list ArrayBuffer/Buffer/TypedArray/DataView for `data`; a string happened to work on Node 20, but encode explicitly (`Buffer.from(str, 'utf8')`).

## Webhooks: when to use HMAC instead

For shared-secret webhook verification (Stripe, GitHub style), use
`crypto.createHmac('sha256', secret).update(rawBody).digest()` and compare
with `timingSafeEqual`. Sign over the **raw** request body bytes, not
re-serialised JSON.

## Verify

- [ ] Signatures verify in the peer implementation (JOSE library, Go, Python).
- [ ] Modified data returns `false`.
- [ ] Key type checked before sign/verify (KeyObject.asymmetricKeyType).
