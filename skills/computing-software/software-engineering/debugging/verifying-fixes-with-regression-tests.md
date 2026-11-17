---
id: computing-software.software-engineering.debugging.verifying-fixes-with-regression-tests
name: verifying-fixes-with-regression-tests
category: computing-software
field: software-engineering
product: debugging
tags: [debugging, regression-test, test-first-bug-fix, verification, minimal-reproduction]
level: practitioner
status: verified
description: "Verify a bug fix by first writing a regression test that fails for the right reason, fixing until it passes, and checking the fix against the original reproduction and neighbours."
sources: ["https://www.debuggingbook.org/", "https://martinfowler.com/bliki/TestDrivenDevelopment.html", "https://google.github.io/eng-practices/review/reviewer/looking-for.html#tests"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Verifying fixes with regression tests

## Sequence
1. **Reproduce** the failure reliably (script, failing input, recorded request).
2. **Minimise** the reproduction (delta debugging by hand or with tools: smaller input, fewer steps).
3. **Write a test that fails** at the lowest level where the defect is visible: unit if the bad
   function is identified, integration if the bug is in wiring/SQL.
4. Check it fails **for the right reason**: the assertion message shows the wrong value you
   observed, not an import error or setup failure.
5. Fix. Test passes. Run the surrounding suite.
6. **Temporarily revert the fix** (or `git stash` it) and confirm the test fails again; then restore.
   Tests that pass with and without the fix prove nothing.
7. Re-run the original reproduction end-to-end (the user's scenario), not only the unit test.

## Writing good regression tests
- Name for the behaviour, not the ticket alone: `test_discount_not_applied_twice_on_retry`
  (mention the issue id in a comment/docstring).
- Assert the specific property that was broken, plus nearby edge cases (boundary values, empty,
  null, concurrency if relevant).
- Keep it deterministic: inject clock/random/IDs; for race bugs, use stress tests or tools
  (deterministic schedulers, loom, jcstress) rather than sleeps.
- For data-dependent bugs, add the real failing input as a fixture (anonymised).
- Property-based tests (Hypothesis, fast-check, jqwik) can generalise one bug into a class of inputs;
  Hypothesis stores failing examples in its `.hypothesis` directory (created in a run, Hypothesis on Python 3.14) and `@example(...)` pins the original (run: a pinned example executed alongside the generated cases).

## When a test isn't feasible
Environment-only bugs (specific OS, hardware, production data): document the manual verification
steps and evidence in the PR, add monitoring or an assertion that would detect recurrence.

## Review checklist
PR contains the test; test fails on the base branch (CI can check by running new tests against
base); fix is at the root cause, not the symptom.
