---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.intent-based-capacity-planning
name: intent-based-capacity-planning
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [intent-based-capacity-planning, auxon, capacity-planning, resource-allocation, linear-programming, sre]
level: advanced
status: docs-checked
description: "Express capacity needs as intent (dependencies, performance metrics, prioritised constraints) instead of machine counts, and solve for an allocation as Google's Auxon did."
sources: ["https://sre.google/sre-book/software-engineering-in-sre/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Intent-based capacity planning

From the SRE Book chapter "Software Engineering in SRE" (Auxon case study): specify *requirements*, not
*implementation*. Machine counts per cluster are an implementation; "N + 2 per continent" is intent. A solver
produces the allocation and re-solves when inputs change.

## Levels of abstraction (from the book)
1. "I want 50 cores in clusters X, Y and Z for service Foo." (explicit resource request)
2. "I want a 50-core footprint in any 3 clusters in geographic region YYY." (more freedom)
3. "I want to meet service Foo's demand in each geographic region, and have N + 2 redundancy." (intent)
4. "I want to run service Foo at 5 nines of reliability." (more abstract still)

The book says all levels should be supported together; in Google's experience services get the best wins as they
cross to step 3, and particularly sophisticated services may aim for step 4.

## Inputs to collect (the book's "precursors to intent")
- **Dependencies**: nested production dependencies decide where a service can be placed. The book's example:
  Foo requires its storage service Bar within 30 ms of network latency.
- **Performance metrics**: the glue between dependencies; they convert demand for one service into resource
  demand on lower-level ones (how many compute resources serve N queries, how many Mbps for Bar per N queries of Foo).
  Deriving them can involve load testing and resource usage monitoring (see `capacity-load-testing-and-benchmarks`).
- **Prioritisation**: which requirements are sacrificed when capacity is insufficient (e.g. N + 2 for Foo over
  N + 1 for Bar). Intent-driven planning makes these trade-offs transparent and consistent.

## Solving
Auxon collects intent-based descriptions through a configuration language or a programmatic API (for example
"My service must be N + 2 per continent" or "The frontend servers must be no more than 50 ms away from the
backend servers"), represents the requirements internally as a mixed-integer or linear program, solves it, and
uses the bin-packing solution to form an allocation plan. Requirements can be prioritised. You can build a small
version with any integer-programming solver: variables are instances per zone, the objective is cost, and each
redundancy requirement is a constraint such as "demand is still met with any k zones removed".

## Gotchas
- Garbage in: per-instance capacity must come from recent load tests, not vendor specs.
- Make the solver output a *plan* reviewed by humans, then applied via IaC; do not auto-apply blindly.
- Encode intent in version control so changes are reviewable and diffable.

## Verify
- [ ] Intent document lists constraints in priority order.
- [ ] Solver output survives a simulated zone loss with demand met.

## Checked

2026-11-01. Confirmed against the SRE Book chapter Software Engineering in SRE, sections Intent-Based Capacity
Planning, Precursors to Intent and Introduction to Auxon (the four levels, step 3 and step 4 guidance, the 30 ms and
50 ms examples, N + 2 per continent, the mixed-integer or linear program). Removed: the PuLP and HiGHS code with its
version and cost claims (not checkable from documentation), the invented p99 and zone-share examples, and the
unread research.google/pubs citation.
Method: documentation only; no commands were run.
