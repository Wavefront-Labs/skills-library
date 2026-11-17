---
id: computing-software.cryptography-implementation.secure-implementation.length-leaks-and-early-exit-comparisons
name: length-leaks-and-early-exit-comparisons
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, length-leak, timing-attack, constant-time-compare, early-exit, token-lookup, selector-verifier, side-channel]
level: advanced
status: verified
description: "Remove timing leaks from secret comparisons and lookups: length mismatch handling, early-exit loops, database token lookups, and the selector/verifier split pattern."
sources: ["https://docs.python.org/3/library/hmac.html#hmac.compare_digest", "https://nodejs.org/api/crypto.html#cryptotimingsafeequala-b", "https://paragonie.com/blog/2017/02/split-tokens-token-based-authentication-protocols-without-side-channels"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Length leaks and early-exit comparisons

## Early exit
`==`, `memcmp`, `strcmp`, `Arrays.equals` and `String.equals` stop at the first differing byte. Comparing a
user-supplied MAC or token this way leaks how many leading bytes are correct, enabling byte-by-byte guessing over
the network (measured with statistics over many requests).

## Length handling
- Python `hmac.compare_digest` is designed to resist timing analysis, but the docs note that for different lengths (or types) a timing attack could theoretically reveal the lengths, not the values.
- Node `crypto.timingSafeEqual` throws `RangeError` (`ERR_CRYPTO_TIMING_SAFE_EQUAL_LENGTH`) if lengths differ (run on Node 20); check lengths yourself first.
- Lengths of MACs and fixed-size tokens are public anyway; enforce the expected length, then compare.
- When the length itself is secret (rare), compare fixed-length digests instead:
  ```python
  k = os.urandom(32)   # per-process
  same = hmac.compare_digest(hmac.digest(k, a, "sha256"), hmac.digest(k, b, "sha256"))
  ```

## Database lookups by secret
`SELECT ... WHERE token = ?` leaks via index traversal and string comparison timing, and stores the token in clear.
Split-token pattern:
1. Token = `selector (12-16 bytes) || verifier (32 bytes)`, both random.
2. Store `selector` and `SHA-256(verifier)`.
3. Look up by selector (not secret), then compare `SHA-256(presented verifier)` to the stored hash in constant time.

## Other length-dependent leaks
- Variable-time padding removal and parsing of decrypted data (see Lucky 13).
- Compression before encryption leaks secret content through ciphertext length (CRIME/BREACH).
- Ciphertext length reveals plaintext length; pad when that matters.

## Verify
- [ ] grep finds no `==` comparisons on MACs, tokens, password hashes or signatures.
- [ ] Token tables store only selector and verifier hash.
