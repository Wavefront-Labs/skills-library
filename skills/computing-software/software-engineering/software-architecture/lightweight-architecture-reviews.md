---
id: computing-software.software-engineering.software-architecture.lightweight-architecture-reviews
name: lightweight-architecture-reviews
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, architecture-evaluation, architecture-review, atam-lite, risk-review, design-review]
level: practitioner
status: draft
description: "Run lightweight architecture reviews (ATAM-lite, risk-focused): scope, prep pack, scenario walk-throughs, findings as risks and sensitivity points, and follow-up."
sources: ["https://insights.sei.cmu.edu/library/atam-method-for-architecture-evaluation/", "https://www.oreilly.com/library/view/fundamentals-of-software/9781492043447/", "https://docs.aws.amazon.com/wellarchitected/latest/framework/the-review-process.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lightweight architecture reviews

Full ATAM takes days and many people; most teams need a 2-3 hour review at key moments: before
committing to a design, before go-live, after a major incident.

## Prep (author, 1 day)
- Context diagram, container diagram, key runtime scenarios, deployment view.
- Top quality-attribute scenarios with targets (from the utility tree).
- ADRs for key decisions and open questions.
- Ask reviewers to read beforehand; pick 2-4 reviewers including someone from ops/security and
  someone outside the team.

## Session (2-3 h)
1. Author presents business drivers and architecture (20 min max).
2. Walk the top scenarios through the design: "a region fails during peak", "traffic triples",
   "a tenant asks for data deletion", "a dependency's latency goes to 5 s". Trace which components
   act and how.
3. Record findings as:
   - **Risks**: decisions that may not meet a scenario.
   - **Non-risks**: confirmed good decisions (worth stating).
   - **Sensitivity points**: parameters a quality attribute depends on (pool size, cache TTL).
   - **Trade-off points**: one decision affecting two attributes in opposite directions.
4. Prioritise risks (impact x likelihood); agree owners.

## Follow-up
Risks become backlog items or ADRs with dates; review again only the high ones. Store the review
record next to the architecture docs. Checklists like AWS Well-Architected pillars help ensure
nothing major is skipped but are not the review itself.

## Pitfalls
Turning it into a presentation without scenario walk-throughs; reviewers redesigning the system
in the room; findings without owners.
