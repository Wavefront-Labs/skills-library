---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.cloud-contract-review
name: cloud-contract-review
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, ecosystem-roles, cloud-contract-review, dpa, customer-agreement, liability, data-processing-agreement, exit-assistance, cloud-procurement]
level: practitioner
status: draft
description: "Review a cloud provider agreement and DPA: service terms, SLA credits, liability caps, data location, sub-processors, audit rights, suspension and termination assistance."
sources: ["https://aws.amazon.com/agreement/", "https://www.microsoft.com/licensing/terms/product/ForOnlineServices/all", "https://cloud.google.com/terms", "https://gdpr-info.eu/art-28-gdpr/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cloud contract and DPA review

Architects are not lawyers, but they must flag the technical terms that change the design.

## Documents in a typical stack
Customer/enterprise agreement, service-specific terms, SLA pages, Data Processing Addendum (GDPR
Art. 28), acceptable use policy, support terms, any negotiated enterprise discount addendum.
SLAs and service terms are usually incorporated by URL and can change; note the version date.

## Technical clauses to check
| Clause | Why the architect cares |
|---|---|
| SLA definition and exclusions | Credit is the only remedy; drives your own redundancy |
| Data location | Whether "region" commitments cover backups, support access, telemetry |
| Sub-processors | Notification period and objection right |
| Security / audit rights | Access to SOC/ISO reports instead of on-site audits |
| Suspension | When the provider may suspend (non-payment, AUP); design for account-level blast radius |
| Termination / exit | Data retrieval window after termination; egress fees |
| Liability caps | Usually 12 months of fees; your residual risk must be covered by architecture or insurance |
| Changes to services | Deprecation notice period (e.g. 12 months for GA features) |

## Regulated sectors
Financial services outsourcing rules (EBA guidelines, DORA Art. 30) mandate contract clauses:
audit and access rights, sub-outsourcing conditions, exit strategies, incident reporting.
Use the provider's financial services addendum.

## Procedure
1. Get the exact document set and versions in force.
2. Extract technical obligations into a register (owner, design impact).
3. Feed gaps to legal/procurement with a concrete ask.
4. Re-review at renewal and when a new service is adopted (service terms differ per service).

## Verify
- [ ] Register of clauses with design implications, signed off by legal.
- [ ] Exit plan references the post-termination data retrieval window.
