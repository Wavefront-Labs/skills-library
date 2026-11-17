---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.project-prioritisation
name: project-prioritisation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, opportunities-and-solutions, project-prioritisation, togaf, phase-e, portfolio-prioritisation, wsjf]
level: practitioner
status: draft
description: "Prioritise architecture work packages and projects by value, risk and dependency: scoring model, consolidated gaps, dependency sequencing and sponsor sign-off."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap08.html", "https://framework.scaledagile.com/wsjf/", "https://pubs.opengroup.org/togaf-standard/adm-techniques/chap07.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Prioritising projects by value and risk

## Steps
1. **Consolidate the gaps** from Phases B-D into work packages (TOGAF consolidated gaps,
   solutions and dependencies matrix).
2. **Score each package**: business value (revenue, cost avoided, risk reduced, compliance
   deadline), enabling value (unblocks others), effort/cost, delivery risk, time criticality.
   WSJF (cost of delay / job size) works well when estimates are rough.
3. **Dependencies first**: a package that enables many (landing zone, identity, network)
   goes early regardless of standalone value.
4. **Risk adjust**: apply confidence factors; break high-risk packages into a cheap
   learning increment first.
5. **Check capacity**: teams and budget per period; build transition architectures
   (plateaus) that each deliver value.
6. **Agree with sponsors** and record rationale; re-prioritise when scoring inputs change.

## Gotchas
- Executive pet projects skip scoring; make the scores public to keep it honest.
- Foundations scored only on direct value always lose; score enabling value explicitly.

## Verify
- [ ] Scored and dependency-sequenced list approved by sponsors.
- [ ] Each transition architecture delivers measurable value.
