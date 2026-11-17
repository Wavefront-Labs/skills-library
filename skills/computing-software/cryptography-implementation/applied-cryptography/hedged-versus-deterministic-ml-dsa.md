---
id: computing-software.cryptography-implementation.applied-cryptography.hedged-versus-deterministic-ml-dsa
name: hedged-versus-deterministic-ml-dsa
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, ml-dsa, hedged-signing, deterministic-signing, fips-204, fault-attacks, side-channels, rnd]
level: advanced
status: docs-checked
description: "Choose hedged or deterministic ML-DSA signing: what rnd does, side-channel and fault trade-offs, test vectors, and library switches."
sources: ["https://csrc.nist.gov/pubs/fips/204/final", "https://docs.openssl.org/3.5/man7/EVP_SIGNATURE-ML-DSA/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hedged versus deterministic ML-DSA signing

ML-DSA.Sign takes a 32-byte value `rnd` mixed into the per-signature
randomness together with the private key and message.

- **Hedged (default)**: `rnd` is fresh from an approved RBG. FIPS 204
  makes this the default.
- **Deterministic**: `rnd` is 32 zero bytes, so the same key and message
  always give the same signature. In FIPS 204 the two variants differ only at line 5 of the signing algorithms.

Verification is identical for both; verifiers cannot tell which was used.

## Why hedged is the default

- **Fault attacks**: deterministic signing lets an attacker who can inject a
  fault compare a faulty and a correct signature of the same message,
  which can leak key material. Fresh `rnd` defeats this.
- **Side channels**: FIPS 204 says fresh randomness helps mitigate side-channel attacks, and the
  deterministic variant should not be used where side-channel attacks are a concern and cannot otherwise be mitigated.
- **Timing leakage**: deterministic signing leaks information about the message (not the key) through timing; use
  hedged signing if the message must stay secret.
- **Weak RNG**: the precomputed key-derived randomness still protects against flaws in the signer's RNG, and
  FIPS 204 says even a weak RBG may be preferable to fully deterministic signing.

## When deterministic is reasonable

- No fresh source of randomness at signing time (the case FIPS 204 permits it for).
- Reproducible test vectors and known-answer tests.

## Library switches

- OpenSSL 3.5: hedged by default; the ML-DSA signature parameter
  `deterministic` (and a `test-entropy` parameter for KATs) changes it.
- Do not implement "deterministic" by passing your own constant into an
  API meant for randomness elsewhere in the code.

## Verify

- [ ] Production signing uses hedged mode with an approved RBG.
- [ ] Known-answer tests run in deterministic mode (or with fixed `test-entropy`) match published vectors.
- [ ] Signing twice with the same message gives different signatures in production.

## Checked
2026-11-01. Confirmed in the FIPS 204 PDF: 32-byte rnd, hedged default with an RBG, deterministic variant using 32 zero bytes, rationale on fault and side-channel attacks, timing note, and identical verification. Confirmed in the OpenSSL 3.5 EVP_SIGNATURE-ML-DSA page: `deterministic` (default 0, 1 sets rnd to zeros) and `test-entropy` (32 bytes). Removed the ECDSA comparison, uniqueness use case, Bouncy Castle/liboqs remark and ACVP claim (unconfirmed).
Method: documentation only; no commands were run.
