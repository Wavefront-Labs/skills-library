---
id: computing-software.cryptography-implementation.applied-cryptography.ml-kem-input-validation
name: ml-kem-input-validation
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [cryptography-implementation, applied-cryptography, ml-kem, ml-kem-input-validation, fips-203, encapsulation-key-check, implicit-rejection, ciphertext-validation]
level: advanced
status: docs-checked
description: "Apply FIPS 203 input checks for ML-KEM: encapsulation key length and modulus check, decapsulation input checks, and handling implicit rejection."
sources: ["https://csrc.nist.gov/pubs/fips/203/final", "https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ML-KEM encapsulation key and ciphertext input checks

FIPS 203 sections 7.2 and 7.3 require input checking: Encaps and Decaps
shall only run on inputs that have been checked.

## Encapsulation key (before Encaps)

1. **Type check**: length is exactly 384k + 32 bytes (800, 1184, 1568).
2. **Modulus check**: `ByteEncode12(ByteDecode12(ek[0:384k]))` must equal
   `ek[0:384k]`. This ensures every encoded integer is in [0, q-1], q = 3329.

If either fails, input checking has failed: do not run Encaps. The key need
not be checked by the encapsulating party on every run, if assurance that it
was checked comes from elsewhere (SP 800-227).

## Decapsulation (before Decaps)

1. Ciphertext length is exactly 32(du*k + dv) bytes (768, 1088, 1568).
   Ciphertext checking shall be done on every Decaps call.
2. Decapsulation key length is 768k + 96 bytes (1632, 2400, 3168).
3. Hash check: `H(dk[384k : 768k+32])` equals `dk[768k+32 : 768k+64]`.
   The dk check need not run on every Decaps (for example once at key load).

Passing these checks does not prove the key or ciphertext was properly
generated.

## Implicit rejection

A well-formed but invalid ciphertext does not produce an error: Decaps
returns a value derived by hashing the stored random value `z` with the
ciphertext (J(z || c)). Consequences:

- The comparison flag inside Decaps is secret intermediate data; FIPS 203
  forbids returning it in any form, so do not add your own "decapsulation
  failed" signal. Failure shows up later, when key confirmation or AEAD
  decryption with the derived key fails.
- Make that later failure look identical to any other decrypt failure.

## Verify

- [ ] Out-of-range coefficients in ek are rejected before Encaps.
- [ ] Wrong-length ciphertexts and keys are rejected before Decaps.
- [ ] Tampered ciphertexts produce the same external error as other failures.

## Checked

2026-11-01. Confirmed against FIPS 203 (NIST.FIPS.203.pdf): sections 7.2
and 7.3 checks, key and ciphertext sizes (Table 3), implicit rejection and
the secret-flag rule (6.3, Algorithm 18). Removed: Go crypto/mlkem,
KyberSlash, liboqs, Bouncy Castle, OpenSSL and C2SP test-vector claims
(not read this batch).
Method: documentation only; no commands were run.
