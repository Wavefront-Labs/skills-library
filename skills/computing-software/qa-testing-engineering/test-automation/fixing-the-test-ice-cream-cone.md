---
id: computing-software.qa-testing-engineering.test-automation.fixing-the-test-ice-cream-cone
name: fixing-the-test-ice-cream-cone
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [ice-cream-cone, test-pyramid, test-strategy, automation-strategy, test-refactoring]
level: practitioner
status: draft
description: "Reshape an inverted test pyramid (ice-cream cone): measure the current mix, push checks down to unit and API level, retire redundant UI tests, and track the shift."
sources:
  - https://martinfowler.com/articles/practical-test-pyramid.html
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fixing an inverted pyramid (ice-cream cone)

**Goal:** turn a suite dominated by slow, flaky UI and manual tests into a fast suite where most checks run at unit/API level.

## Diagnose
- Count tests per level (unit, integration/API, UI/E2E, manual) and their runtime and flaky rate.
- Typical cone: 60% manual regression, 30% UI E2E, few unit tests; suite takes hours; failures ignored.

## Push down, test by test
For each UI test ask "what is it actually checking?"
| Checks | Move to |
|---|---|
| Calculation/validation rules | unit tests (parametrised) |
| Server response and persistence | API/integration tests |
| Component rendering/states | component tests (Playwright CT, Testing Library) |
| Integration between services | contract tests (Pact) |
| Real user journey end to end | keep a small set of UI E2E (critical journeys only) |

## Process
1. Freeze growth: new UI tests need justification in review; new features require lower-level tests.
2. Start with the flakiest and slowest UI tests; write the lower-level replacement, then delete the UI test.
3. Replace UI setup with API/DB setup in remaining E2E tests.
4. Automate manual regression cases at the lowest viable level; keep exploratory testing manual.
5. Track the mix monthly.

## Targets (guidance, not law)
Hundreds to thousands of unit tests in seconds, tens to hundreds of API tests in minutes, 10-30 E2E journeys under ~10 minutes.

## Gotchas
- Deleting UI tests without the replacement loses coverage; pair each deletion with a lower-level test in the same PR.
- Unit tests that mock everything give a "pyramid" with no confidence; keep integration tests real (Testcontainers).

## Verify
Test mix and pipeline time trend in the right direction each month, and escaped defects do not rise while UI tests are removed.
