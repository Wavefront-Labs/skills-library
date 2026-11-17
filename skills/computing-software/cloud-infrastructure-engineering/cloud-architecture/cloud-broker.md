---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cloud-broker
name: cloud-broker
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, cloud-ecosystem, cloud-broker, managed-service-provider, msp, nist-reference-architecture, csp-reseller]
level: practitioner
status: draft
description: "Engage a cloud broker, reseller or MSP well: NIST broker roles, responsibility matrix, billing relationship, access model, SLAs and exit terms."
sources: ["https://www.nist.gov/publications/nist-cloud-computing-reference-architecture", "https://learn.microsoft.com/partner-center/csp-overview", "https://aws.amazon.com/partners/programs/msp/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud broker and MSP engagement model

NIST SP 500-292 defines a cloud broker as an entity that manages use, performance and delivery
of cloud services: **intermediation** (adds value such as monitoring or security),
**aggregation** (combines several providers) and **arbitrage** (chooses providers dynamically).
In practice: resellers (Microsoft CSP, AWS Solution Provider), MSPs and consultancies.

## Steps
1. **Decide what you buy**: billing only (reseller), operations (24x7 monitoring, patching,
   backup), engineering capacity, or FinOps services. Scope drives the contract shape.
2. **Responsibility matrix (RACI)** per domain: identity, network, patching, backup, incident
   response, cost management, security monitoring. Make the customer's retained duties explicit.
3. **Billing relationship**: under reseller models the partner owns the billing account; check
   you still get full cost and usage exports, discount transparency and the right to move
   the account.
4. **Access model**: partner uses your identity provider or delegated admin with
   least-privilege roles, JIT elevation and full audit logging; no shared root credentials.
5. **SLAs**: response and resolution times by severity, reporting cadence, named contacts,
   service credits.
6. **Exit**: transfer of accounts, runbooks, IaC, credentials and documentation; assistance period.

## Gotchas
- Some reseller agreements restrict which support plan or marketplace purchases you can use.
- Standing global-admin access for a partner is a top breach path; audit it quarterly.

## Verify
- [ ] RACI signed; partner access reviewed in the last quarter.
- [ ] Cost exports available to you directly.
