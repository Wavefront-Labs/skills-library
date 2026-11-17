---
id: computing-software.qa-testing-engineering.test-case-design.definition-of-ready-for-testing
name: definition-of-ready-for-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [definition-of-ready, entry-criteria, story-readiness, refinement, istqb]
level: practitioner
status: docs-checked
description: "Define entry criteria and a definition of ready: what a story, build or environment must satisfy before testing starts, and how to enforce it without bureaucracy."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.scrum.org/resources/blog/walking-through-definition-ready
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Definition of ready and entry criteria

**Goal:** testing starts when it can be effective, not when the calendar says so.

## Story-level definition of ready
- Acceptance criteria written and agreed (testable, with boundaries and negatives).
- Examples for non-trivial rules (example mapping done).
- Dependencies identified (APIs, designs, test data, third-party sandboxes).
- Non-functional expectations stated where relevant.
- Sized small enough to build and test within the sprint.

## Phase-level entry criteria (e.g. system test)
- Build deployed to test env, version recorded; smoke suite passes.
- Unit/integration tests green in CI; static analysis gate passed.
- Test environment and data available; third-party stubs or sandboxes reachable.
- Test basis baselined; known open critical defects from earlier phases below agreed number.
- Testers and tools available.

## Enforcement
- Put story DoR as a checklist in the ticket template; refinement checks it.
- Phase entry: automated where possible (pipeline gates), a short sign-off for the rest.
- When criteria are not met: either start with a documented risk (and scope down) or wait. Record the decision.

## Gotchas
- DoR used as a weapon to refuse work creates friction; treat it as a conversation trigger.
- Entry criteria that are never measured are wishes; make each one checkable.

## Verify
Count stories that bounced back in-sprint for missing information; it should fall after introducing DoR.

## Checked

2026-10-28. Confirmed: Process advice only; the Scrum.org source is blocked (403) and nothing source-specific is claimed. Removed: Syllabus section number.

Method: documentation only; no commands were run.
