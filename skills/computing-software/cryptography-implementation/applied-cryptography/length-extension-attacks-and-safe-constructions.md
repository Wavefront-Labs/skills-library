---
id: computing-software.cryptography-implementation.applied-cryptography.length-extension-attacks-and-safe-constructions
name: length-extension-attacks-and-safe-constructions
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, hash-functions, length-extension-attack, sha-256, merkle-damgard, hmac, secret-prefix-mac, kmac]
level: practitioner
status: verified
description: "Recognise and fix length-extension bugs: why H(secret||msg) with SHA-256 is forgeable, which hashes resist, and replacing it with HMAC or KMAC."
sources: ["https://csrc.nist.gov/pubs/fips/180-4/upd1/final", "https://www.rfc-editor.org/rfc/rfc2104", "https://github.com/iagox86/hash_extender"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Length-extension attacks and safe constructions

SHA-1, SHA-256, SHA-512 and MD5 are Merkle-Damgard hashes: the digest is
the full internal state. Given `H(secret || msg)` and `len(secret)`, an
attacker can compute `H(secret || msg || padding || extra)` without the
secret. The 2009 Flickr API signature forgery (Duong and Rizzo, 28 September 2009, MD5) is the textbook case.
Run here: an SHA-256 extension implemented from the compression function forged
`SHA-256(secret || msg || padding || "&admin=1")` from the digest and the secret's length alone.

## Find it

Grep for hash calls whose input starts with a key or secret:

```
sha256(secret + data)   md5(api_secret . params)   sha1(key || msg)
```

Also custom "signatures" in URLs and cookies, and `H(msg || secret)` (no
extension, but vulnerable to collision attacks on the hash).

Test with `hash_extender` (supports MD4, MD5, RIPEMD-160, SHA-0, SHA-1, SHA-256, SHA-512, WHIRLPOOL; not SHA-224/384): if the server accepts the
extended message with the forged digest, it is vulnerable.

## Fix

| Need | Use |
|---|---|
| Keyed integrity | HMAC-SHA-256 (`hmac.new(key, msg, sha256)`) |
| FIPS keyed hash with customisation | KMAC128/KMAC256 (SP 800-185) |
| Fast keyed hash outside FIPS | BLAKE2b keyed mode, BLAKE3 `keyed_hash` |
| Plain hash that resists extension | SHA-512/256, SHA-384, SHA3-256 |

Truncated SHA-2 variants (SHA-384, SHA-512/256) and SHA-3 resist length
extension because the output is not the full state, but they are still
not MACs by contract; prefer HMAC/KMAC for keyed use.

## Migration

Version the token or signature format, accept old and new during a window,
issue only new, then reject old. Rotate the secret at cutover, since it was
exposed to a forgeable construction.

## Verify

- [ ] No `hash(secret || ...)` constructions remain in code or protocol specs.
- [ ] Extended-message forgery test against the endpoint fails.
