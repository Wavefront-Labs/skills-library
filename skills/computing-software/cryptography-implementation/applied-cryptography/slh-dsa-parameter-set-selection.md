---
id: computing-software.cryptography-implementation.applied-cryptography.slh-dsa-parameter-set-selection
name: slh-dsa-parameter-set-selection
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, slh-dsa, hash-based-signatures, slh-dsa-parameter-sets, fips-205, sphincs-plus, post-quantum, signature-size]
level: advanced
status: docs-checked
description: "Choose an SLH-DSA (FIPS 205) parameter set: SHA2 vs SHAKE, small (s) vs fast (f), public key and signature sizes, and where a stateless hash-based signature is worth it."
sources: ["https://csrc.nist.gov/pubs/fips/205/final", "https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.205.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SLH-DSA parameter set selection

SLH-DSA (FIPS 205, from SPHINCS+) is a stateless hash-based signature. Its
security rests on hash functions, which makes it the most conservative
post-quantum signature: a good fit for long-lived roots of trust, firmware and
code signing, where signatures are large and produced rarely, and a poor fit
for size-sensitive protocol handshakes.

## The twelve sets

Name pattern `SLH-DSA-{SHA2|SHAKE}-{128|192|256}{s|f}`; the SHA2 and SHAKE
variants of a size share the same public key and signature sizes (FIPS 205
Table 2).

| Set | Pub key | Sig |
|---|---|---|
| 128s | 32 B | 7,856 B |
| 128f | 32 B | 17,088 B |
| 192s | 48 B | 16,224 B |
| 192f | 48 B | 35,664 B |
| 256s | 64 B | 29,792 B |
| 256f | 64 B | 49,856 B |

The `s` sets give smaller signatures and the `f` sets larger ones; the `f`
variants are the ones intended for faster signing. Measure signing and
verification on your own hardware before committing.

## Choosing

- **Security category**: each set is claimed at least as secure as a generic
  block cipher with a prescribed key size (FIPS 205 section on categories);
  pick the category your policy requires.
- **s vs f**: `s` if signatures are stored or transmitted a lot and signing is
  rare (firmware, root CA, software releases). `f` if you sign more often and
  can afford the bandwidth.
- **SHA2 vs SHAKE**: pick what your HSM or library accelerates and what your
  approval regime allows.
- **Pure vs pre-hash**: FIPS 205 defines a pure version (`slh_sign`) and a
  pre-hash version (`hash_slh_sign`, HashSLH-DSA) that takes a hash function or
  XOF for the content. Do not mix the two for the same key.

## When to choose a different scheme

- High-volume online signing: ML-DSA (FIPS 204).
- Stateful hash-based signatures that you can manage safely: LMS/XMSS
  (SP 800-208).

## Verify

- [ ] Parameter set recorded in the signature format.
- [ ] Signature buffers and protocol fields sized for the chosen set.
- [ ] NIST ACVP vectors for SLH-DSA keyGen/sigGen/sigVer pass.
- [ ] Signing latency measured on target hardware.

## Checked
2026-11-01. Confirmed in FIPS 205 Table 2 (twelve sets, public key sizes 32/48/64 bytes, signature sizes above),
the pure and pre-hash signing variants and the security-category wording. Removed: speed multiples, private key
size, verification-speed comparison, CNSA 2.0 and hardware-acceleration statements, and the liboqs and
sphincs.org sources.
Method: documentation only; no commands were run.
