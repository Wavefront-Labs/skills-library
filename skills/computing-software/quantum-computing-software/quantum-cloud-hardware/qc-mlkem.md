---
id: computing-software.quantum-computing-software.quantum-cloud-hardware.qc-mlkem
name: qc-mlkem
category: computing-software
field: quantum-computing-software
product: quantum-cloud-hardware
tags: [ml-kem, nist-pqc-standards]
level: practitioner
status: draft
description: "Use ML-KEM-512/768/1024 for key establishment, know sizes and the encapsulate and decapsulate flow."
sources:
  - https://openqasm.com/
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ML-KEM (FIPS 203) key encapsulation
- FIPS 203 (2024), derived from CRYSTALS-Kyber; sets: ML-KEM-512, ML-KEM-768, ML-KEM-1024; shared secret 32 bytes.
- ML-KEM-768 sizes: encapsulation key 1184 B, ciphertext 1088 B.
```python
import oqs   # liboqs-python; algorithm name may be "ML-KEM-768" or legacy "Kyber768" depending on build
with oqs.KeyEncapsulation("ML-KEM-768") as kem:
    pk = kem.generate_keypair(); ct, ss = kem.encap_secret(pk)
```
- Use a vetted library (OpenSSL 3.5+, liboqs, BoringSSL, language-native crypto libs); never implement it yourself.

## Gotchas
- KEMs are not encryption; feed the shared secret into a KDF and AEAD.

## Self-check
Verify encap and decap secrets match.
