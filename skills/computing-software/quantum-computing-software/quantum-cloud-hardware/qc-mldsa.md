---
id: computing-software.quantum-computing-software.quantum-cloud-hardware.qc-mldsa
name: qc-mldsa
category: computing-software
field: quantum-computing-software
product: quantum-cloud-hardware
tags: [ml-dsa]
level: practitioner
status: draft
description: "Sign and verify with ML-DSA-44/65/87, noting key and signature sizes and context strings."
sources:
  - https://openqasm.com/
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ML-DSA (FIPS 204) signatures
- FIPS 204 (2024), derived from CRYSTALS-Dilithium. ML-DSA-65: public key 1952 B, signature 3309 B.
- ML-DSA-44 sizes 1312/2420 B; ML-DSA-87 2592/4627 B.
```bash
openssl genpkey -algorithm ML-DSA-65 -out key.pem    # OpenSSL 3.5 or later, unconfirmed on your build
openssl pkeyutl -sign -inkey key.pem -rawin -in msg -out sig
```
- Signature sizes affect certificate chains and TLS handshake sizes.

## Gotchas
- Randomized vs deterministic signing is a parameter; follow your protocol profile.

## Self-check
Verify a tampered message fails.
