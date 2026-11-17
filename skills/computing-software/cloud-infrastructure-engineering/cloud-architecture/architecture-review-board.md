---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.architecture-review-board
name: architecture-review-board
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, implementation-governance, togaf, architecture-review-board, architecture-board, design-review]
level: practitioner
status: draft
description: "Run an architecture review board that helps rather than blocks: remit, membership, intake triage, review criteria, decision records and SLAs."
sources: ["https://pubs.opengroup.org/togaf-standard/architecture-capability/chap03.html", "https://learn.microsoft.com/azure/well-architected/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Architecture review board operation

## Steps
1. **Remit** (TOGAF architecture board): consistency between sub-architectures, ensuring
   compliance, approving dispensations, managing principle changes. Write what it does NOT
   review: changes within a team's boundary that follow standards.
2. **Membership**: chair (lead architect), domain architects (security, data, platform),
   rotating engineering representatives, FinOps for cost-significant designs. Quorum rule.
3. **Intake triage** on a short form: does it introduce a new technology, cross team
   boundaries, handle Restricted data, exceed a cost threshold, or deviate from a
   reference architecture? If none, self-certify against the checklist; no board time.
4. **Pre-read**: one-page context, C4 container diagram, ADRs, NFRs, cost estimate, threat
   model summary - circulated 3 working days ahead.
5. **Review criteria**: principles, standards and radar, Well-Architected pillars, risks.
6. **Decisions**: approve, approve with conditions (tracked to closure), defer with
   specific asks, reject with reasons. Record in the governance log within 24 hours.
7. **SLA**: decision within two weeks of complete submission; publish throughput metrics.

## Gotchas
- Boards that review everything become bottlenecks and teams route around them.
- Conditions never followed up make approvals meaningless.

## Verify
- [ ] Governance log shows decisions and condition closure dates.
- [ ] Median time to decision tracked and within SLA.
