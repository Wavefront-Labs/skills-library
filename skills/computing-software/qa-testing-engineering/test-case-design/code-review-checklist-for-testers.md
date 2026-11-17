---
id: computing-software.qa-testing-engineering.test-case-design.code-review-checklist-for-testers
name: code-review-checklist-for-testers
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [code-review-checklist, static-testing, reviews, pull-request-review, testability, test-code-review]
level: practitioner
status: docs-checked
description: "Review pull requests as a tester: test coverage of the change, missing negative cases, error handling, logging, testability seams and test code quality."
sources:
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Code review checklist for testers

**Goal:** add a testing lens to PR review. Google eng-practices "What to look for" (its Tests section asks for unit, integration or end-to-end tests as appropriate for the change).

## Production code
- Inputs validated at trust boundaries; error paths return useful errors, not swallowed exceptions (`except: pass`, empty `catch`).
- Boundaries: off-by-one in loops and comparisons (`<` vs `<=`), empty collections, null/undefined, unicode, large inputs.
- Concurrency: shared mutable state, missing locks/transactions, retries not idempotent.
- Time: time zones, DST, `now()` called in logic (hard to test; inject a clock).
- Logging: errors logged with context and correlation id, no secrets/PII.
- Config/feature flags: default values safe; both flag states tested.
- Testability: dependencies injectable, no hidden singletons/global state.

## Tests in the PR
- New behaviour has tests at the right level; bug fix has a regression test that fails without the fix.
- Negative and boundary cases present, not just the happy path.
- Assertions are specific (not just `assert result`); no logic (loops/ifs) in tests.
- No sleeps; no order dependence; no real network calls in unit tests.
- Test names describe behaviour (`test_rejects_expired_card`).

## Gotchas
- Coverage percentage in the PR bot says nothing about assertion quality; read the asserts.
- Big PRs get rubber-stamped; ask for smaller ones.

## Verify
Your review comments are specific and actionable (file:line, case missing, suggested test).

## Checked

2026-10-28 Confirmed against: Google engineering practices, what to look for in a code review (Tests, Complexity, Naming, Design sections). Removed or generalised: the ISTQB syllabus section and its source link (page returned an error).

Method: documentation only; no commands were run.
