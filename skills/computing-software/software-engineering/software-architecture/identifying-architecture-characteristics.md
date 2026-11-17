---
id: computing-software.software-engineering.software-architecture.identifying-architecture-characteristics
name: identifying-architecture-characteristics
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, architecture-evaluation, architecture-characteristics, quality-attributes, non-functional-requirements, ilities]
level: practitioner
status: draft
description: "Extract the few architecture characteristics that matter from requirements and domain concerns, separate explicit from implicit, and pick a top three to drive design."
sources: ["https://www.oreilly.com/library/view/fundamentals-of-software/9781492043447/", "https://www.iso.org/standard/78176.html", "https://www.developertoarchitect.com/resources.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Identifying architecture characteristics

Architecture characteristics ("-ilities", ISO 25010 quality characteristics) are what the
structure must support beyond features. You can't maximise all; choosing is the work.

## Sources
- **Explicit**: stated requirements ("10,000 concurrent users", "GDPR", "99.95%").
- **Implicit from the domain**: translate business concerns.
| Domain concern | Characteristics |
|---|---|
| Mergers and acquisitions | interoperability, extensibility, scalability |
| Time to market | agility, testability, deployability |
| User satisfaction | performance, availability, usability |
| Competitive advantage | agility, scalability, availability |
| Fixed budget | simplicity, feasibility, cost |
- **Implicit always**: security, maintainability, observability; included unless explicitly not.

## Process (Richards & Ford "architecture katas" approach)
1. List candidate characteristics from requirements and domain concerns.
2. Separate **architectural** characteristics (influence structure, e.g. elasticity) from ones solved
   in code or ops (e.g. a usable UI).
3. Pick the **top three** with stakeholders; the rest are "also considered". Least worst
   architecture, not best.
4. Make each measurable: operational (p99 latency, availability %, RTO/RPO), structural
   (cyclomatic complexity, coupling), process (deploy frequency, lead time).
5. Decide scope: do characteristics differ per part of the system (architecture quanta)? Payments
   need consistency; catalogue needs elasticity, suggesting separate deployables.
6. Record in an ADR and turn into fitness functions.

## Pitfalls
Generic lists of 15 ilities, characteristics without numbers, and gold-plating (designing for
elasticity no one needs).
