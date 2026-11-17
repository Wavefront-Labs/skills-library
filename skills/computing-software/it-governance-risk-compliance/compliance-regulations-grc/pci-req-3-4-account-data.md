---
id: computing-software.it-governance-risk-compliance.compliance-regulations-grc.pci-req-3-4-account-data
name: pci-req-3-4-account-data
category: computing-software
field: it-governance-risk-compliance
product: compliance-regulations-grc
tags:
- compliance-regulations-grc
- pci-req-3-4-account-data
level: practitioner
status: draft
description: Implement PCI DSS Requirements 3 (protect stored account data) and 4 (protect cardholder data in transit with strong cryptography).
sources:
- https://www.pcisecuritystandards.org/
- https://gdpr-info.eu/
- https://csrc.nist.gov/projects/olir
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Req 3-4 stored and transmitted account data
**Goal:** minimise and protect PAN.
- Req 3: keep storage to a minimum (retention policy), do not store SAD after authorisation, mask PAN when displayed (first six and last four maximum), render PAN unreadable where stored (strong cryptography, truncation, tokens, hashing with keyed hash), manage keys (generation, distribution, storage, rotation, retirement).
- Req 4: strong cryptography on open public networks (TLS), certificate inventory (v4), no PAN in end-user messaging unless protected.
- Find unknown PAN with a data discovery scan.

## Self-check
Run a PAN discovery scan across file shares and databases and reconcile with the data inventory.
