---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.design-review-gates
name: design-review-gates
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, implementation-governance, design-review-gates, architecture-checkpoints, lightweight-governance, adr-review, delivery-lifecycle]
level: practitioner
status: draft
description: "Place proportionate architecture review gates in delivery (concept, design, pre-production) with entry criteria, risk-based depth and decision SLAs, without blocking agile teams."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap09.html", "https://pubs.opengroup.org/togaf-standard/architecture-content/", "https://learn.microsoft.com/azure/well-architected/review-your-workload"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Design review gates in the delivery lifecycle

## Gates
| Gate | When | Asks |
|---|---|---|
| Concept | Before funding | Fits strategy/principles? Reuse possible? Major risks? |
| Design | Before significant build | NFRs, patterns, data, security, cost estimate, ADRs |
| Pre-production | Before go-live | Operational readiness, security tests, DR test, cost tags |

## Proportionality
Tier projects by risk (data sensitivity, criticality, novelty, spend):
- Low: self-assessment checklist + ADRs in repo, no meeting.
- Medium: async review by a domain architect within 5 working days.
- High: design authority session with security and operations.

## Entry criteria (design gate example)
Context and container diagrams, NFRs with targets, ADRs for key decisions, threat model, cost
estimate, deviations from approved patterns listed.

## Steps
1. Publish the gate criteria and checklist.
2. Automate evidence where possible (policy scans, Well-Architected tool results).
3. Record outcome: approved / approved with conditions / rework; conditions tracked as tickets.
4. Measure lead time; aim for days not weeks.

## Gotchas
- Gates at the end only (pre-production) find problems when they are expensive.
- Reviewing documents nobody will maintain; prefer living ADRs and diagrams-as-code.

## Verify
- [ ] Conditions from reviews closed before go-live.
- [ ] Median review lead time reported.
