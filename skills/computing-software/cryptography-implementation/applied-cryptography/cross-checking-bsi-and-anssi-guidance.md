---
id: computing-software.cryptography-implementation.applied-cryptography.cross-checking-bsi-and-anssi-guidance
name: cross-checking-bsi-and-anssi-guidance
category: computing-software
field: cryptography-implementation
product: applied-cryptography
tags: [applied-cryptography, cryptography-implementation, bsi-tr-02102, anssi, key-length, algorithm-selection, keylength-recommendations]
level: practitioner
status: draft
description: "Cross-check algorithm and key-length choices against BSI TR-02102 and ANSSI guides alongside NIST, noting where European guidance is stricter (RSA 3000, hybrid PQ)."
sources: ["https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/Technische-Richtlinien/TR-nach-Thema-sortiert/tr02102/tr02102_node.html", "https://cyber.gouv.fr/publications/mecanismes-cryptographiques", "https://www.keylength.com/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cross-checking BSI and ANSSI guidance

## Where they differ from NIST (verify current editions; they update yearly)
| Item | NIST SP 800-57/131A | BSI TR-02102-1 | ANSSI guide |
|---|---|---|---|
| RSA/DH minimum | 2048 (to 2030) | 3000 for use beyond 2023 | 2048 to 2030, 3072 after |
| ECC | P-256+ | P-256+, Brainpool curves | P-256+, FRP256v1 accepted |
| Hash | SHA-256+ | SHA-256+, SHA-3 | SHA-256+ |
| PQ | ML-KEM alone acceptable | hybrid with classical recommended | hybrid required in transition |

## Process
1. List the jurisdictions your customers or certifications care about (BSI C5, ANSSI SecNumCloud, FIPS).
2. Take the strictest requirement per item as the default; document deviations.
3. Use keylength.com for a quick side-by-side, then confirm against the primary PDF before committing.
4. Record the edition year in the crypto policy; set a review date.

## Practical outcomes
- RSA 3072 or ECC P-256/P-384 satisfies all three for new keys.
- AES-128 is acceptable everywhere; AES-256 for long-term or PQ-motivated data.
- Plan hybrid ML-KEM + ECDH for European deployments rather than pure ML-KEM.

## Verify
- [ ] Crypto policy cites document IDs and versions (e.g. TR-02102-1 2025-01).
