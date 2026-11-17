---
id: computing-software.it-governance-risk-compliance.nist-csf-800-53.nist800171-cui-requirements
name: nist800171-cui-requirements
category: computing-software
field: it-governance-risk-compliance
product: nist-csf-800-53
tags:
- nist-csf-800-53
- nist800171-cui-requirements
- nist-800-171-cmmc
level: practitioner
status: draft
description: Protect controlled unclassified information in non-federal systems with SP 800-171 requirement families, SSP, POA&M and scoping.
sources:
- https://www.nist.gov/cyberframework
- https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final
- https://csrc.nist.gov/pubs/sp/800/37/r2/final
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SP 800-171 requirements for CUI
**Goal:** scope and implement 800-171.
- Rev 2 has 110 requirements across 14 families (access control, audit, config management, identification and authentication, incident response, maintenance, media protection, personnel security, physical, risk assessment, security assessment, system and communications protection, system and information integrity, awareness and training). Rev 3 (2024) restructures to 97 requirements in 17 families; which revision a contract cites should be confirmed.
- Assessment per SP 800-171A; score using DoD Assessment Methodology where the DFARS clause applies.
- Define CUI boundary; consider enclave to reduce scope.

## Self-check
Identify the CUI data flows and mark every system that stores, processes or transmits CUI.
