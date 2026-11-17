---
id: computing-software.software-engineering.python.hashlib-and-hmac-digests
name: hashlib-and-hmac-digests
category: computing-software
field: software-engineering
product: python
tags: [python, py-archives-crypto, hashlib-hmac, hashlib, hmac, sha256, blake2, scrypt, pbkdf2, compare-digest, file-hash]
level: practitioner
status: docs-checked
description: "Hash files and messages with hashlib, sign with hmac and compare_digest, and store passwords with scrypt or PBKDF2 (or a dedicated library), keyed BLAKE2 and usedforsecurity."
sources: ["https://docs.python.org/3/library/hashlib.html", "https://docs.python.org/3/library/hmac.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# hashlib and hmac digests

```python
import hashlib, hmac, os

hashlib.sha256(b"data").hexdigest()
h = hashlib.sha256()
with open("big.iso", "rb") as f:
    for block in iter(lambda: f.read(1 << 20), b""): h.update(block)    # streaming
hashlib.file_digest(open("big.iso", "rb"), "sha256").hexdigest()        # 3.11+: one call

hashlib.blake2b(b"x", digest_size=16, key=b"secret-key")                # fast keyed hash / MAC

# Message authentication
tag = hmac.new(key, msg, "sha256").digest()
ok = hmac.compare_digest(tag, received_tag)       # constant time; never use ==
hmac.digest(key, msg, "sha256")                   # one-shot, optimized C path for OpenSSL digest names

# Password storage: salted, slow, memory-hard
salt = os.urandom(16)
dk = hashlib.scrypt(password.encode(), salt=salt, n=2**15, r=8, p=1, dklen=32, maxmem=64*2**20)
dk2 = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 600_000)   # docs: hundreds of thousands of SHA-256 iterations (as of 2022)
```
Store `algorithm$params$salt$hash`; compare with `compare_digest`; re-hash with new parameters on login.

## Choosing
- Integrity checksums/dedupe: SHA-256 or BLAKE2 (both in hashlib). Since 3.9 all constructors take `usedforsecurity=False` to mark non-security use (it permits algorithms blocked in restricted environments).
- MACs: `hmac` with a SHA-2 digest, or keyed BLAKE2 (`key=`).
- Passwords: use scrypt or PBKDF2 with a random salt of 16 or more bytes; never a bare fast hash.

## Gotchas
- Hash input must be bytes, so encode strings first.
- `hexdigest()` returns `str` and `digest()` returns `bytes`; compare like with like.
- `scrypt` `maxmem` limits memory (OpenSSL 1.1.0 defaults to 32 MiB); tune work factors on production hardware and pin parameters in config.
- `hashlib.algorithms_available` can list one algorithm under several names (thanks to OpenSSL); `algorithms_guaranteed` is the portable subset.
- Compare MACs with `hmac.compare_digest`, not `==`, to avoid timing attacks.

## Verify
- [ ] Known-answer tests (e.g. `sha256(b"abc")` = `ba7816bf...15ad`).
- [ ] Password verification cost is measured on production hardware, and tag comparison uses `compare_digest`.

## Checked

- 2026-11-03: checked against the CPython docs `library/hashlib.rst` and `library/hmac.rst`: `file_digest` (3.11), `usedforsecurity` (3.9), `scrypt` signature and `maxmem`, `pbkdf2_hmac` iteration guidance, `blake2b` `digest_size` and `key`, `hmac.digest` one-shot (3.7), `compare_digest`, `algorithms_available`.
- Removed: OWASP iteration claim, MD5/SHA-1 collision remark, length-extension note, BLAKE3 and third-party password libraries, `hash()` randomisation, the exact TypeError message, the 50-500 ms target.

Method: documentation only; no commands were run.
