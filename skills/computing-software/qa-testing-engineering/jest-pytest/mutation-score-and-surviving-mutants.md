---
id: computing-software.qa-testing-engineering.jest-pytest.mutation-score-and-surviving-mutants
name: mutation-score-and-surviving-mutants
category: computing-software
field: qa-testing-engineering
product: jest-pytest
tags: [mutation-score, surviving-mutants, equivalent-mutants, mutation-testing, test-effectiveness]
level: practitioner
status: verified
description: "Interpret mutation testing results: mutation score, killed vs survived vs no-coverage vs timeout, equivalent mutants, triaging survivors into tests, and setting thresholds."
sources:
  - https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/
  - https://pitest.org/quickstart/basic_concepts/
  - https://mutmut.readthedocs.io/en/latest/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interpreting mutation score and surviving mutants

## Mutant states (Stryker terminology; PIT and mutmut are similar)
| State | Meaning |
|---|---|
| Killed | at least one test failed: good |
| Survived | tests passed with the mutation: missing or weak assertion |
| No coverage | no test executes the code: coverage gap |
| Timeout | mutation caused an infinite loop/hang; counted as detected |
| Runtime/compile error | invalid mutant; excluded from score |
| Ignored | excluded by config |

**Mutation score** = detected (killed + timeout) / valid mutants. "Covered score" excludes no-coverage mutants and tells you how good your assertions are where you do test.

## Triage a survivor
Example: `if (qty > 10)` mutated to `if (qty >= 10)` survives (reproduced with StrykerJS: reported as `[Survived] EqualityOperator`, score 66.67 total / 75.00 covered, then 100 after adding a `qty = 10` test).
1. Is it **equivalent** (no observable behaviour change)? e.g. mutating a log message or a cache size hint. Mark ignored with a reason.
2. Otherwise it's a missing boundary test: add a case with `qty = 10` asserting the expected result.
3. Survivors on `return x` -> `return null` usually mean the return value is never asserted.
Group survivors by file; files with many survivors are where tests assert little.

## Thresholds
Stryker: `"thresholds": { "high": 80, "low": 60, "break": 50 }` (defaults are 80, 60 and `null`; `break` fails the build below that score; verified by a StrykerJS 9 run). PIT: `<mutationThreshold>70</mutationThreshold>`, `<coverageThreshold>` (names confirmed in the PIT Maven docs; PIT itself was not run, no JDK).
Start with break at the current score, ratchet upward; don't demand 100%.

## Keeping it affordable
- Incremental modes: Stryker `--incremental` (writes `reports/stryker-incremental.json`), PIT `withHistory`, mutmut remembers finished work. mutmut 3 needs fork support and refuses to run natively on Windows (use WSL).
- Run on changed files in PRs (`--mutate` globs from `git diff`), full runs nightly.

## Gotchas
- High line coverage with low mutation score = tests that execute code without checking results.
- Flaky tests make mutants look killed; stabilise the suite first.

## Verify
After adding tests for top survivors, re-run: those mutants are killed and the score rises.
