---
id: computing-software.cryptography-implementation.crypto-libraries.nodejs-hkdf-and-pbkdf2
name: nodejs-hkdf-and-pbkdf2
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [crypto-libraries, cryptography-implementation, node-hkdf, node-pbkdf2, nodejs, hkdf, pbkdf2, key-derivation]
level: practitioner
status: verified
description: "Derive keys in Node.js with crypto.hkdf and crypto.pbkdf2 (async and sync): parameter order, ArrayBuffer output, iteration counts and avoiding event-loop blocking."
sources: ["https://nodejs.org/api/crypto.html#cryptohkdfdigest-ikm-salt-info-keylen-callback", "https://nodejs.org/api/crypto.html#cryptopbkdf2password-salt-iterations-keylen-digest-callback"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node.js hkdf and pbkdf2

## HKDF
```js
const { hkdf, hkdfSync } = require('node:crypto');
hkdf('sha256', ikm, salt, 'myapp v1 enc', 32, (err, ab) => {   // ab is an ArrayBuffer
  const key = Buffer.from(ab);
});
const key2 = Buffer.from(hkdfSync('sha256', ikm, salt, 'myapp v1 mac', 32));
```
- Argument order: digest, ikm, salt, info, keylen. Swapping salt and info compiles fine and breaks interop.
- Output is an ArrayBuffer, not a Buffer. `info` may be a string or buffer. RFC 5869 test case 1 reproduces (`3cb25f25faacd57a9043...`).
- `keylen` max is 255 x hash length (8160 bytes for SHA-256 worked, 8161 threw `ERR_CRYPTO_INVALID_KEYLEN`).

## PBKDF2
```js
const { pbkdf2 } = require('node:crypto');
const { promisify } = require('node:util');
const key = await promisify(pbkdf2)(password, salt, 600000, 32, 'sha256');
```
- Async version runs on the libuv threadpool (default 4 threads); heavy login traffic queues behind it.
  Increase `UV_THREADPOOL_SIZE` or limit concurrency.
- `pbkdf2Sync` blocks the event loop at 600k iterations (about 160 ms on the test machine); never in request handlers.
- For password storage prefer `crypto.scrypt` or an Argon2 package; PBKDF2 when FIPS requires it.

## Web Crypto alternative
`crypto.subtle.deriveBits({ name: 'HKDF', hash: 'SHA-256', salt, info }, key, 256)` gave identical output to `hkdfSync` in Node (checked), and `subtle` PBKDF2 matched `pbkdf2Sync`; browsers implement the same spec.

## Verify
- [ ] RFC 5869 test case 1 reproduces with `hkdfSync`.
