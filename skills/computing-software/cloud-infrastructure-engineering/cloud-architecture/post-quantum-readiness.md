---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.post-quantum-readiness
name: post-quantum-readiness
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, data-protection, post-quantum-readiness, pqc, ml-kem, crypto-agility, cryptographic-inventory]
level: practitioner
status: draft
description: "Prepare cloud estates for post-quantum cryptography: crypto inventory, harvest-now-decrypt-later risk, hybrid ML-KEM TLS, crypto agility and migration roadmap."
sources: ["https://csrc.nist.gov/pubs/fips/203/final", "https://csrc.nist.gov/pubs/fips/204/final", "https://www.ncsc.gov.uk/whitepaper/next-steps-preparing-for-post-quantum-cryptography", "https://www.cisa.gov/quantum"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Post-quantum cryptography readiness

## Steps
1. **Cryptographic inventory**: where public-key crypto is used: TLS endpoints, VPNs, SSH,
   code signing, PKI, KMS asymmetric keys, data-at-rest wrapping, partner integrations, and
   libraries in use (CBOM tooling helps).
2. **Prioritise by data lifetime**: data that must stay confidential for many years is exposed
   to harvest-now-decrypt-later today; protect those channels first.
3. **Standards**: NIST FIPS 203 (ML-KEM, key establishment), FIPS 204 (ML-DSA) and FIPS 205
   (SLH-DSA) signatures, finalised August 2024. Symmetric AES-256 and SHA-2/3 remain fine.
4. **Hybrid key exchange first**: X25519 + ML-KEM-768 in TLS 1.3 is supported by major
   browsers and cloud edges/load balancers and SDKs progressively; enable where offered and
   test middleboxes (larger ClientHello).
5. **Crypto agility**: centralise crypto in libraries/services, avoid hard-coded algorithms,
   track provider PQC support (KMS PQ signatures, PQ TLS on endpoints).
6. **Roadmap** aligned to government timelines (e.g. NCSC target migration by 2035) and
   vendor contracts requiring PQC plans.

## Gotchas
- Old middleboxes fail on large TLS handshakes; test before enabling hybrid groups widely.
- Long-lived signing roots (firmware, PKI) take years to replace; start early.

## Verify
- [ ] Inventory with data-lifetime priority exists.
- [ ] Hybrid PQ key exchange enabled and tested on priority endpoints.
