---
id: computing-software.quantum-computing-software.quantum-cloud-hardware.qc-slhdsa
name: qc-slhdsa
category: computing-software
field: quantum-computing-software
product: quantum-cloud-hardware
tags: [slh-dsa]
level: advanced
status: draft
description: "Understand SLH-DSA parameter sets, large signatures and stateless hash-based assurance."
sources:
  - https://openqasm.com/
  - https://quantum.cloud.ibm.com/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SLH-DSA (FIPS 205) hash-based signatures
- FIPS 205 (2024), derived from SPHINCS+; parameter sets SLH-DSA-SHA2/SHAKE-128/192/256 with s (small) or f (fast) variants.
- SLH-DSA-SHA2-128s: public key 32 B, signature 7856 B; 128f signature 17088 B.
- Security relies only on hash functions; stateless unlike LMS/XMSS.

## Gotchas
- Signatures are large and signing is slow; reserve for roots and firmware.

## Self-check
Compare signature sizes of s vs f.
