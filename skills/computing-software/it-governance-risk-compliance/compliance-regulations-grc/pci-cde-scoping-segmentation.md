---
id: computing-software.it-governance-risk-compliance.compliance-regulations-grc.pci-cde-scoping-segmentation
name: pci-cde-scoping-segmentation
category: computing-software
field: it-governance-risk-compliance
product: compliance-regulations-grc
tags:
- compliance-regulations-grc
- pci-cde-scoping-segmentation
- pci-scope
level: practitioner
status: draft
description: 'Scope the PCI cardholder data environment: data flows, in-scope and connected-to systems, segmentation validation and scope reduction.'
sources:
- https://www.pcisecuritystandards.org/
- https://gdpr-info.eu/
- https://csrc.nist.gov/projects/olir
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cardholder data environment scoping and segmentation
**Goal:** the smallest defensible CDE.
- In scope: system components that store, process or transmit cardholder data (CHD) or sensitive authentication data, and systems connected to or able to impact the security of the CDE.
- Method: map card data flows, inventory systems, apply segmentation, test it (penetration testing of segmentation per Requirement 11.4), document scope (v4 formalises scoping confirmation under 12.5.2, annually).
- Reduce scope: P2PE solutions, tokenisation, hosted payment pages/iframes from a PCI-compliant provider.

## Gotchas
- Segmentation is not a PCI requirement but unvalidated segmentation leaves all networks in scope.
- Never store sensitive authentication data (full track, CVV, PIN) after authorisation.

## Self-check
Draw the data-flow diagram and mark each system with its scope reason.
