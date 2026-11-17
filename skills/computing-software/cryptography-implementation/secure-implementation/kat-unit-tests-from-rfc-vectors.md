---
id: computing-software.cryptography-implementation.secure-implementation.kat-unit-tests-from-rfc-vectors
name: kat-unit-tests-from-rfc-vectors
category: computing-software
field: cryptography-implementation
product: secure-implementation
tags: [secure-implementation, cryptography-implementation, rfc-test-vectors, known-answer-tests, test-vectors, kat, crypto-testing, wycheproof, cavp, unit-tests]
level: practitioner
status: verified
description: "Turn RFC and NIST test vectors into table-driven known-answer tests: where to find vectors per primitive, file formats, negative vectors and provenance tracking."
sources: ["https://www.rfc-editor.org/rfc/rfc8439#appendix-A", "https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program", "https://github.com/C2SP/wycheproof"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# KAT unit tests from RFC vectors

## Where vectors live
| Primitive | Source |
|---|---|
| ChaCha20, Poly1305, ChaCha20-Poly1305 | RFC 8439 Appendix A |
| HKDF | RFC 5869 Appendix A |
| HMAC-SHA-2 | RFC 4231 |
| Ed25519 / Ed448 | RFC 8032 section 7 |
| X25519 / X448 | RFC 7748 sections 5.2 and 6 |
| AES-GCM, SHA-2, SHA-3, DRBGs, ECDSA, RSA | NIST CAVP response files; ACVP JSON |
| HPKE | RFC 9180 Appendix A (and test-vectors.json in the CFRG repo) |
| ML-KEM / ML-DSA / SLH-DSA | NIST ACVP server JSON; C2SP CCTV has ML-KEM and ML-DSA directories (no SLH-DSA directory at time of writing) |
| TLS 1.3 key schedule | RFC 8448 traces |
| Edge cases (invalid inputs) | Wycheproof JSON per algorithm |

## Table-driven pattern (pytest)
```python
import json, pytest
VECTORS = json.load(open("tests/vectors/hkdf_rfc5869.json"))   # transcribed once, with source noted
@pytest.mark.parametrize("v", VECTORS, ids=lambda v: v["name"])
def test_hkdf(v):
    okm = hkdf_sha256(bytes.fromhex(v["ikm"]), bytes.fromhex(v["salt"]), bytes.fromhex(v["info"]), v["L"])
    assert okm.hex() == v["okm"]
```
Store vectors as data files with a header naming the source document, section and retrieval date. Hand-copying hex
into code invites typos that make a test pass trivially or fail mysteriously.

## Rules
- Test both directions (encrypt and decrypt, sign and verify).
- Include negative vectors: wrong tag, invalid point, non-canonical encoding. Wycheproof labels each with
  `result: valid|invalid|acceptable` (acceptable is for legacy cases, weak parameters or common BER encodings; check the `flags`).
- Run KATs at build time and, for FIPS-style modules, at startup (self-tests).
- When a vector fails, check endianness and encoding (hex vs base64, big- vs little-endian integers) before assuming
  the implementation is wrong.

## Verify
- [ ] Every primitive used has at least one standards vector and one negative vector.
- [ ] Vector files record provenance.
