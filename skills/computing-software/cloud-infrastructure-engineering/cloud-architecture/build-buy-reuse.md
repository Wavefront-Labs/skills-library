---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.build-buy-reuse
name: build-buy-reuse
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, opportunities-and-solutions, build-buy-reuse, togaf-phase-e, make-or-buy, saas-vs-custom, differentiation, total-cost]
level: practitioner
status: draft
description: "Decide build vs buy vs reuse for each solution building block using differentiation, fit, TCO, time-to-value, integration and exit risk, as in TOGAF Phase E."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap06.html", "https://learn.microsoft.com/azure/cloud-adoption-framework/plan/plan-intro", "https://martinfowler.com/bliki/UtilityVsStrategicDichotomy.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Build vs buy vs reuse decision

## Options
- **Reuse**: an existing internal component or platform service.
- **Buy**: SaaS, COTS, managed cloud service, marketplace product.
- **Build**: custom code on cloud primitives.
- **Hybrid**: buy the core, build differentiating extensions via APIs.

## Criteria
| Criterion | Questions |
|---|---|
| Differentiation | Does this capability give competitive advantage? (Fowler's utility vs strategic) |
| Fit | % of requirements met out of the box; configuration vs customisation |
| TCO (5 yr) | Licences/subscription, build effort, run/ops staff, upgrades, integration |
| Time to value | Weeks to first value |
| Integration | APIs, events, SSO, data export |
| Risk | Vendor viability, lock-in, security posture, roadmap control |
| Skills | Do we have people to build and run it? |

## Procedure
1. Default bias: reuse > buy > build for utility capabilities; build for strategic ones.
2. Score options with weights agreed upfront (avoid weighting after seeing the scores).
3. Prototype the riskiest integration for buy options.
4. Record as an ADR with the revisit trigger (e.g. vendor price change, scale threshold).

## Gotchas
- Heavy customisation of COTS: you pay for both buy and build and lose upgrades.
- Underestimating build run cost (on-call, patching, security) - often larger than build cost.
- "Not invented here" disguised as requirements.

## Verify
- [ ] Each building block has a decision and 5-year TCO.
- [ ] Revisit triggers recorded.
