---
id: computing-software.qa-testing-engineering.test-case-design.shift-left-testing-practices
name: shift-left-testing-practices
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [shift-left-testing, shift-left, static-testing, atdd, early-testing, ctfl]
level: practitioner
status: draft
description: "Apply shift-left testing: tester involvement in refinement, reviews of requirements and designs, ATDD/TDD, static analysis and fast pipeline checks before merge."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.istqb.org/certifications/certified-tester-foundation-level
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Shift-left testing practices

**Goal:** find defects as early as possible, when they are cheapest to fix (ISTQB CTFL 2.1.5: early testing saves time and money).

## Practices by stage
- **Idea/refinement:** testers in backlog refinement and three amigos sessions; example mapping turns rules into examples; testability and acceptance criteria review before a story is "ready".
- **Design:** review architecture and API designs for testability (observability, seams, test data needs); agree contracts early (OpenAPI first, consumer-driven contracts).
- **Coding:** TDD for logic; ATDD/BDD acceptance tests written before or with the code; developer-run unit and component tests.
- **Pre-merge:** static analysis, linters, SAST, dependency scanning, unit and contract tests in the PR pipeline in under 10 minutes; code review including tests.
- **Environments:** ephemeral preview environments per PR so testers explore before merge.
- **Non-functional early:** performance budgets and accessibility linting in CI rather than a late test phase.

## Making it real
- Definition of Ready includes testable acceptance criteria; Definition of Done includes automated tests.
- Track where defects are found (phase containment): more found in review and PR stages, fewer in system test and production.
- Shift-left does not remove later testing; it changes its focus to integration, exploration and risk.

## Pitfalls
"Shift-left" used to mean "developers do all the testing" without skills or time; testers' role becomes coaching and test design, not disappearing.

## Verify
Defect phase-containment data shows a rising share found before merge, and every story has acceptance criteria reviewed before development starts.
