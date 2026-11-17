---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.reference-architecture
name: reference-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, technology-architecture, togaf, reference-architecture, architecture-patterns, golden-path]
level: practitioner
status: draft
description: "Write a reusable cloud reference architecture: problem context, diagram, component choices with rationale, NFRs met, IaC module, and variation points."
sources: ["https://learn.microsoft.com/azure/architecture/browse/", "https://aws.amazon.com/architecture/reference-architecture-diagrams/", "https://pubs.opengroup.org/togaf-standard/architecture-content/chap05.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Writing a reference architecture

A reference architecture is a proven, reusable solution for a recurring problem (internal
web app, event-driven data pipeline, batch analytics) that teams adopt rather than reinvent.

## Structure
1. **Context**: problem solved, when to use and when not to.
2. **Diagram**: C4 container level with network boundaries, identity flows and data stores.
3. **Components and rationale**: chosen service per role and why (link ADRs); alternatives rejected.
4. **Quality attributes met**: availability target, RTO/RPO, scaling limits, security
   controls, typical monthly cost at small/medium/large sizes.
5. **Operations**: monitoring, alerts, runbooks, backup, patching responsibility.
6. **Implementation**: IaC module or template (golden path) with sane defaults; a reference
   that is only a picture gets ignored.
7. **Variation points**: what teams may change (instance size, region) and what they may not
   (encryption, private endpoints).
8. **Owner, version and review date.**

## Steps
- Derive from 2-3 successful implementations, not from scratch.
- Test by having a team that did not write it deploy it.
- Version it; publish changes with migration notes.

## Gotchas
- Over-general references (fits everything) give no guidance.
- Unmaintained IaC modules drift from provider best practice; schedule upgrades.

## Verify
- [ ] Deployable from the module in a fresh account.
- [ ] Cost and SLO figures included and dated.
