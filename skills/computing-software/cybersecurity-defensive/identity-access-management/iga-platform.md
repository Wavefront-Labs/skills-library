---
id: computing-software.cybersecurity-defensive.identity-access-management.iga-platform
name: iga-platform
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [iga-platform, identity-governance, sailpoint, saviynt, entra-id-governance, provisioning-connectors, sod-policies]
level: advanced
status: draft
description: "Operate an IGA platform: authoritative sources, connectors and aggregation, role and SoD models, certification campaigns, provisioning reconciliation and health metrics."
sources: ["https://documentation.sailpoint.com/", "https://learn.microsoft.com/en-us/entra/id-governance/identity-governance-overview", "https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IGA platform operation

## Building blocks
| Component | What to get right |
|---|---|
| Authoritative sources | HR (employees), VMS/contractor register, with unique immutable ID; correlation rules to accounts |
| Connectors / aggregation | Read accounts and entitlements from AD, Entra, SaaS, databases, mainframe; schedule (daily), delta where possible |
| Correlation | Map each account to an identity; uncorrelated accounts are orphans for review |
| Entitlement catalogue | Owner, description in business language, risk level for every entitlement |
| Roles | Birthright roles (by department/location) and business roles; mined from data, approved by owners |
| SoD policies | Toxic combinations (create vendor + approve payment); preventive at request, detective in campaigns |
| Access requests | Approval chains (manager + entitlement owner), justification |
| Certifications | Manager and entitlement-owner campaigns; risk-based frequency |
| Provisioning | Direct (connector writes) or ticketed (manual fulfilment) with closed-loop verification |

## Operations
- Reconciliation: compare requested vs actual; flag out-of-band grants (granted directly in the target) for revocation or approval.
- Health metrics: connector failures, aggregation age, orphan count, open certification items, SoD violations, mean time to deprovision.
- Change management for connectors and correlation rules - a broken rule can mass-disable accounts. Use preview/simulation mode.

## Gotchas
- Rubber-stamp certifications (approve-all in seconds); track decision time, show usage data (last login) to reviewers.
- Manual fulfilment without verification leaves revocations undone.
- Starting with role mining before data quality is clean produces garbage roles.

## Verify
- [ ] All connected systems aggregated within 24 h.
- [ ] Leaver deprovisioned in all connected systems within SLA (sample test).
- [ ] SoD violations have mitigating controls or removal.
