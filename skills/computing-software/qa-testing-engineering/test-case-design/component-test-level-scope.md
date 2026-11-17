---
id: computing-software.qa-testing-engineering.test-case-design.component-test-level-scope
name: component-test-level-scope
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [unit-test-scope, component-test-level, test-levels, unit-testing, test-isolation]
level: practitioner
status: docs-checked
description: "Define the component (unit) test level: what a unit is, what is isolated vs real, objectives, test basis, typical defects, and who owns the tests."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://martinfowler.com/bliki/UnitTest.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Component (unit) test level scope

**Goal:** agree what "unit test" means in this codebase so suites are fast, focused and not duplicated at higher levels.

## Level profile (a common convention; adapt it)
| Aspect | Component testing |
|---|---|
| Objective | verify each component behaves per its detailed design; find defects in logic early |
| Test basis | detailed design, code, data model, component specs |
| Test objects | classes, modules, functions, stored procedures, UI components |
| Typical defects | wrong logic, boundary errors, unhandled nulls, incorrect data flow |
| Approach | white-box and black-box; TDD; run on every commit |
| Owner | developers |

## Deciding the unit
- **Solitary** unit tests: one class, collaborators replaced by test doubles.
- **Sociable** unit tests: a small cluster of real in-process objects, doubles only at process boundaries.
Choose per team and write it down. Either way, a unit test must not touch network, real database, filesystem outside a temp dir, or system clock without control.

## Isolation boundary checklist
Replace: HTTP clients, DB repositories, message brokers, time (inject a controllable clock), randomness (seeded), environment variables.
Keep real: value objects, pure functions, in-memory collections.

## Gotchas
- A "unit test" that needs Docker is an integration test; label and run it separately.
- Mocking everything couples tests to implementation; refactors then break tests without behaviour change.
- Duplicating a rule's every case at unit and E2E levels wastes runtime; push combinatorics down to unit level.

## Verify
Unit suite runs in seconds offline, in any order, in parallel, and its scope definition is in the test strategy or CONTRIBUTING.

## Checked

2026-10-28 Confirmed against: Martin Fowler UnitTest (solitary versus sociable units, test doubles, unit tests expected to be fast). Removed or generalised: the ISTQB section number, the Google small-test rule, and the freezegun/Jest/Clock names (not in the fetched pages).

Method: documentation only; no commands were run.
