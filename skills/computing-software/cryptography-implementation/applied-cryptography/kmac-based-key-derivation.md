---
id: computing-software.cryptography-implementation.applied-cryptography.kmac-based-key-derivation
name: kmac-based-key-derivation
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, kmac-kdf, kmac, sp-800-108, sp-800-185, sha3, key-derivation]
level: advanced
status: docs-checked
description: "Derive keys with KMAC128/KMAC256 per SP 800-108r1 section 4.4 and SP 800-185: key, context, output length and label roles, and why KMACXOF is not allowed."
sources: ["https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-108r1-upd1.pdf", "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-185.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KMAC-based key derivation

## Construction (SP 800-108r1 4.4)
`KOUT = KMAC#(KIN, Context, L, Label)`, where `KMAC#` is KMAC128 or KMAC256, KIN is the key-derivation key,
`Context` is the information related to the derived keying material, L is the output length in bits, and `Label` is
the optional customization string S (the publication's example is the 8-bit ASCII encoding of "KDF" or "KDF4X").
No iteration is needed: KMAC outputs the required length in one call.

Because L is encoded into KMAC's input (`right_encode(L)`), asking for 32 bytes vs 64 bytes yields unrelated
outputs, not a prefix of each other.

## Choosing
- Good fit when the stack is already SHA-3 based (ML-KEM/ML-DSA implementations carry Keccak).
- Pick KMAC128 or KMAC256 to match the strength you need.
- The key may be any length, including zero, per SP 800-185; still use a full-strength secret as KIN.

## Pitfalls
- SP 800-185 names the parameters K (key), X (main input), L and S (customization); do not swap Label (S) and
  Context (X).
- KMACXOF128/KMACXOF256 encode length as `right_encode(0)` and are a different function from KMAC with fixed L.
  SP 800-108r1 says the KDF must use KMAC128 or KMAC256 because the output length must be known before the call.

## Verify
- [ ] Cross-check derived keys between two implementations using the same key, context, label and L.

## Checked
2026-11-01. Confirmed in SP 800-108r1-upd1 section 4.4 (KMAC#(K, X, L, S) parameters, Label example, no iteration,
KMACXOF excluded) and SP 800-185 (right_encode(L) in KMAC, right_encode(0) in KMACXOF, key and customization of
any length). Removed: the OpenSSL command and parameter names, and the claim that S is always "KDF" || Label
(the publication gives "KDF" as an example only).
Method: documentation only; no commands were run.
