---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.launch-failure-mode-analysis
name: launch-failure-mode-analysis
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [launch-failure-modes-review, failure-mode-analysis, fmea, production-readiness-review, launch-planning]
level: advanced
status: docs-checked
description: "Analyse failure modes before launch: walk each component and dependency, ask what fails and how users notice, rank the risks, and fix or accept each one."
sources: ["https://sre.google/sre-book/reliable-product-launches/", "https://sre.google/sre-book/launch-checklist/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Failure mode analysis before launch

SRE Book "Reliable Product Launches", section "Failure Modes": examine each component and dependency and identify the
impact of its failure. The book's questions: can the service deal with individual machine failures, datacenter outages
and network failures? How does it deal with bad input data? Is it prepared for a denial-of-service attack? Can it keep
serving in degraded mode if a dependency fails? How does it handle a dependency being unavailable at startup, and during
runtime? Example checklist questions: do you have any single points of failure; how do you mitigate unavailability of
your dependencies? Example action items: implement request deadlines so long-running requests do not exhaust resources,
and implement load shedding to reject new requests early under overload.

## Method (an FMEA-style walk; the ranking is a common technique, not from the book)
1. Draw the request and data flow; list every component, dependency and piece of shared infrastructure (the book's
   architecture review also identifies owners of shared infrastructure as launch stakeholders).
2. For each, ask: what if it is down, slow, returning errors, returning wrong data, overloaded, misconfigured, or lost
   with a whole zone or region?
3. Record effect on users, how it would be detected, and the current mitigation.
4. Rank by severity, likelihood and detectability using a scale your team agrees on. The numbers order the work; they are
   not a measured risk.
5. Fix or explicitly accept the highest-ranked items before launch.

## Table
| Component | Failure | User effect | Detection | Mitigation | Rank | Action |
|---|---|---|---|---|---|---|
| `<dependency>` | slow | `<effect>` | `<alert>` | `<timeout, cache>` | `<n>` | `<fix or accept>` |
| `<soft dependency>` | down | `<effect>` | `<none?>` | `<fallback?>` | `<n>` | `<action>` |

## Typical findings
- Soft dependencies that are actually hard (no timeout, blocking call).
- No detection for wrong-data failures.
- Config systems that push globally at once.
- Missing degraded modes (see `degraded-mode-design`).

## Gotchas
- Do not argue over a point of rank; use it for ordering.
- Include people and process failures (only one person can deploy; a secret held by one person).
- The book warns checklists grow without limit; curate the questions that matter for your launch.

## Verify
- [ ] Table covers every dependency in the architecture diagram.
- [ ] Top-ranked items fixed or explicitly accepted before launch.

## Checked
2026-11-01. Confirmed against the SRE Book chapter "Reliable Product Launches" (Failure Modes and Architecture and
Dependencies sections, example questions and action items, checklist curation warning) and Appendix E (launch checklist
exists as the abridged original). Removed: the 60-90 minute session length, the 1-5 scoring bands and the sample table rows with timeout,
latency and failover figures.
Method: documentation only; no commands were run.
