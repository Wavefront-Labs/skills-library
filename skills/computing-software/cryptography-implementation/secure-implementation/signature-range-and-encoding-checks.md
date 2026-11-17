---
id: computing-software.cryptography-implementation.secure-implementation.signature-range-and-encoding-checks
name: signature-range-and-encoding-checks
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, signature-range-check, ecdsa, psychic-signatures, cve-2022-21449, der-strictness, ed25519, rsa-pkcs1, signature-verification, input-validation]
level: advanced
status: verified
description: "Validate signature inputs before trusting them: ECDSA r and s ranges (Psychic Signatures), strict DER, Ed25519 S < L, RSA length checks and full PKCS#1 encoding comparison."
sources: ["https://neilmadden.blog/2022/04/19/psychic-signatures-in-java/", "https://www.rfc-editor.org/rfc/rfc8032#section-5.1.7", "https://csrc.nist.gov/pubs/fips/186-5/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Signature range and encoding checks

## ECDSA
- Reject unless `1 <= r <= n-1` and `1 <= s <= n-1`. Oracle Java SE skipped this (CVE-2022-21449, "Psychic Signatures"; NVD lists Oracle Java SE 17.0.2 and 18 as affected, other write-ups date the flaw from Java 15):
  `r = s = 0` verified for every message and key. Run here: pyca rejects r=s=0, r=0, s=n and r=n on P-256, and rejects DER with a padded INTEGER or a trailing byte.
- Strict DER: INTEGERs minimal-length, non-negative, no trailing data after the SEQUENCE. BER-lenient parsing makes
  signatures malleable (Bitcoin's BIP 66, "Strict DER signatures", fixed this).
- Raw `r||s`: exactly 2 x field-size bytes.
- Optional low-S normalisation where malleability matters.

## Ed25519
- Signature exactly 64 bytes; `S < L` (group order) or reject; reject non-canonical `R` and small-order public keys
  if you need strict behaviour (see the Ed25519 verification strictness skill).

## RSA PKCS#1 v1.5 verification
- Signature length must equal the modulus length in bytes; integer `s < n`.
- Verify by **re-encoding**: compute the expected `EM = 00 01 FF..FF 00 || DigestInfo || hash` and compare the whole
  block. Parsing the decrypted block and extracting the hash allowed Bleichenbacher's 2006 e=3 forgery (garbage after
  the hash) and many later variants.
- Allowlist the DigestInfo for the expected hash; do not accept whatever hash algorithm the signature claims.

## RSA-PSS
Check salt length matches the expected value when the protocol fixes it; use library verification with explicit
parameters.

## Where to enforce
Normally inside the crypto library; your job is to use a library that does it, keep it updated, and include
Wycheproof signature vectors in your tests, which contain exactly these malformed cases.

## Verify
- [ ] Wycheproof ECDSA, EdDSA and RSA signature vectors pass (invalid ones rejected).
- [ ] Test: `r = 0, s = 0` signature is rejected.
