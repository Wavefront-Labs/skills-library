---
id: computing-software.cryptography-implementation.applied-cryptography.argon2id-parameter-selection
name: argon2id-parameter-selection
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, password-hashing, argon2id-parameters, argon2id, rfc-9106, owasp, memory-cost, argon2-cffi]
level: practitioner
status: verified
description: "Pick Argon2id memory, iterations and parallelism: OWASP minimums, RFC 9106 profiles, benchmarking on production hardware, and memory DoS limits."
sources: ["https://www.rfc-editor.org/rfc/rfc9106#section-4", "https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html", "https://argon2-cffi.readthedocs.io/en/stable/parameters.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Argon2id parameter selection

Argon2id has three cost knobs: memory `m` (KiB), iterations `t`, and lanes
`p`. Memory is what makes GPU/ASIC cracking expensive, so maximise it
within what your servers can afford at peak login concurrency.

## Starting points

| Source | Parameters |
|---|---|
| OWASP minimum | m=19 MiB (19456 KiB), t=2, p=1 |
| OWASP equivalents | m=46 MiB t=1; m=12 MiB t=3; m=9 MiB t=4; m=7 MiB t=5 (all p=1) |
| RFC 9106 first choice | m=2 GiB (2^21 KiB), t=1, p=4: the uniformly safe option when you cannot tune to your hardware |
| RFC 9106 second choice | m=64 MiB (2^16 KiB), t=3, p=4, for much less memory (also the argon2-cffi `PasswordHasher()` default, run) |

Salt 16 bytes random; tag (hash) 32 bytes (RFC 9106: 128-bit salt, 256-bit tag).

## Tuning procedure

1. Fix `p` to the cores you will dedicate per hash (often 1 on busy web
   servers, so concurrent requests use the other cores).
2. Set `m` as high as `peak_concurrent_logins x m` fits in RAM with margin.
3. Increase `t` until a hash takes your target latency on production
   hardware (commonly 100-500 ms for interactive login).
4. Record the parameters in the encoded hash (`$argon2id$v=19$m=...,t=...,p=...$salt$hash`)
   so you can raise them later and rehash on login.

```python
from argon2 import PasswordHasher
ph = PasswordHasher(time_cost=2, memory_cost=19456, parallelism=1, hash_len=32, salt_len=16)
h = ph.hash(pw)
ph.verify(h, pw)                 # raises on mismatch
if ph.check_needs_rehash(h): h = ph.hash(pw)
```

Run with argon2-cffi 25.1.0: the hash string begins `$argon2id$v=19$m=19456,t=2,p=1$`, a wrong password raises
`VerifyMismatchError`, and `check_needs_rehash` is False for the same hasher but True for a default
`PasswordHasher()` (m=65536, t=3, p=4). Hashing took 21 ms here, so tune t upward to your target.

## Protect the server

- Bound concurrent hashes (semaphore/queue); a burst of login requests can
  exhaust memory.
- Cap password length (e.g. 1-4 KiB) before hashing.
- Rate-limit login per account and per IP; cost alone is not a defence.

## Verify

- [ ] Benchmark recorded on production instance type; latency target met at p95.
- [ ] Encoded hashes carry parameters; rehash-on-login implemented.
- [ ] Load test at peak login rate does not OOM.
