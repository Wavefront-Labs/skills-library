---
id: computing-software.cryptography-implementation.applied-cryptography.one-step-concatenation-kdf
name: one-step-concatenation-kdf
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, concat-kdf, sp-800-56c, ansi-x9-63, one-step-kdf, ecdh-es, jwe, fixedinfo, key-derivation]
level: advanced
status: verified
description: "Implement the SP 800-56C one-step KDF and the ANSI X9.63 variant: counter placement, FixedInfo encoding, JWE ECDH-ES Concat KDF parameters and test vectors."
sources: ["https://csrc.nist.gov/pubs/sp/800/56/c/r2/final", "https://www.rfc-editor.org/rfc/rfc7518#section-4.6.2", "https://www.secg.org/sec1-v2.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# One-step concatenation KDF (SP 800-56C and X9.63)

## Definitions
**SP 800-56C Rev 2 section 4 (one-step, hash option):**
```
for i = 1 .. ceil(L / hashlen):
    K_i = H( uint32_be(i) || Z || FixedInfo )
DerivedKey = leftmost L bits of K_1 || K_2 || ...
```
Also allowed: HMAC(salt, counter || Z || FixedInfo) or KMAC with a salt.

**ANSI X9.63 / SEC 1 KDF:** `K_i = H( Z || uint32_be(i) || SharedInfo )`. The counter comes **after** Z.
Mixing the two orders is the classic interop bug.

## FixedInfo encoding
SP 800-56A Rev 3 5.8.2.1.1 (concatenation format) recommends `AlgorithmID || PartyUInfo || PartyVInfo {|| SuppPubInfo}{|| SuppPrivInfo}` with each
variable-length field length-prefixed. JWE ECDH-ES (RFC 7518 4.6.2) is the most common concrete profile:
```
AlgorithmID = uint32_be(len(enc_or_alg)) || enc_or_alg   # "A256GCM" or "ECDH-ES+A128KW"
PartyUInfo  = uint32_be(len(apu)) || apu
PartyVInfo  = uint32_be(len(apv)) || apv
SuppPubInfo = uint32_be(keydatalen_in_bits)
```
Counter starts at 1, H = SHA-256. Run: with the RFC 7518 Appendix C inputs (Z = 9e56d91d...90c4, A128GCM, Alice, Bob,
keydatalen 128) the first 16 bytes of the round-1 hash are `56 aa 8d ea ... 10 1a` (base64url `VqqN6vgjbSBcIijNcacQGg`),
matched by hashlib, pyca `ConcatKDFHash`, and OpenSSL SSKDF; pyca `X963KDF` and OpenSSL X963KDF match the Z-then-counter formula.

## Implementations
- OpenSSL 3: `openssl kdf -keylen 32 -kdfopt digest:SHA256 -kdfopt hexsecret:<Z> -kdfopt hexinfo:<FixedInfo> SSKDF`
  (SSKDF = SP 800-56C one-step); `X963KDF` for the X9.63 order. Run on 3.2.3: both match a hashlib loop of the two
  formulas above (including a 40-byte, 2-block output), and the two orders give different keys.
- pyca: `ConcatKDFHash(algorithm=hashes.SHA256(), length=32, otherinfo=fixed_info)` and `X963KDF(...)`.

## Gotchas
- Z must be the fixed-length shared secret including leading zero bytes (pad to the field size).
- Forgetting to include the algorithm or key length in FixedInfo lets one Z feed two different algorithms.
- Prefer HKDF for new protocols unless a standard (JWE, CMS ECC, some PIV/smart card profiles) mandates this KDF.

## Verify
- [ ] RFC 7518 Appendix C (ECDH-ES example) reproduces the derived key.
- [ ] Unit test distinguishes 56C and X9.63 counter order.
- [ ] Z is padded to the curve's byte length.
