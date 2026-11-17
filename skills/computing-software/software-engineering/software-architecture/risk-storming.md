---
id: computing-software.software-engineering.software-architecture.risk-storming
name: risk-storming
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, architecture-evaluation, risk-storming, architecture-risk, risk-assessment, workshop, c4-model]
level: practitioner
status: draft
description: "Facilitate a risk-storming workshop on an architecture diagram: individual risk identification, likelihood x impact scoring, consensus and mitigation tracking."
sources:
  - https://riskstorming.com/
  - https://www.oreilly.com/library/view/fundamentals-of-software/9781492043447/
  - https://c4model.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Risk storming

A collaborative, visual technique (Simon Brown; also in Richards and Ford, *Fundamentals of Software Architecture* ch. 20) to find architectural risks quickly with the whole team.

## Prepare
- One or more diagrams at an agreed level, usually the C4 container diagram (plus deployment for infrastructure risks), printed large or on a shared whiteboard (Miro/FigJam).
- 4-8 participants with mixed roles: developers, architect, ops/SRE, security, product.
- Sticky notes in three colours for high/medium/low risk; 60-90 minutes.
- Optional focus per session: availability, security, performance, data integrity, delivery risk.

## Steps
1. **Individual identification (10 min, silent):** each person writes risks on stickies and places them on the diagram element/arrow they concern. Silence avoids anchoring on the loudest voice.
2. **Score each risk:** likelihood (1-3) x impact (1-3) -> 1-2 low, 3-4 medium, 6-9 high. Colour the sticky.
3. **Converge:** walk the diagram; clusters of stickies show hotspots. Discuss disagreements (one person's high risk others did not see is the most valuable output). Agree a consensus score per risk.
4. **Mitigate:** for high and medium risks, brainstorm mitigations and their cost (redundancy, load test, spike, timeout and circuit breaker, contract tests, security review). Pick actions with owners.
5. **Record:** a risk register (risk, element, score, mitigation, owner, date) - arc42 section 11 or the backlog.

## Typical risks found
Single points of failure (one DB primary, one region), unknown scaling of a new technology, third-party API rate limits, synchronous call chains, missing auth between internal services, data migration complexity, team knowledge concentrated in one person.

## Tips
- Re-run after major changes or before a launch; compare scores to show risk reduction.
- Use a risk matrix per quality attribute when the focus is broad.
- Combine with a spike or proof of concept for risks whose likelihood is genuinely unknown.

## Verify
- [ ] Every high risk has an owner and a mitigation with a date.
- [ ] Follow-up session shows high-risk count reduced or accepted explicitly.
