---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.architecture-waiver
name: architecture-waiver
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, implementation-governance, togaf, architecture-waiver, dispensation, exception-management]
level: practitioner
status: draft
description: "Handle architecture waivers and dispensations: request content, risk assessment, time-boxed approval, compensating controls and expiry tracking."
sources: ["https://pubs.opengroup.org/togaf-standard/architecture-capability/chap03.html", "https://pubs.opengroup.org/togaf-standard/architecture-capability/chap05.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Waivers and dispensations

A dispensation (TOGAF) is granted when a project cannot conform to the architecture; it is
time-bound and comes with conditions. Unmanaged exceptions become the de facto architecture.

## Request content
- Standard or principle being waived and the exact deviation.
- Business reason and why conformance is not feasible now.
- Risk assessment (security, operability, cost, lock-in) and compensating controls.
- Duration and the remediation plan to return to conformance.
- Requester, accountable owner (senior enough to own the risk).

## Steps
1. **Triage**: low-risk deviations approved by a domain architect; high-risk by the board
   with security and risk present.
2. **Approve time-boxed** (typically 3-12 months) with conditions; never open-ended.
3. **Record** in a waiver register: ID, scope (resources affected - tag them, e.g.
   `waiver-id=ARB-2026-014`), conditions, expiry.
4. **Policy-as-code exemptions** reference the waiver ID and expiry date (Azure Policy
   exemptions support `expiresOn`; for SCPs or OPA use an exemption list with dates).
5. **Expiry**: notify owners 30 days ahead; renewals need fresh justification and progress evidence.
6. **Report** count and age of waivers; many waivers on one standard means the standard needs revisiting.

## Gotchas
- Waivers without resource tagging cannot be audited.
- Silent renewals turn exceptions into permanent debt.

## Verify
- [ ] Every active waiver has an expiry date and an owner.
- [ ] No policy exemption exists without a matching register entry.
