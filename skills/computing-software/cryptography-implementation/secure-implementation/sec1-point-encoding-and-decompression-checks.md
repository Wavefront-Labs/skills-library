---
id: computing-software.cryptography-implementation.secure-implementation.sec1-point-encoding-and-decompression-checks
name: sec1-point-encoding-and-decompression-checks
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, sec1-point-encoding, point-validation, elliptic-curve, input-validation, ecdh, invalid-curve-attack]
level: advanced
status: gated
description: "Validate SEC1 elliptic-curve point encodings: 0x04 uncompressed, 0x02/0x03 compressed, length checks, on-curve verification after decompression, and identity rejection."
sources: ["https://www.secg.org/sec1-v2.pdf", "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-56Ar3.pdf", "https://github.com/C2SP/wycheproof"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SEC1 point encoding and decompression checks

## Encodings (SEC1 2.3.3-2.3.4)
| Prefix | Length (P-256) | Meaning |
|---|---|---|
| `0x00` | 1 | point at infinity (reject in protocols) |
| `0x04` | 65 | uncompressed X or Y |
| `0x02` / `0x03` | 33 | compressed, Y even / odd |
| `0x06` / `0x07` | 65 | hybrid, rarely supported; reject (pyca raises "Unsupported elliptic curve point type") |

## Checks before use
1. Length matches prefix exactly (no trailing bytes).
2. Coordinates are less than the field prime p (reject non-canonical values).
3. Uncompressed: verify `y^2 = x^3 + ax + b mod p`.
4. Compressed: compute `y = sqrt(x^3 + ax + b)`; if no square root exists, reject. Select the root with the
   parity in the prefix.
5. Not the identity; for curves with cofactor > 1, check order (SP 800-56A full validation).

Skipping the on-curve check enables invalid-curve attacks: an attacker sends points on a weaker curve and recovers
the static ECDH private key piece by piece (seen in JWT ECDH-ES libraries and Bluetooth pairing (gated: unconfirmed, source is paywalled or blocked)).

## Library behaviour
- OpenSSL `EC_POINT_oct2point` checks on-curve; Go `ecdh.P256().NewPublicKey` validates and rejects compressed;
  Java `KeyFactory` with `ECPublicKeySpec` validates on-curve in recent JDKs (gated: unconfirmed, source is paywalled or blocked); OpenSSL `EC_POINT_oct2point` is C and was not run here.
- Run here: pyca `from_encoded_point` on P-256 rejected trailing bytes, short input, an off-curve point, hybrid prefix 0x06 and the lone 0x00 byte; Go 1.22 `ecdh.P256().NewPublicKey` rejected a compressed point and an off-curve point (and accepted the valid uncompressed one).
- Hand-rolled decompression in embedded or JS code is where checks get skipped.

## Verify
- [ ] Wycheproof `ecdh_*_ecpoint_test.json` passes, including invalid points and compressed encodings.
