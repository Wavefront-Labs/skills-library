---
id: computing-software.qa-testing-engineering.test-case-design.suspension-and-resumption-criteria
name: suspension-and-resumption-criteria
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [suspension-criteria, resumption-criteria, exit-criteria, test-control, blocked-testing, istqb]
level: practitioner
status: draft
description: "Define when to suspend testing (broken build, blocking defects, unstable environment) and what must be true to resume, to avoid wasting effort on unusable builds."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.iso.org/standard/79429.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Suspension and resumption criteria

**Goal:** stop wasting test effort on a build or environment that cannot produce useful results, and restart cleanly. ISO/IEC/IEEE 29119-3 test plan content; ISTQB CTFL v4.0 5.3 (test control).

## Typical suspension criteria
- Smoke test fails on the delivered build.
- A blocking defect prevents more than ~X% (e.g. 25%) of planned tests from running.
- Environment unavailable or unstable (more than N hours downtime per day, data corruption).
- Defect discovery rate so high (e.g. > N critical per day) that testing just documents chaos.
- Wrong build/config deployed.

## Resumption criteria
- New build with fixes for blockers, passing smoke.
- Environment restored and verified (health checks, data reset).
- Tests affected by the suspension identified for rerun.

## Procedure
1. Announce suspension with reason, evidence and impact on schedule.
2. Redirect testers: test design, automation, exploratory on stable areas, reviewing requirements.
3. On resumption, rerun smoke plus tests executed shortly before the suspension (results may be invalid).

## Gotchas
- Not suspending leads to dozens of duplicate defect reports and unreliable results.
- Suspension without clear resumption criteria drags on; define both together.

## Verify
Test plan lists measurable suspension/resumption criteria; suspension events are logged with duration.
