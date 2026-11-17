---
id: computing-software.qa-testing-engineering.test-case-design.test-case-and-automation-code-review
name: test-case-and-automation-code-review
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [test-case-review, static-testing, reviews, test-code-quality, peer-review]
level: practitioner
status: docs-checked
description: "Peer-review test cases and test automation code with a checklist: traceability, expected results, independence, assertions, flakiness risks and data."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://glossary.istqb.org/
  - https://martinfowler.com/articles/nonDeterminism.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Peer review of test cases and automation code

**Goal:** tests are work products too and contain defects; a wrong test is worse than none because it gives false confidence.

## Manual test case checklist
- Traces to a requirement / risk / condition; priority stated.
- Preconditions and test data are explicit and obtainable.
- Steps are unambiguous; one action per step.
- **Expected result is concrete** and taken from the spec (not "works correctly").
- Covers negative and boundary cases, not only the happy path.
- Independent: does not rely on another case's leftovers.
- No duplicate of an existing case.

## Automation code checklist
- Test name states behaviour and expected outcome (`test_expired_coupon_is_rejected`).
- Arrange/Act/Assert visible; one behaviour per test.
- Assertions are specific (status *and* body field), and the test would fail if the feature broke (try breaking it, or check mutation results).
- No fixed sleeps; waits on conditions.
- No hard-coded environment URLs, credentials or dates; data created by the test or builders.
- Cleans up, or runs in isolation (transaction, unique IDs) so it is parallel-safe.
- No logic in tests (loops/ifs that could hide failures); use parametrization.
- Uses page objects/helpers rather than raw selectors repeated.
- Skips/xfails have a linked ticket.

## Process
Review test code in the same PR as the production change; tester reviews developers' tests for missing cases, developer reviews testers' automation for code quality.

## Gotchas
- Reviewers check that tests pass, not that they can fail; ask "what change would make this test red?"
- Snapshot updates in a PR need the same scrutiny as code.

## Verify
PR template includes the test checklist, and sampled merged tests have specific assertions and no sleeps.

## Checked

2026-10-28 Confirmed against: Martin Fowler non-determinism article (sleeps as a common mistake with asynchrony, lack of isolation as a cause of flaky tests). Removed or generalised: nothing; the skill has no other named APIs or figures (the test name is an example).

Method: documentation only; no commands were run.
