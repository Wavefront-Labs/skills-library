---
id: computing-software.cryptography-implementation.applied-cryptography.sp-800-131a-legacy-use
name: sp-800-131a-legacy-use
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, legacy-use-only, sp-800-131a, deprecated-algorithms, disallowed-algorithms, transition, sha-1, tdea, rsa-1024, crypto-policy]
level: practitioner
status: docs-checked
description: "Apply SP 800-131A Rev 2 acceptable, deprecated, disallowed and legacy-use categories: keep decrypt and verify paths for old data while blocking new encrypt and sign."
sources: ["https://csrc.nist.gov/pubs/sp/800/131/a/r2/final"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SP 800-131A legacy-use status

## Categories (section 1.2.3)
| Status | Meaning |
|---|---|
| Acceptable | Safe to use; no security risk currently known when used per the associated guidance. |
| Deprecated | May be used, but the user must accept some security risk; used when discussing algorithms for applying cryptographic protection. |
| Disallowed | No longer allowed for applying cryptographic protection. |
| Legacy use | May be used only to process already protected information, for example decrypting ciphertext or verifying a signature. |

Deprecated and legacy-use carry a risk that increases over time; if the user decides the risk is
unacceptable, the algorithm is disallowed from that user's perspective.

## Examples in Rev. 2
| Algorithm | Applying protection | Processing |
|---|---|---|
| Two-key TDEA | Encryption disallowed | Decryption: legacy use (modes in SP 800-38A) |
| Three-key TDEA | Deprecated through 31 Dec 2023, disallowed after that unless other NIST guidance allows; may continue in existing applications but not new ones; at most 2^20 blocks per single key bundle (SP 800-67) | Decryption: legacy use |
| SKIPJACK | Encryption disallowed | Decryption: legacy use |
| AES-128, AES-192, AES-256 | Acceptable | Acceptable |
| SHA-1 | Signature generation disallowed except where NIST protocol-specific guidance allows | Signature verification: legacy use; non-signature applications acceptable if collision resistance is not required |
| SHA-224, SHA-256, SHA-384, SHA-512, SHA-512/224, SHA-512/256 and SHA3-224/256/384/512 | Acceptable for all hash applications | |
| RSA signature generation with len(n) < 2048 (also DSA/ECDSA below 112 bits) | Disallowed | Verification of RSA 1024 <= len(n) < 2048: legacy use |

## Implementing legacy-use in code
- Split the APIs: the encrypt and sign functions accept only current algorithms; decrypt and
  verify accept legacy identifiers from a short allowlist.
- Log and count every legacy-path use so you can drive it toward zero.
- Re-protect on read where possible: decrypt with the legacy algorithm, then encrypt with a
  current one.

## Verify
- [ ] Tests show encrypt and sign paths reject disallowed algorithms.
- [ ] Legacy-use counts exist and trend down.

## Checked
Method: docs-checked 2026-11-09 against SP 800-131A Rev. 2 (section 1.2.3 definitions, encryption table and TDEA text, hash table 8 text, digital signature table; downloaded PDF). Removed Rev. 3 draft and IR 8547 claims, the OpenSSL, Java and RHEL policy settings and the timestamped SHA-1 advice (sources not read).
