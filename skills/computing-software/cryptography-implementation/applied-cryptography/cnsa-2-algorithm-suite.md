---
id: computing-software.cryptography-implementation.applied-cryptography.cnsa-2-algorithm-suite
name: cnsa-2-algorithm-suite
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, cnsa-2-suite, cnsa-2, cnsa, national-security-systems, ml-kem-1024, ml-dsa-87, lms, xmss, aes-256, sha-384, pq-migration]
level: practitioner
status: draft
description: "Apply NSA CNSA 2.0: required algorithms and parameters (AES-256, SHA-384, ML-KEM-1024, ML-DSA-87, LMS/XMSS) and the per-category transition deadlines."
sources: ["https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0_FAQ_.PDF", "https://media.defense.gov/2025/May/30/2003728741/-1/-1/0/CSA_CNSA_2.0_ALGORITHMS.PDF", "https://www.cnss.gov/CNSS/issuances/Policies.cfm"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# CNSA 2.0 algorithm suite

CNSA 2.0 is NSA's required algorithm suite for US National Security Systems (and anyone selling into them).

## Algorithms
| Function | CNSA 2.0 | CNSA 1.0 (being replaced) |
|---|---|---|
| Symmetric encryption | AES-256 | AES-256 |
| Hashing | SHA-384 or SHA-512 | SHA-384 |
| Key establishment | ML-KEM-1024 | ECDH P-384, DH/RSA 3072+ |
| Signatures | ML-DSA-87 | ECDSA P-384, RSA 3072+ |
| Software/firmware signing | LMS or XMSS (SP 800-208; SHA-256/192 parameter sets allowed) | |

Only the highest parameter sets are allowed: ML-KEM-512/768 and ML-DSA-44/65 do not qualify. AES-128 and SHA-256
(outside LMS/XMSS) do not qualify.

## Transition timeline (support and prefer by / exclusive use by)
| Category | Prefer by | Exclusive by |
|---|---|---|
| Software and firmware signing | 2025 | 2030 |
| Web browsers, servers, cloud services | 2025 | 2033 |
| Traditional networking equipment (VPNs, routers) | 2026 | 2030 |
| Operating systems | 2027 | 2033 |
| Niche equipment | 2030 | 2033 |
| Custom applications and legacy equipment | update or replace by 2033 | |
NSS overall: quantum-resistant only by 2035.

## Practical implications
- Hybrid (e.g. X25519MLKEM768) is a commercial migration path but CNSA 2.0 expects ML-KEM-1024; check whether the
  program accepts hybrids during transition (NSA has said it will not require them).
- Firmware signing is the earliest deadline: adopt LMS/HSS with careful state management now.
- Protocol profiles: IETF drafts define CNSA 2.0 profiles for TLS, IPsec, SSH and CMS; follow them rather than
  picking parameters ad hoc.

## Verify
- [ ] Inventory flags every algorithm below CNSA 2.0 parameters for NSS-bound products.
- [ ] Firmware signing roadmap uses LMS/XMSS with state handling.
