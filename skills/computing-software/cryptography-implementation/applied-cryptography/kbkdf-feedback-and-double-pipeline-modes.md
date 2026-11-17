---
id: computing-software.cryptography-implementation.applied-cryptography.kbkdf-feedback-and-double-pipeline-modes
name: kbkdf-feedback-and-double-pipeline-modes
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, kbkdf-feedback-mode, kbkdf, sp-800-108, double-pipeline, key-derivation]
level: advanced
status: verified
description: "Implement SP 800-108r1 KBKDF in feedback and double-pipeline modes: PRF choice, IV and counter options, encoding L, and interop parameters to fix."
sources: ["https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-108r1-upd1.pdf", "https://docs.openssl.org/3.0/man7/EVP_KDF-KB/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KBKDF feedback and double-pipeline modes

## Feedback mode (SP 800-108r1 4.2)
`K(i) = PRF(KI, K(i-1) [|| i] || Label || 0x00 || Context || [L]2)` with `K(0) = IV` (may be empty). The counter
is optional in the standard (sections 4.1, 4.2 and 4.3 of Rev 1 are counter, feedback and double-pipeline); OpenSSL always includes it. Output = `K(1) || K(2) || ...` truncated to L bits.

## Double-pipeline mode (4.3)
`A(0) = Label || 0x00 || Context || [L]2`, `A(i) = PRF(KI, A(i-1))`,
`K(i) = PRF(KI, A(i) [|| i] || Label || 0x00 || Context || [L]2)`. Chosen when the PRF cannot be run on
a counter input efficiently; rare in new designs.

## OpenSSL
```sh
openssl kdf -keylen 32 -kdfopt mode:FEEDBACK -kdfopt mac:HMAC -kdfopt digest:SHA256 \
  -kdfopt hexkey:$KI -kdfopt hexseed:$IV -kdfopt salt:label -kdfopt info:context KBKDF
```
(`salt` = Label, `info` = Context, `seed` = IV; `use-l` and `use-separator` toggle L and the zero byte.)
Run on OpenSSL 3.2.3 against a Python loop of `K(i) = HMAC(KI, K(i-1) || [i]_32 || Label || 0x00 || Context || [L]_32)`:
OpenSSL's feedback mode **includes the 32-bit counter** (matches with counter, not without), a seed of 32 bytes (the HMAC-SHA-256
output size) or none works, and a 16- or 64-byte seed fails with `invalid seed length`. OpenSSL implements only counter and
feedback (the man page); `mode:DOUBLE_PIPELINE` is rejected as an invalid mode, so use another library for double-pipeline.

## Parameters both sides must fix
- PRF (HMAC-SHA-256 or CMAC-AES), counter present and its width (8/16/24/32 bits) and position.
- Whether the 0x00 separator and [L] are included and L's byte width.
- IV value for feedback mode.
Mismatched flags give different keys with no error; pin them in the format spec.

## Prefer
Counter mode (4.1) or HKDF for new designs; use feedback mode only when a protocol requires it. (Kerberos AES-SHA2, RFC 8009, uses counter mode, not feedback.)

## Verify
- [ ] CAVP KBKDF feedback vectors pass with the same flag settings.
