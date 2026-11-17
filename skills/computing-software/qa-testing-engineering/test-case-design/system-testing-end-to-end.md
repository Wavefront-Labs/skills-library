---
id: computing-software.qa-testing-engineering.test-case-design.system-testing-end-to-end
name: system-testing-end-to-end
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [system-testing, test-levels, end-to-end-testing, functional-and-non-functional, production-like-environment]
level: practitioner
status: draft
description: "Plan system testing of the whole integrated product against requirements: functional and non-functional coverage, production-like environment, and independence."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# System testing

**Goal:** evaluate the complete system's end-to-end behaviour and quality characteristics. ISTQB CTFL v4.0 2.2.1.

## Scope
- End-to-end business processes and user journeys.
- All requirements (functional and non-functional: performance, security, usability, compatibility).
- Data quality characteristics (reports, exports).
- Often done by an independent tester or team.

## Approach
1. Base tests on requirements, use cases, risk analysis and user journeys (`critical-user-journey-design`).
2. Use specification-based techniques (EP, BVA, decision tables, state transition) for rules, plus exploratory sessions.
3. Environment: production-like topology, config and data volume; third parties real or stubbed (record which).
4. Automate the stable regression subset at API level where possible, a thin UI layer on top.
5. Non-functional tests scheduled once functionality is stable enough (performance needs a feature-frozen build).

## Gotchas
- System testing on a dev-like environment misses config, scaling and integration defects.
- Treating system testing as "rerun all unit tests on the full system" duplicates effort.
- Late system testing turns into the bottleneck; start with thin slices early.

## Verify
Requirement coverage report shows all requirements with at least one system-level test executed on the release build.
