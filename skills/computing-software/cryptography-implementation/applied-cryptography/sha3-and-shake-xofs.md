---
id: computing-software.cryptography-implementation.applied-cryptography.sha3-and-shake-xofs
name: sha3-and-shake-xofs
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, hash-functions, sha-3, sha3-shake, shake128, shake256, xof, fips-202, cshake, sp-800-185]
level: practitioner
status: verified
description: "Use SHA-3 and the SHAKE128/256 extendable-output functions: security levels, output length choice, domain separation, and OpenSSL and Python calls."
sources: ["https://csrc.nist.gov/pubs/fips/202/final", "https://csrc.nist.gov/pubs/sp/800/185/final", "https://docs.python.org/3/library/hashlib.html#shake-variable-length-digests"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SHA-3 and SHAKE extendable-output functions

FIPS 202 defines SHA3-224/256/384/512 (fixed output) and SHAKE128/256
(extendable-output functions, XOFs). All are Keccak sponges; unlike SHA-2
they do not allow length extension. ML-KEM (FIPS 203) and ML-DSA (FIPS 204) are specified using SHAKE.

## Security levels

- SHA3-256: 128-bit collision, 256-bit preimage resistance (FIPS 202 Table 4).
- SHAKE128 with d output bits: `min(d/2, 128)` collision security (and
  `min(d, 128)` preimage). SHAKE256: `min(d/2, 256)`. So SHAKE128 with 256-bit output gives 128-bit
  security; asking for 1024 bits does not make it stronger.

## Calls

```bash
openssl dgst -sha3-256 file
openssl dgst -shake256 -xoflen 64 file     # OpenSSL 3.x, 64 bytes
```

```python
import hashlib
hashlib.sha3_256(b"data").hexdigest()
hashlib.shake_256(b"data").digest(64)      # length is required
```

Go: `crypto/sha3` (Go 1.24+, run: `sha3.Sum256`, `sha3.NewSHAKE256`) or
`golang.org/x/crypto/sha3`. For Java and other stacks check their docs (not run here).
Run: OpenSSL 3.2.3 and Python agree on SHAKE-256("abc", 64 bytes) = `48336660...`.

## XOF pitfalls

- Outputs are prefixes of each other: `SHAKE256(x, 32)` equals the first 32
  bytes of `SHAKE256(x, 64)`. If two uses need different lengths, domain-
  separate the input (or use cSHAKE with a customisation string) so one
  output never leaks part of another.
- Do not treat SHAKE as a MAC with `SHAKE(key || msg)`; use KMAC (SP 800-185),
  which is the standardised keyed variant.
- For hashing structured inputs, TupleHash (SP 800-185) gives unambiguous
  encoding.

## When to choose SHA-3 over SHA-2

- You need an XOF (mask generation, deriving variable-length material).
- Algorithm diversity (hedging against a SHA-2 break) or a protocol mandates it.
- Otherwise SHA-256 is faster in software with SHA-NI and universally supported.

## Verify

- [ ] NIST CAVP SHA-3/SHAKE vectors pass on your stack.
- [ ] Each SHAKE use has a fixed output length and a distinct domain prefix.
