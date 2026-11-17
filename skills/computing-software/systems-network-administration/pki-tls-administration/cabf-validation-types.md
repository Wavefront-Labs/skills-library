---
id: computing-software.systems-network-administration.pki-tls-administration.cabf-validation-types
name: cabf-validation-types
category: computing-software
field: systems-network-administration
product: pki-tls-administration
tags: [cabf-validation-types, pki-cabf, pki, cabf, baseline-requirements, validation, pki-tls-administration]
level: practitioner
status: draft
description: "Understand domain, organisation and extended validation, accepted DCV methods and which to pick for a deployment."
sources:
  - https://cabforum.org/working-groups/server/baseline-requirements/documents/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DV, OV and EV validation
Goal: choose the cheapest validation level that meets the trust need.
- DV: proves control of the domain only (policy OID 2.23.140.1.2.1). Used by ACME. Methods: HTTP file, DNS TXT/CNAME, TLS-ALPN, email to constrained addresses (confirm the current BR 3.2.2.4 list).
- OV: DV plus verified organisation name in the subject (2.23.140.1.2.2).
- EV: legal-entity checks per the EV Guidelines; browsers no longer show special UI, so value is mostly contractual.
- Wildcards require DNS-based control of the base domain.
- Domain validation reuse is shrinking with the lifetime schedule (see the 47-day plan).
- Private CAs are outside the BRs but should still lint against them if browsers or mail clients are involved.
Gotcha: a CNAME delegation of `_acme-challenge` lets one validator account issue for you; scope the delegation to a zone the automation owns.
Verify:
- [ ] Policy OID in the cert matches the product bought (`openssl x509 -noout -ext certificatePolicies`).
- [ ] Renewal path does not depend on a manual email approval.
