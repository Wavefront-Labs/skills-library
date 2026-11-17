---
id: computing-software.qa-testing-engineering.test-case-design.test-types-functional-nonfunctional-black-white-box
name: test-types-functional-nonfunctional-black-white-box
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [test-types, functional-testing, non-functional-testing, black-box-testing, white-box-testing]
level: practitioner
status: docs-checked
description: "Distinguish and plan the four test types (functional, non-functional, black-box, white-box) across test levels, and avoid gaps between them."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://glossary.istqb.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Test types: functional, non-functional, black-box, white-box

**Goal:** cover *what* the system does, *how well*, and from both spec and structure perspectives. Test types apply at every test level.

## The four types
| Type | Question | Basis | Examples |
|---|---|---|---|
| Functional | does it do what it should? | requirements, user stories, use cases | business rules, calculations, workflows |
| Non-functional | how well does it do it? | quality characteristics | performance, security, usability, reliability, compatibility, maintainability, portability |
| Black-box | behaviour vs spec, ignoring internals | specifications | EP, BVA, decision tables, state transition |
| White-box | is the internal structure exercised? | code, architecture, data flow | statement, branch, MC/DC, API call coverage |

Confirmation and regression testing are change-related and also apply at every level.

## Planning matrix
Build a level x type grid in the test plan and mark what runs where:
| | Functional | Non-functional | White-box |
|---|---|---|---|
| Component | unit tests | micro-benchmarks, static maintainability | branch coverage |
| Integration | API/contract tests | timeouts, retries | interface call coverage |
| System | E2E journeys | load, security scans, a11y | - |
| Acceptance | UAT scenarios | OAT (backup, failover), usability | - |

## Gotchas
- Non-functional testing started late is the classic schedule killer; plan perf and security from the first sprint.
- Black-box and white-box are complementary: code coverage reveals untested code, spec techniques reveal missing code.
- Non-functional requirements are often implicit; elicit measurable targets (p95 < 300 ms) or you cannot test them.

## Verify
The plan's grid has no empty row for a high-risk quality characteristic, and each cell names an owner.

## Checked

2026-10-28. Confirmed: Nothing source-specific remains; the four-type framing is general practice. Removed: Syllabus section number, the "ISTQB" attribution of the four types, and the ISO 25010 references (source unreadable).

Method: documentation only; no commands were run.
