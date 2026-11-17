---
id: computing-software.qa-testing-engineering.test-case-design.orthogonal-defect-classification
name: orthogonal-defect-classification
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [orthogonal-defect-classification, odc, defect-classification, defect-analysis, process-improvement]
level: practitioner
status: draft
description: "Classify defects with IBM ODC attributes (activity, trigger, impact, defect type, qualifier, source, age) and read the distributions to find process gaps."
sources:
  - https://www.chillarege.com/articles/odc-concept
  - https://ieeexplore.ieee.org/document/177364
  - https://www.istqb.org/certifications/test-analyst
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Orthogonal Defect Classification (ODC)

**Goal:** turn a defect backlog into process signals by classifying each defect on independent attributes. Chillarege et al., IBM, IEEE TSE 1992.

## Attributes
**When opened (by tester)**
- *Activity*: review, unit test, function test, system test.
- *Trigger*: what surfaced it, e.g. design conformance, logic/flow, backward compatibility, concurrency, workload/stress, recovery, startup/restart, hardware config, coverage, variation, sequencing, interaction.
- *Impact*: capability, usability, performance, reliability, installability, security, integrity, etc.

**When fixed (by developer)**
- *Target*: design, code, build, documentation.
- *Defect type*: assignment/initialisation, checking, algorithm/method, function/class/object, timing/serialisation, interface, relationship.
- *Qualifier*: missing, incorrect, extraneous.
- *Source*: in-house, library, outsourced, ported.
- *Age*: base, new, rewritten, refixed.

## Reading the distributions
- Many *function/missing* defects late = requirements/design gap; strengthen reviews and acceptance criteria.
- *Checking/assignment* dominant = code-level; unit tests and static analysis help.
- System test triggers (workload, recovery) appearing in production = system test too weak in those areas.
- Trigger distribution per activity vs expected profile shows whether each test level does its job.
- *Refixed* age = fix verification/regression gaps.

## Implement lightly
- Add the attributes as required single-select fields on the bug workflow (open vs resolve transitions).
- Train with 20 example defects; check inter-rater agreement.
- Analyse quarterly with pivot tables/charts per release.

## Gotchas
- Too many choices produce random answers; keep the standard short lists.
- Classification done months later from memory is unreliable; do it at transition time.

## Verify
At least 90% of closed defects have all attributes, and the quarterly analysis produced at least one process change.
