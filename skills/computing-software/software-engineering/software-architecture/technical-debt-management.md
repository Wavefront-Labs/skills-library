---
id: computing-software.software-engineering.software-architecture.technical-debt-management
name: technical-debt-management
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, architecture-evaluation, technical-debt, debt-register, code-health, refactoring-budget, hotspots]
level: practitioner
status: draft
description: "Identify, record, prioritise and pay down technical debt: debt quadrant, hotspot analysis with git history, a debt register with interest estimates, and budgeting."
sources:
  - https://martinfowler.com/bliki/TechnicalDebtQuadrant.html
  - https://codescene.com/blog/prioritize-technical-debt-by-impact
  - https://www.sei.cmu.edu/library/managing-technical-debt-reducing-friction-in-software-development/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Technical debt identification and management

Technical debt: design or implementation shortcuts that make future change slower or riskier. The "interest" is the extra effort every change in that area costs.

## Classify (Fowler's quadrant)
| | Reckless | Prudent |
|---|---|---|
| Deliberate | "We don't have time for design" | "Ship now, deal with consequences" (planned) |
| Inadvertent | "What's layering?" | "Now we know how we should have done it" |
Deliberate-prudent debt is a legitimate business decision if it is recorded and repaid.

## Find it
- **Hotspots:** code that is both complex and frequently changed. Change frequency from git:
  `git log --since=12.month --name-only --format= | sort | uniq -c | sort -rn | head -30`
  Cross with complexity (lizard, radon, SonarQube cognitive complexity, CodeScene). High churn + high complexity = highest interest.
- **Change coupling:** files that always change together across module boundaries (`code-maat`, CodeScene).
- Static analysis debt estimates (SonarQube "technical debt ratio") - useful trend, poor absolute measure.
- Team signals: "everyone avoids touching X", long lead times for small changes, recurring incidents in one area, slow/flaky test suites.
- Outdated dependencies and EOL runtimes (Renovate dashboards, `npm outdated`, endoflife.date).

## Record it: debt register
One entry per item, in the backlog or an ADR-style file:
- What and where (module, files), how it was introduced.
- **Interest:** concrete cost now (e.g. "+2 days per payments feature, 3 incidents/quarter").
- **Principal:** estimated effort to fix.
- Risk if left (security, scaling cliff, EOL date).
- Proposed remedy and owner.
Use `TODO(DEBT-123)` comments linking to the ticket rather than bare TODOs.

## Prioritise and pay
- Rank by interest x likelihood of change, not by ugliness. Debt in code nobody touches can stay.
- Pay down where the next features land ("leave it better", boy-scout rule) and with dedicated capacity (a fixed share of each sprint, often 15-20%, or periodic fix-it weeks).
- Large items: plan as projects with Mikado/strangler fig and measurable outcomes (lead time, incident count).
- Communicate in business terms: delivery speed, risk, cost - not "code quality".

## Verify
- [ ] Register reviewed each quarter; top 5 items have owners and dates.
- [ ] Hotspot trend (complexity in top-churn files) is flat or falling.
