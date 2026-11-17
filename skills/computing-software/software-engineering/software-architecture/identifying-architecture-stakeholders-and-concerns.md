---
id: computing-software.software-engineering.software-architecture.identifying-architecture-stakeholders-and-concerns
name: identifying-architecture-stakeholders-and-concerns
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, architecture-description, architecture-stakeholders, concerns, iso-42010, stakeholder-map]
level: practitioner
status: draft
description: "Identify architecture stakeholders and their concerns (ISO/IEC/IEEE 42010), map them to views, and use them to prioritise quality attributes and decisions."
sources: ["https://www.iso-architecture.org/42010/", "https://www.viewpoints-and-perspectives.info/", "https://docs.arc42.org/section-1/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Stakeholders and concerns

ISO/IEC/IEEE 42010: an architecture description identifies **stakeholders**, their **concerns**,
and the **views** that address each concern. Missed stakeholders become late requirements.

## Find them (Rozanski & Woods classes)
Acquirers (budget holders), assessors (security, compliance, audit), communicators (docs,
training), developers, maintainers, production engineers / SRE, suppliers (vendors, platform teams),
support staff, system administrators, testers, users (by persona). Plus regulators and data
protection officers for anything with personal data.

## Capture concerns
For each stakeholder: what they care about, in their words, with a measure if possible.
| Stakeholder | Concern | Measure / scenario | View |
|---|---|---|---|
| SRE | can we roll back in < 10 min | deployment rollback scenario | deployment view |
| DPO | where is personal data stored | data flow + residency | information view |
| Finance | cloud cost per tenant | cost model | deployment view |
| Mobile team | API stability | breaking-change policy | context / interface view |

## Use it
- Turn concerns into quality-attribute scenarios and a utility tree; rank with stakeholders.
- Pick views/diagrams by concern (C4 context for business sponsors, deployment for ops).
- Name decision approvers per concern in ADRs (who must sign off on data residency).
- Stakeholder map (power/interest grid) decides involvement: manage closely, keep satisfied,
  keep informed, monitor.

## Pitfalls
- Only talking to developers and the product owner. Operations, security and support concerns
  surface at go-live.
- Concerns without measures ("fast", "secure") can't drive trade-offs.
- Stakeholder list never revisited as the system enters operation.
