---
id: computing-software.software-engineering.v-lang.v-crypto-and-hashing
name: v-crypto-and-hashing
category: computing-software
field: software-engineering
product: v-lang
tags: [v-crypto-and-hashing, standard-library-misc, crypto, sha256, md5, sha1, hmac, bcrypt, hash, crypto.rand, password hashing, checksum, v-lang]
level: practitioner
status: docs-checked
description: "Compute sha256, md5, sha1 and hmac digests, hash passwords with bcrypt and generate secure random bytes."
sources:
  - https://docs.vlang.io/
  - https://modules.vlang.io/
  - https://github.com/vlang/v
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hashing and crypto modules

Goal: use the standard crypto/hash modules properly.

- Digests: `import crypto.sha256; sha256.hexhash('text')`, `sha256.sum(bytes)`; `crypto.sha1`, `crypto.sha512`, `crypto.md5` (the md5 and sha1 sources say both are cryptographically broken: checksums only).
- HMAC: `import crypto.hmac; hmac.new(key, data, sha256.sum, sha256.block_size)` returns bytes; compare with `hmac.equal(a, b)` (constant time).
- Passwords: `import crypto.bcrypt; h := bcrypt.generate_from_password(pw.bytes(), 12)!`; verify `bcrypt.compare_hash_and_password(pw.bytes(), h.bytes())!`.
- Random: `import crypto.rand; key := rand.bytes(32)!`, or `rand.read(mut buf)!` to fill an existing `[]u8`.
- Fast non-crypto hashes: the `hash.fnv1a`, `hash.crc32`, `hash.crc64` and `hash.adler32` modules.
- Encryption: `crypto.aes` (`aes.new_cipher(key)!`) is low level; ChaCha20 lives in `x.crypto.chacha20`; have the design reviewed.

Gotchas:
- For critical needs, prefer an independently reviewed implementation.
- Never log or hard-code keys.

Verify: hash a known test vector and compare.

## Checked

2026-11-03. Confirmed against the V repository source (vlib modules and doc/docs.md) read in this batch: sha256.hexhash/sum/block_size, sha1/sha512/md5 sum, hmac.new(key, data, hash_func, blocksize) and hmac.equal, bcrypt.generate_from_password(pw []u8, cost) and compare_hash_and_password, crypto.rand.bytes and read, aes.new_cipher, the md5 and sha1 source notes that they are broken, the existence of hash.fnv1a/crc32/crc64/adler32 and x/crypto/chacha20 (vlib/crypto, vlib/hash, vlib/x/crypto).
Removed or corrected: `rand.read(32)!` (read takes a mut buffer), `hash.wyhash` as a module, `crypto.chacha20` (it is x.crypto.chacha20), `(confirm audit status)` and the unsupported claim that V's crypto has had no third-party audits.
Method: documentation only; no commands were run.
