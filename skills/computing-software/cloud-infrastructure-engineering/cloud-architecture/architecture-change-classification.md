---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.architecture-change-classification
name: architecture-change-classification
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-change-management, architecture-change-classification, togaf-phase-h, change-request, simplification-change, re-architecting-change]
level: practitioner
status: draft
description: "Classify architecture change requests per TOGAF Phase H (simplification, incremental, re-architecting) and route each to the right process: maintenance, partial or full ADM cycle."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap10.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Classifying architecture change

## TOGAF Phase H classes
| Class | Typical example | Handling |
|---|---|---|
| Simplification | Retire duplicate service, consolidate accounts | Change management process; update repository |
| Incremental | Add a new region, new integration, new managed service in an approved pattern | Partial re-architecting; targeted ADM iteration or design review |
| Re-architecting | Move from monolith to event-driven, change cloud provider, new operating model | New ADM cycle with Request for Architecture Work |

TOGAF's rule of thumb: if the change affects two or more stakeholders' concerns significantly,
it likely needs architecture redesign; if it affects one, change management may suffice.

## Steps
1. Intake: change request with driver (technology change, business change, lessons learned,
   regulatory), scope, affected building blocks.
2. Impact assessment against the repository: affected principles, standards, contracts, KPIs.
3. Classify and route; record decision and rationale in the governance log.
4. For re-architecting, raise a Request for Architecture Work; for incremental, schedule a review.
5. Update roadmaps and dependent work packages.

## Sources of change to monitor
Provider deprecations, new services that obsolete a pattern, cost/price changes, incidents and
post-incident actions, new regulations, mergers and acquisitions.

## Verify
- [ ] Every change request classified with rationale.
- [ ] Repository updated after each implemented change.
