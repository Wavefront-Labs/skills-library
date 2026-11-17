---
id: computing-software.cryptography-implementation.crypto-libraries.nodejs-scrypt-randombytes-uuid
name: nodejs-scrypt-randombytes-uuid
category: computing-software
field: cryptography-implementation
product: crypto-libraries
tags: [cryptography-implementation, crypto-libraries, node-crypto, node-scrypt, randombytes, randomuuid, randomint, timingsafeequal, password-hashing, nodejs]
level: practitioner
status: verified
description: "Use Node.js crypto.scrypt for password hashing (params, maxmem, storage format), randomBytes/randomInt/randomUUID for tokens, and timingSafeEqual for comparisons."
sources: ["https://nodejs.org/api/crypto.html#cryptoscryptpassword-salt-keylen-options-callback", "https://nodejs.org/api/crypto.html#cryptorandomintmin-max-callback", "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html#scrypt"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node.js scrypt, randomBytes and friends

Node has no built-in Argon2 (use the `argon2` npm package for that); its
built-in password KDF is scrypt.

## Password hashing with scrypt

OWASP (when Argon2id is unavailable): N=2^17, r=8, p=1 (128 MiB). Node's default `maxmem` is 32 MiB and scrypt errors when about 128 * N * r exceeds `maxmem`, so you must raise it, or scrypt throws `ERR_CRYPTO_INVALID_SCRYPT_PARAMS` ("memory limit exceeded"). A `maxmem` of exactly 128 MiB still failed at N=2^17, r=8; 129 MiB and the 256 MiB below worked.

```js
const { scrypt, randomBytes, timingSafeEqual } = require('node:crypto');
const { promisify } = require('node:util'); const scryptP = promisify(scrypt);
const P = { N: 2 ** 17, r: 8, p: 1, maxmem: 256 * 1024 * 1024 };

async function hash(pw) {
  const salt = randomBytes(16);
  const dk = await scryptP(pw.normalize('NFKC'), salt, 32, P);
  return `scrypt$${P.N}$${P.r}$${P.p}$${salt.toString('base64')}$${dk.toString('base64')}`;
}
async function verify(pw, stored) {
  const [, N, r, p, s, h] = stored.split('$');
  const expected = Buffer.from(h, 'base64');
  const dk = await scryptP(pw.normalize('NFKC'), Buffer.from(s, 'base64'), expected.length,
                           { N: +N, r: +r, p: +p, maxmem: P.maxmem });
  return timingSafeEqual(dk, expected);
}
```

- Use the async version: `scrypt` at these parameters took about 250 ms here, and `scryptSync` would block the event loop that long.
  The async one runs in the libuv threadpool (default 4 threads,
  `UV_THREADPOOL_SIZE`) - size it for login concurrency.
- Store parameters with the hash so you can raise them later.
- `timingSafeEqual` throws `ERR_CRYPTO_TIMING_SAFE_EQUAL_LENGTH` if lengths differ; compare lengths first or hash
  both sides to fixed length.

## Randomness

```js
randomBytes(32).toString('base64url');   // session tokens, API keys (256 bits, 43 chars)
crypto.randomInt(0, 62);                 // unbiased integer in [0, 62)
crypto.randomUUID();                     // version 4 UUID, 122 random bits
crypto.getRandomValues(new Uint8Array(16)); // Web Crypto-compatible
```

- `randomUUID` is fine as an unguessable identifier; for secrets prefer 256-bit
  `randomBytes` (UUIDs get logged and shown in URLs).
- Never `Math.random()` for anything security-relevant.
- `randomInt` avoids modulo bias; `randomBytes(1)[0] % 62` does not.

## Verify

- [ ] scrypt runs with N >= 2^17 without `memory limit exceeded`; login latency measured.
- [ ] Hash strings include parameters; old hashes upgrade on login.
- [ ] Token generation uses `randomBytes`/`randomInt`, comparisons use `timingSafeEqual`.
