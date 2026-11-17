---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.reversible-decisions
name: reversible-decisions
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-change-management, reversible-decisions, evolutionary-architecture, one-way-door, two-way-door, last-responsible-moment, option-value]
level: practitioner
status: draft
description: "Classify architecture decisions as one-way or two-way doors, delay irreversible ones to the last responsible moment, and design seams that keep options cheap to change."
sources: ["https://www.aboutamazon.com/news/company-news/2016-letter-to-shareholders", "https://www.thoughtworks.com/insights/books/building-evolutionary-architectures-second-edition", "https://martinfowler.com/articles/designDead.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Evolutionary architecture and reversible decisions

## Classify
- **Two-way door** (reversible, cheap to undo): library choice behind an interface, instance type,
  feature flag rollout. Decide fast, at team level.
- **One-way door** (irreversible or very costly): primary database engine for a large dataset,
  public API contract, data residency region, identity provider, tenancy model. Slow down,
  prototype, involve wider review.

## Techniques to make decisions reversible
1. Seams: ports/adapters, anti-corruption layers around vendors.
2. Data in open formats (Parquet, standard SQL) and exportable.
3. Versioned APIs and events so consumers can migrate gradually.
4. Infrastructure as code so environments can be recreated elsewhere.
5. Feature flags and dark launches for behavioural changes.
6. Fitness functions to detect drift from desired characteristics.

## Last responsible moment
Delay a one-way decision until the cost of not deciding exceeds the cost of deciding; meanwhile
gather data (spikes, load tests). Record the decision and what would make you revisit (ADR
"revisit when" section).

## Gotchas
- Abstracting everything "to stay portable" costs more than the switch it insures against.
- Treating reversible decisions with heavyweight governance slows teams for nothing.

## Verify
- [ ] ADRs record door type; one-way decisions had a spike or prototype.
- [ ] Seams exist around the vendors you consider most likely to change.
