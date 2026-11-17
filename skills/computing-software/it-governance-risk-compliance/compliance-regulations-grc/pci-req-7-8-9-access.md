---
id: computing-software.it-governance-risk-compliance.compliance-regulations-grc.pci-req-7-8-9-access
name: pci-req-7-8-9-access
category: computing-software
field: it-governance-risk-compliance
product: compliance-regulations-grc
tags:
- compliance-regulations-grc
- pci-req-7-8-9-access
level: practitioner
status: draft
description: Implement PCI DSS Requirements 7 (need-to-know access), 8 (identify users and authenticate, MFA) and 9 (physical access to cardholder data).
sources:
- https://www.pcisecuritystandards.org/
- https://gdpr-info.eu/
- https://csrc.nist.gov/projects/olir
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Req 7-9 access control and physical access
**Goal:** access evidence.
- Req 7: access by business need and job role; review user accounts and privileges every six months (v4).
- Req 8: unique IDs, MFA for all access into the CDE (v4 extends from admin to all CDE access), passwords of at least 12 characters (v4) or equivalent strength, service account management.
- Req 9: physical entry controls, visitor logs, media handling, POI device inspection.

## Self-check
List all accounts with CDE access and confirm MFA enforced for each path.
