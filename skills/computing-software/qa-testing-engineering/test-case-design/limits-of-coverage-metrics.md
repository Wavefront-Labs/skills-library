---
id: computing-software.qa-testing-engineering.test-case-design.limits-of-coverage-metrics
name: limits-of-coverage-metrics
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [coverage-misuse, code-coverage, white-box-testing, test-quality, mutation-testing]
level: practitioner
status: draft
description: "Explain what code coverage does and does not tell you, avoid coverage-target anti-patterns, and pair coverage with mutation scores and risk."
sources:
  - https://martinfowler.com/bliki/TestCoverage.html
  - https://testing.googleblog.com/2020/08/code-coverage-best-practices.html
  - https://stryker-mutator.io/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Limits of coverage metrics and target anti-patterns

**Goal:** use coverage as a tool to find untested code, not as a quality score.

## What coverage tells you
- Code that **no test executes** (useful: look at it).
- Low coverage strongly suggests weak testing. High coverage does **not** imply good testing.

## What it does not tell you
- Whether tests assert anything (assertion-free tests give 100%).
- Missing code: requirements never implemented are invisible to coverage.
- Data-dependent defects: one test runs the line; the boundary value never ran.
- Integration and timing defects.
- Correctness of expected results.

## Anti-patterns
| Anti-pattern | Effect |
|---|---|
| Hard org-wide target (e.g. 90% everywhere) | tests written to touch lines, trivial getters tested, risky code under-tested |
| Coverage in performance reviews | gaming: assertion-free tests, excluded files |
| Ratcheting on total only | new untested code hidden by old tested code |
| Excluding hard code to hit the number | risk concentrated in excluded files |
| Chasing the last 5% | low value; error handlers for impossible states |

## Better practice
- Gate on **diff/patch coverage** for changed lines (e.g. >= 80%) rather than an absolute total.
- Review uncovered lines in risky modules during code review.
- Use **mutation testing** (Stryker, PIT, mutmut) on critical modules to check that tests detect changes; surviving mutants show weak assertions.
- Set targets per risk: payment logic high branch/MC/DC, generated code excluded, UI glue lower.
- Google's guidance: 60% acceptable, 75% commendable, 90% exemplary, as rough guides, not mandates.

## Gotchas
- Coverage tools measure differently (line vs statement vs branch; Istanbul counts logical operators); compare like with like.
- Merging coverage from parallel or multiple suites needs the right combine step or numbers are wrong.

## Verify
Coverage policy is documented per risk level, gates use diff coverage, and critical modules have a mutation score reported alongside coverage.
