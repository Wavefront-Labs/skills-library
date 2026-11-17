---
id: computing-software.cryptography-implementation.applied-cryptography.hmac-key-sizing-and-verification
name: hmac-key-sizing-and-verification
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, hmac, hmac-verification, message-authentication-code, constant-time-compare, fips-198-1, webhook-signing]
level: practitioner
status: verified
description: "Use HMAC correctly: key length versus hash size, constant-time tag comparison per language, verifying raw bytes, and replay protection."
sources: ["https://csrc.nist.gov/pubs/fips/198-1/final", "https://csrc.nist.gov/pubs/sp/800/107/r1/final", "https://www.rfc-editor.org/rfc/rfc2104"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# HMAC key sizing and verification

## Key size

- Generate the key from a CSPRNG at least as long as the hash output
  (32 bytes for HMAC-SHA-256, 64 for HMAC-SHA-512). Shorter keys cap
  security at the key's entropy (SP 800-107 Rev 1 5.3.2: an HMAC key "shall have a security strength that
  meets or exceeds" the strength needed to protect the data).
- Keys longer than the hash block size (64 bytes for SHA-256, 128 for
  SHA-512) are hashed first, so a 200-byte key gives no extra strength (run: a
  200-byte key and its SHA-256 digest give the same tag).
- Never use a human password directly as an HMAC key; derive it with a
  password KDF or, better, issue random keys.
- One key per purpose; do not reuse an encryption key as the MAC key.

## Constant-time verification

Recompute the tag over the exact received bytes and compare in constant time:

| Language | Compare |
|---|---|
| Python | `hmac.compare_digest(expected, received)` |
| Node.js | `crypto.timingSafeEqual(a, b)` (throws `ERR_CRYPTO_TIMING_SAFE_EQUAL_LENGTH` if lengths differ, run; check length first) |
| Java | `MessageDigest.isEqual(a, b)` (Javadoc: time depends only on the length of the first array) |
| Go | `hmac.Equal(a, b)` |
| .NET | `CryptographicOperations.FixedTimeEquals(a, b)` (short-circuits only on different lengths, per Microsoft docs) |
| C/OpenSSL | `CRYPTO_memcmp(a, b, len)` (returns 0 when equal; cannot order) |

Compare decoded bytes, not hex or base64 strings: hex case and base64
padding differences cause false rejects, and string compares short-circuit.

## Verification rules

- MAC the raw bytes received (raw HTTP body), not a re-serialised object.
- Include a timestamp or nonce in the MAC'd data and reject old ones
  (Stripe's libraries default to a 5-minute tolerance; a tolerance of 0 disables the check) to stop replays.
- Support two keys during rotation: try the current key, then the previous.
- Reject before parsing; do not parse untrusted JSON to find the signature
  scheme.

## Verify

- [ ] RFC 4231 test vectors pass (cases 1 and 2 matched with Python `hmac`).
- [ ] Unit test: tag differing in the last byte is rejected; timing compare used.
- [ ] Keys are random, >= hash output length, and purpose-specific.
