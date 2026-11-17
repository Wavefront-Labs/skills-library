---
id: computing-software.cryptography-implementation.applied-cryptography.security-strength-equivalence-tables
name: security-strength-equivalence-tables
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, algorithm-selection, security-strength, security-strength-equivalence, sp-800-57, key-length, comparable-strength, keylength]
level: practitioner
status: docs-checked
description: "Match key sizes across algorithm families using SP 800-57 Pt1 Rev 5 Tables 2 and 3: symmetric, RSA/FFC, ECC and hash strengths, and the weakest-link rule."
sources: ["https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Security strength equivalence

A system is only as strong as its weakest algorithm. SP 800-57 Part 1 Rev. 5 Table 2 gives
comparable strengths (bits of security):

| Strength | Symmetric | FFC (DSA, DH, MQV) | IFC (RSA) | ECC (ECDSA, EdDSA, DH, MQV) |
|---|---|---|---|---|
| 80 | 2TDEA | L = 1024, N = 160 | k = 1024 | f = 160-223 |
| 112 | 3TDEA (footnote: deprecated through 2023, then disallowed for protection) | L = 2048, N = 224 | k = 2048 | f = 224-255 |
| 128 | AES-128 | L = 3072, N = 256 | k = 3072 | f = 256-383 |
| 192 | AES-192 | L = 7680, N = 384 | k = 7680 | f = 384-511 |
| 256 | AES-256 | L = 15360, N = 512 | k = 15360 | f = 512+ |

The table carries a note that the security-strength estimates for IFC and ECC will be
significantly affected when quantum computing becomes a practical consideration.

## Hashes (Table 3)
Strength depends on the output length and the application. For digital signatures and other
applications needing collision resistance, the smallest hashes per strength are: 112 bits
SHA-224, SHA-512/224, SHA3-224; 128 bits SHA-256, SHA-512/256, SHA3-256; 192 bits SHA-384, SHA3-384;
256 bits SHA-512, SHA3-512. For HMAC, KMAC, key derivation and random bit generation (which assume
pre-image resistance is what matters): 128 bits SHA-1 or KMAC128; 192 bits SHA-224, SHA-512/224,
SHA3-224; 256 bits SHA-256, SHA-512/256, SHA-384, SHA-512, SHA3 variants, KMAC256. A hash
with a larger output may also be used at a lower strength than it can support (SHA-512 for 128 bits).
Footnotes: SHA-1 has been shown to give under 80 bits for digital signatures; the HMAC/KMAC
strength assumes the key length and entropy are at least the strength; KDF strength assumes the
shared secret contains enough entropy; random bit generation assumes adequate entropy input.
Anything below 112 bits (80 in the tables) is no longer approved for applying protection to federal
information, though flexibility remains for processing already-protected data such as verifying
signatures.

## Applying the weakest-link rule
- Take the minimum across every component: cipher, key exchange or key wrap, signature
  algorithm, hash, KDF and the entropy of the input secret. An AES-256 key wrapped by RSA-2048 is
  112-bit protection by Table 2; an AES key derived from a password is limited by the password's
  entropy (the KDF footnote above).
- Pick a target strength first, then choose every component at or above it.

## Lifetime
SP 800-131A Rev. 2 states that SP 800-57 Part 1 includes a transition to a 128-bit security
strength in 2030, so information needing protection beyond 2030 should not rely on 112 bits.

## Verify
- [ ] Each system documents a target strength and lists every algorithm with its strength.
- [ ] No component falls below the target (key wrap, KDF, signature hash included).
- [ ] Data lifetime checked against the 2030 transition.

## Checked
Method: docs-checked 2026-11-09 against SP 800-57 Part 1 Rev. 5 Tables 2 and 3 with footnotes (downloaded PDF) and SP 800-131A Rev. 2 (2030 transition text). Removed the keylength.com and NIST PQ criteria sources (not read) and the PQ category mapping and curve-name annotations.
