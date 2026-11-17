---
id: computing-software.cryptography-implementation.crypto-libraries.nodejs-aes-gcm-createcipheriv
name: nodejs-aes-gcm-createcipheriv
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, node-crypto, createcipheriv, nodejs, aes-256-gcm, getauthtag, setauthtag, authtaglength, javascript]
level: practitioner
status: verified
description: "Encrypt with AES-256-GCM in Node.js crypto: createCipheriv, getAuthTag/setAuthTag ordering, authTagLength to block truncated tags, setAAD, and a safe wire format."
sources: ["https://nodejs.org/api/crypto.html#cryptocreatecipherivalgorithm-key-iv-options", "https://nodejs.org/api/crypto.html#deciphersetauthtagbuffer-encoding", "https://github.com/nodejs/node/issues/52327"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AES-256-GCM with Node.js createCipheriv

```js
const { createCipheriv, createDecipheriv, randomBytes } = require('node:crypto');

function seal(key, plaintext, aad) {           // key: 32-byte Buffer
  const iv = randomBytes(12);
  const c = createCipheriv('aes-256-gcm', key, iv, { authTagLength: 16 });
  c.setAAD(aad);
  const ct = Buffer.concat([c.update(plaintext), c.final()]);
  return Buffer.concat([iv, ct, c.getAuthTag()]);   // iv(12) || ct || tag(16)
}

function open(key, blob, aad) {
  if (blob.length < 28) throw new Error('decrypt failed');
  const iv = blob.subarray(0, 12), tag = blob.subarray(blob.length - 16);
  const ct = blob.subarray(12, blob.length - 16);
  const d = createDecipheriv('aes-256-gcm', key, iv, { authTagLength: 16 });
  d.setAAD(aad);
  d.setAuthTag(tag);                                 // before final()
  return Buffer.concat([d.update(ct), d.final()]);   // final() throws if tag invalid
}
```

## Ordering rules

- Encrypt: `setAAD` before `update`; `getAuthTag` only after `final`.
- Decrypt: `setAAD` and `setAuthTag` before `final`. `final()` throws
  `Unsupported state or unable to authenticate data` on a bad tag.
- `update()` on decrypt returns plaintext **before** authentication. Do not
  stream it to a client or parse it until `final()` has succeeded.

## Truncated tag gotcha

Without `authTagLength`, Node before v26 accepts tags shorter than 16 bytes in
`setAuthTag`: only 4, 8, 12, 13, 14, 15 and 16 bytes are valid lengths (docs DEP0090), and on Node 20 the first 4 bytes of the real tag decrypted successfully. That is DEP0182: runtime deprecation in v23.0.0, end-of-life in v26.0.0. An attacker could submit a 4-byte tag and forge with ~2^32 tries.
Always pass `{ authTagLength: 16 }` to `createDecipheriv` (or check
`tag.length === 16`); with it, 4-byte and 15-byte tags throw `ERR_CRYPTO_INVALID_AUTH_TAG` (checked).

## Other details

- Key must be exactly 32 bytes for aes-256 (a string key is UTF-8 encoded -
  never pass a passphrase; derive with `crypto.scrypt` or HKDF first).
- 12-byte random IVs: at most ~2^32 messages per key; rotate keys sooner.
- Do not use `createCipher` (weak MD5 key derivation, static IV; DEP0106, removed in v22.0.0; still present on Node 20) or `aes-256-cbc`
  without a MAC.
- Web Crypto (`crypto.subtle`) in Node appends the tag to the ciphertext
  automatically; the output of `seal()` above decrypted in `subtle.decrypt` with `iv` and `ct || tag` split as shown (checked).

## Verify

- [ ] Decryption with a 4-byte or 15-byte tag throws.
- [ ] Changing AAD, IV, ciphertext or tag throws on `final()`.
- [ ] No plaintext from `update()` is used before `final()` returns.
