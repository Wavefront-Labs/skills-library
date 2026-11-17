---
id: computing-software.cryptography-implementation.key-management.pci-dss-key-management-requirements
name: pci-dss-key-management-requirements
category: computing-software
field: cryptography-implementation
product: key-management
tags: [key-management, cryptography-implementation, pci-dss-key-management, pci-dss, pci-dss-4, key-custodian, split-knowledge, dual-control, cryptoperiod, key-management-policy, compliance]
level: practitioner
status: draft
description: "Meet PCI DSS 4.0.1 requirements 3.6 and 3.7: key protection, KEK separation, split knowledge and dual control, cryptoperiods, custodians and evidence."
sources: ["https://docs-prv.pcisecuritystandards.org/PCI%20DSS/Standard/PCI-DSS-v4_0_1.pdf", "https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final", "https://listings.pcisecuritystandards.org/documents/PCI_PIN_Security_Requirements_v3.1.pdf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# PCI DSS key management requirements (3.6 and 3.7)

## 3.6 - protect keys used for stored account data
| Req | What it means in practice |
|---|---|
| 3.6.1 | Access to keys restricted to the fewest custodians; KEKs at least as strong as the DEKs they protect; KEKs stored separately from DEKs; keys in the fewest locations |
| 3.6.1.1 | (Service providers) documented crypto architecture: algorithms, protocols, keys, strength, expiry, usage, HSM/SCD inventory |
| 3.6.1.2 | Secret/private keys stored only as: encrypted under a KEK, inside an SCD (HSM, PTS-approved device), or as at least two full-length components/shares |
| 3.6.1.3 | Clear-text key component access restricted |
| 3.6.1.4 | Keys stored in the fewest possible locations |

## 3.7 - key-management lifecycle procedures
| Req | Procedure required |
|---|---|
| 3.7.1 | Strong key generation |
| 3.7.2 | Secure key distribution |
| 3.7.3 | Secure key storage |
| 3.7.4 | Key change at end of defined cryptoperiod |
| 3.7.5 | Retirement/replacement when integrity weakened or compromise suspected |
| 3.7.6 | Manual clear-text key operations use split knowledge and dual control |
| 3.7.7 | Prevent unauthorised key substitution |
| 3.7.8 | Key custodians formally acknowledge their responsibilities |
| 3.7.9 | (Service providers) guidance to customers for keys they share |

## Key custodians (3.7.8)
- Name custodians per key or component; no custodian holds more than one component of the same key.
- Signed acknowledgement form: duties, confidentiality, reporting suspected compromise, return of materials on exit;
  re-acknowledge annually and on role change.
- Backup custodians so one absence does not block operations.

## Evidence assessors ask for
- Key inventory with cryptoperiods; rotation records (KMS rotation config, ceremony logs).
- HSM/KMS policies showing who can use and manage keys; separation between key admins and key users.
- Ceremony scripts with component KCVs and dual sign-off.
- Custodian acknowledgement forms.

## Cloud KMS mapping
KMS/HSM-backed keys satisfy 3.6.1.2 (SCD) and simplify 3.7.6 (no clear-text components). You still need written
procedures, defined cryptoperiods, and access control evidence.

## Verify
- [ ] Each 3.6/3.7 sub-requirement maps to a procedure document and an evidence artifact.
- [ ] Custodian acknowledgements are current.
