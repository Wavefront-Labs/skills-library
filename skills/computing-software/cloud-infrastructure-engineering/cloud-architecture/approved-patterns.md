---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.approved-patterns
name: approved-patterns
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, technology-architecture, approved-patterns, paved-road, golden-paths, pattern-library, reference-implementations, architecture-standards]
level: practitioner
status: draft
description: "Run a library of approved architecture patterns (paved roads): template, lifecycle states, reference implementation, review and how deviations are handled."
sources: ["https://pubs.opengroup.org/togaf-standard/architecture-content/chap05.html", "https://learn.microsoft.com/azure/architecture/browse/", "https://netflixtechblog.com/how-we-build-code-at-netflix-c5d9bd727f15"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Approved patterns and paved roads

## Pattern entry template
- Name, problem/context, forces and when not to use.
- Solution diagram and components (with approved products/services).
- Non-functional properties: availability, RTO/RPO, security controls, cost range.
- **Reference implementation**: IaC modules + app template that deploy it.
- Operational guidance: monitoring, runbooks, scaling.
- Lifecycle: proposed / approved / contained (no new use) / retired, with dates.
- Owner and review date.

## Process
1. Harvest patterns from successful production systems, not from slides.
2. Review at the design authority; approve with evidence (load test, security review).
3. Publish in the portal/repository, searchable by problem.
4. Teams using an approved pattern get fast-track review; deviations go through the normal
   review with an ADR.
5. Review annually; contain/retire patterns when technology moves on.

## Gotchas
- Patterns without reference implementations get reinvented differently by each team.
- Too many approved variants; the point is a small number of well-supported roads.
- Retired patterns still deployed by templates; update the templates.

## Verify
- [ ] Each approved pattern has a deployable reference implementation.
- [ ] Usage report: number of workloads per pattern.
