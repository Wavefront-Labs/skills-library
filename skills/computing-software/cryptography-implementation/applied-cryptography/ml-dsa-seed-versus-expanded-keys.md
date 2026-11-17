---
id: computing-software.cryptography-implementation.applied-cryptography.ml-dsa-seed-versus-expanded-keys
name: ml-dsa-seed-versus-expanded-keys
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, ml-dsa-key-format, ml-dsa, fips-204, pkcs8, private-key-seed, openssl]
level: advanced
status: docs-checked
description: "Store and exchange ML-DSA private keys correctly: 32-byte seed versus expanded key, RFC 9881 PKCS#8 choices, and OpenSSL 3.5 output formats."
sources: ["https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf", "https://datatracker.ietf.org/doc/rfc9881/", "https://docs.openssl.org/3.5/man7/EVP_PKEY-ML-DSA/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ML-DSA seed versus expanded private keys

## Two representations
- **Seed**: 32-byte `xi` passed to `ML-DSA.KeyGen_internal`. Everything else is derived deterministically.
- **Expanded key**: 2560 (ML-DSA-44), 4032 (65) or 4896 (87) bytes containing rho, K, tr, s1, s2, t0.

## Prefer the seed
- Smaller to store, wrap and back up; one canonical value.
- The expanded key is derived from the seed; the seed cannot be recovered from it.
- RFC 9881 (ML-DSA in X.509 / PKCS#8) defines a CHOICE: `seed`, `expandedKey`, or `both`; the seed format is RECOMMENDED as most compact. A recipient of `both` SHOULD check the seed and expanded key match.

## OpenSSL 3.5
```sh
openssl genpkey -algorithm ML-DSA-65 -out k.pem
openssl genpkey -algorithm ML-DSA-65 -provparam ml-dsa.output_formats=seed-only -out seed.pem
```
Provider params `ml-dsa.input_formats` / `output_formats` control which encodings are accepted and written.
The `ml-dsa.prefer_seed` provider parameter chooses seed or companion key when a PKCS#8 file holds both.

## Interop pitfalls
- Peers may support only some of the three formats (RFC 9881 notes some only support expanded keys). Agree the format per peer.
- RFC 9881 says to tell the CHOICE variants apart by their ASN.1 tags (0x80 seed, 0x04 expandedKey, 0x30 both), not by length.

## Verify
- [ ] Key round-trips through the peer library; signature from one verifies in the other.

## Checked
2026-11-01. Confirmed in the FIPS 204 PDF: 32-byte seed xi and private key sizes 2560, 4032 and 4896 bytes. Confirmed in RFC 9881: seed/expandedKey/both CHOICE, seed RECOMMENDED, consistency check, tag-based parsing. Confirmed in the OpenSSL 3.5 EVP_PKEY-ML-DSA page: `ml-dsa.input_formats`, `ml-dsa.output_formats`, `seed-only` and `ml-dsa.prefer_seed`. Removed the contents list of the expanded key, the `pkey -text` comment, the claim that OpenSSL checks both on import, and the draft-era encoding remark.
Method: documentation only; no commands were run.
