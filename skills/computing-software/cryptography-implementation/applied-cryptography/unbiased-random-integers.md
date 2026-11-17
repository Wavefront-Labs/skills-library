---
id: computing-software.cryptography-implementation.applied-cryptography.unbiased-random-integers
name: unbiased-random-integers
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, random-generation, modulo-bias, rejection-sampling, csprng, secrets-randbelow, randombytes-uniform, nonce-bias]
level: practitioner
status: verified
description: "Generate uniform random integers, choices and shuffles without modulo bias: rejection sampling and the library calls that already do it right."
sources: ["https://docs.python.org/3/library/secrets.html", "https://doc.libsodium.org/generating_random_data", "https://arxiv.org/abs/1805.10941"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unbiased random integers

`random_u32() % n` is biased unless n divides 2^32: smaller values occur
slightly more often. For a 6-digit OTP the bias is tiny; for anything
cryptographic it can be fatal. Biased ECDSA nonces leak the private key
through lattice attacks (PuTTY 0.68 to 0.80, P-521 nonce bias, CVE-2024-31497: key recovery from about 60 signatures per NVD).

## Use the library call

| Language | Uniform integer in [0, n) |
|---|---|
| Python | `secrets.randbelow(n)`, `secrets.choice(seq)` |
| Node.js | `crypto.randomInt(0, n)` (max exclusive; `randomInt(n)` also works; range must be below 2^48, else `ERR_OUT_OF_RANGE`, run) |
| Java | `SecureRandom.nextInt(n)` (not run here) |
| Go | `rand.Int(rand.Reader, big.NewInt(n))` (crypto/rand, run) |
| .NET | `RandomNumberGenerator.GetInt32(n)` (not run here) |
| libsodium | `randombytes_uniform(n)` (docs: uniform even when n is not a power of 2) |
| Rust | rand 0.9: `rand::rng().random_range(0..n)`, or `OsRng.unwrap_err().random_range(0..n)` with `TryRngCore` in scope (run; `gen_range` is the 0.8 name) |

## Rejection sampling (if implementing)

```python
import os
def randbelow(n: int) -> int:
    k = n.bit_length()
    while True:
        r = int.from_bytes(os.urandom((k + 7) // 8), "big") >> ((8 - k % 8) % 8)
        if r < n:
            return r
```

Draw just enough bits, reject values `>= n`, retry. Expected draws are below 2 (run: 1.60 for n=5 with 3 bits, matching 8/5).
The function above returned only values below n for n in 1, 2, 3, 6, 7, 8, 255, 256, 257 and 2^64+1, and a chi-square
over 60,000 draws for n=6 gave 3.5 (critical value 11.07, 5 df). The modulo trap, for contrast: `i % 6` over 256 byte values gives counts 43,43,43,43,42,42.
Lemire's multiply-shift method is a faster variant used by some runtimes.

## Related traps

- **Floats**: `floor(random() * n)` inherits float granularity bias; use the
  integer API.
- **Shuffles**: Fisher-Yates with a uniform integer per step
  (`secrets.SystemRandom().shuffle(lst)`); sorting by random keys is only uniform when ties cannot occur
  (run: 1-bit keys on 3 items gave the identity order 50% of the time; 53-bit float keys were uniform).
- **Random strings**: pick each character with `secrets.choice(alphabet)`;
  do not map bytes `% len(alphabet)` unless the alphabet size is a power of two.
- **Scalars and nonces**: use the library's key/nonce generation (RFC 6979
  or hedged signing), not your own reduction mod q.

## Verify

- [ ] No `% n` on random bytes in security code (grep).
- [ ] Chi-square test over 10^6 samples for custom samplers.
