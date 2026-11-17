---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.nalsd-design-evaluation
name: nalsd-design-evaluation
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [design-evaluation, design-review-questions, nalsd, system-design, design-review, failure-domains]
level: advanced
status: docs-checked
description: "Evaluate a large-system design with NALSD's questions: possible, better, feasible, resilient, plus a review checklist for scale, failure domains, latency, cost and operability."
sources: ["https://sre.google/workbook/non-abstract-design/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Evaluating a design (NALSD)

Workbook NALSD frames each design phase with questions: Is it possible? Can we do better? Is it
feasible (within budget and real hardware)? Is it resilient? Can we do better still? Use them as a
structured review, with numbers behind every answer.

## Review checklist
**Correctness and feasibility**
- Does the design meet every requirement number (QPS, latency, storage, freshness)? Show the arithmetic.
- Does it fit real hardware, quotas and budget?

**Scalability**
- What breaks at 10x? Which component is the next bottleneck? Is growth linear in machines?
- Are there global singletons (one coordinator, one queue) on the hot path?

**Reliability**
- Failure domains: what happens on loss of a machine, rack, zone, region? Does each layer survive it?
- Data durability: replication factor and placement; backup and restore path.
- Overload: load shedding, rate limits, retry policy (see cascading-failure skills).
- Dependencies: hard vs soft; timeouts; degraded modes.

**Latency**
- Latency budget by hop: does p99 fit? Fan-out amplifying tail latency?

**Cost**
- Machine count x price, storage cost per month, network egress. Biggest line item and how to shrink it.

**Operability**
- How is it deployed, canaried, rolled back? Monitored (SLIs)? Debugged?
- What does on-call do when component X fails?

## Format of the review
| Area | Question | Answer (with numbers) | Risk (H/M/L) | Follow-up |
|---|---|---|---|---|
Run with a reviewer who did not design it. Push for concrete numbers whenever an answer is abstract
("it scales horizontally" -> "how many machines at 10x, and what is shared?").

## Gotchas
- A design that only works in the happy path is not finished; spend half the review on failures.
- Cost is a requirement; a design that meets SLOs at 5x the budget fails evaluation.

## Verify
- [ ] Every checklist area answered with numbers or explicitly marked unknown with an owner.
- [ ] High risks have a mitigation in the design or an accepted-risk note.

## Checked
2026-11-01. Confirmed against the SRE Workbook chapter "Introducing Non-Abstract Large System Design": the questions "Is it possible?", "Can we do better?", "Is it feasible?", "Is it resilient?"; evaluating each iteration by asking what happens when a component fails, and checking the design against each requirement and SLO.
Removed: the N+2 claim and the evolving-engagement-model source. The checklist items and table format are review advice, not sourced facts.
Method: documentation only; no commands were run.
