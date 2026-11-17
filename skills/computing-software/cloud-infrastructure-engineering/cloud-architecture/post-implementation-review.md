---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.post-implementation-review
name: post-implementation-review
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, implementation-governance, post-implementation-review, pir, lessons-learned, benefits-review, architecture-compliance-review]
level: practitioner
status: draft
description: "Run a post-implementation review after go-live: compare delivered architecture to design and contract, KPIs vs baseline, operational issues, and capture reusable lessons."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap09.html", "https://pubs.opengroup.org/togaf-standard/adm/chap10.html", "https://www.axelos.com/certifications/propath/prince2-project-management"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Post-implementation review

## Timing
4-12 weeks after go-live: long enough for real usage, short enough that people remember.

## Agenda
1. **Architecture conformance**: as-built vs approved design; list deviations, check each has a
   dispensation or ADR. Update the architecture repository to as-built.
2. **Outcomes**: KPIs from the vision vs baseline and target; early signals if benefits take longer.
3. **NFRs in production**: SLOs, incidents, performance, cost vs estimate (variance and causes).
4. **Operational health**: alerts noise, runbook gaps, on-call load, backlog of tech debt created.
5. **Delivery lessons**: what helped/hindered (gates, environments, vendors).
6. **Reusable outputs**: new patterns or modules worth promoting; standards to change.

## Outputs
- PIR report with actions (owner, date).
- Updated architecture debt register.
- Change requests to standards/patterns (feeds Phase H).
- Benefits tracking schedule continuing beyond the project.

## Gotchas
- Blame-oriented reviews; use blameless language.
- Cost variance ignored because the project budget is closed.

## Verify
- [ ] Repository reflects the as-built architecture.
- [ ] Actions tracked to closure.
