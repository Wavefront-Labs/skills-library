---
id: computing-software.qa-testing-engineering.test-case-design.iso-25010-quality-model-mapping
name: iso-25010-quality-model-mapping
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [iso-25010, quality-characteristics, functional-suitability, non-functional-testing, quality-model, test-planning]
level: practitioner
status: gated
description: "Map tests to ISO/IEC 25010 quality characteristics to find blind spots: choose relevant sub-characteristics, define measures, and assign test types to each."
sources:
  - https://iso25000.com/index.php/en/iso-25000-standards/iso-25010
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mapping tests to ISO/IEC 25010

**Goal:** use the product quality model as a checklist so non-functional areas are chosen deliberately, not forgotten.

## Characteristics (25010:2023 product quality)
Functional suitability, performance efficiency, compatibility, interaction capability (formerly usability), reliability, security, maintainability, flexibility (formerly portability), safety. Each has sub-characteristics, e.g. reliability -> faultlessness, availability, fault tolerance, recoverability. (gated: unconfirmed, source is paywalled or blocked)

## Procedure
1. With stakeholders, rate each characteristic's importance for this product (high/medium/low/not relevant) and record why.
2. For high and medium ones, pick the sub-characteristics that matter and a **measure**: e.g. an availability target per month; p95 latency < 300 ms at 500 rps; WCAG 2.2 AA; recovery < 15 min.
3. Assign test types and owners: performance tests, security scans and pen test, accessibility audit, failover tests, compatibility matrix.
4. Put them in the test plan and the definition of done where they apply per story.

| Characteristic | Priority | Measure | Test type | Owner |
|---|---|---|---|---|
| Performance efficiency | High | p95 < 300 ms @ 500 rps | k6 load test | Perf eng |
| Interaction capability | Medium | WCAG 2.2 AA | axe + manual audit | QA |

## Gotchas
- Many teams still use 25010:2011 names (usability, portability); map both. (gated: unconfirmed, source is paywalled or blocked)
- Not relevant is a valid rating, but write the reason so it can be revisited.

## Verify
Every characteristic has a recorded rating, and every high one has a measure and a planned test.

## Checked

2026-10-28. Confirmed: Nothing; the iso25000.com page could not be fetched. Gated: the list of 25010:2023 characteristics, their renaming from 2011 and the sub-characteristics. Removed: Syllabus-linked source (error page) and the percentage example "99.9% monthly".

Method: documentation only; no commands were run.
