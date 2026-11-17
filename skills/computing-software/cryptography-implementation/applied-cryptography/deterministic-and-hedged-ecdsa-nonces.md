---
id: computing-software.cryptography-implementation.applied-cryptography.deterministic-and-hedged-ecdsa-nonces
name: deterministic-and-hedged-ecdsa-nonces
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, digital-signatures, deterministic-ecdsa, rfc6979, hedged-signatures, ecdsa-nonce, k-leakage, fault-attacks, fips-186-5]
level: advanced
status: docs-checked
description: "Generate ECDSA nonces safely: RFC 6979 deterministic k, hedged (random plus deterministic) signing against faults, and why biased k is dangerous."
sources: ["https://datatracker.ietf.org/doc/html/rfc6979", "https://datatracker.ietf.org/doc/draft-irtf-cfrg-det-sigs-with-noise/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deterministic and hedged ECDSA nonces

Each (EC)DSA signature uses a secret per-signature value k that must be chosen uniformly from a
set of modular integers by a cryptographically secure process; RFC 6979 notes that even slight
biases in that process may be turned into attacks.

## Options

| Method | k = | Pros | Cons |
|---|---|---|---|
| Random | CSPRNG output | simple | needs a source of high-quality randomness |
| Deterministic (RFC 6979) | HMAC_DRBG instantiated with the private key x as entropy input and bits2octets(H(m)) as nonce | no randomness source needed | deterministic signatures are theoretically exposed to side-channel and fault-injection attacks (draft-irtf-cfrg-det-sigs-with-noise) |
| Hedged | k derived from a random string, the secret key and the message | protects against weak RNG yet still prevents many side-channel and fault attacks that exploit determinism; no extra point multiplications, so fine for constrained IoT | not reproducible |

The draft states that NIST's FIPS 186-5 warns about side-channel and fault attacks while allowing
deterministic ECDSA for devices that lack good randomness, that ML-DSA uses hedged signing by
default, and that it updates RFC 6979 and RFC 8032 to recommend hedged constructions where
side-channel and fault attacks are a concern. The updates are invisible to verifiers. Adding
randomness to EdDSA is not compliant with RFC 8032. Deriving k deterministically is also
insecure in multi-party (FROST) signing.

RFC 6979 section 3.6 allows additional data k' appended to the HMAC input
(`K = HMAC_K(V || 0x00 || int2octets(x) || bits2octets(h1) || k')`), for example a
signature counter or monotonic clock when no good random source exists; this is a variant, not
plain deterministic ECDSA.

## Generating k uniformly
RFC 6979 compares the bits2int result of each candidate T against q and loops if it is not in
1 to q-1; it states that a simple modular reduction would induce biases detrimental to signature
security. Never hand-roll k; use a vetted implementation.

## Verify
- [ ] Which mode (random, deterministic, hedged) each ECDSA signer uses is identified.
- [ ] RFC 6979 Appendix A.2 test vectors pass if deterministic mode is used.
- [ ] Fault-exposed devices use a hedged construction.

## Checked
Method: docs-checked 2026-11-09 against RFC 6979 (sections 3.2, 3.3, 3.6, Appendix A.2 index; downloaded text) and draft-irtf-cfrg-det-sigs-with-noise-04 (introduction and background). Removed unconfirmed incident dates, library-default claims and the eprint 2019/1155 and FIPS 186-5 sources (the eprint paper is about SHA-3 proofs).
