---
id: computing-software.qa-testing-engineering.test-case-design.deriving-tests-for-branch-coverage
name: deriving-tests-for-branch-coverage
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [branch-coverage-design, branch-coverage, white-box-testing, decision-coverage, coverage-py]
level: practitioner
status: verified
description: "Derive tests systematically for 100% branch coverage: map decisions, find uncovered branch outcomes in reports, and design inputs that reach them."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://coverage.readthedocs.io/en/latest/branch.html
  - https://istanbul.js.org/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deriving tests for full branch coverage

**Goal:** design (not just measure) tests so every branch outcome executes. CTFL v4.0 section 4.3.2 (branch coverage subsumes statement coverage).

## Definitions
- A **branch** is a transfer of control between two nodes in the control flow graph: both outcomes of each `if`, each `case` of a switch, loop entered/skipped, exception handler taken.
- Branch coverage = branches exercised / total branches. 100% branch coverage implies 100% statement coverage, not vice versa.

## Procedure
1. Run the existing tests with branch coverage on:
   `pytest --cov=shop --cov-branch --cov-report=term-missing` (coverage.py reports partial branches as `12->15`, meaning the jump from line 12 to 15 never happened),
   Jest `--coverage` (Istanbul reports branch %), JaCoCo for JVM.
2. For each missed branch, read the decision and work backwards: what input values make the condition take the missing outcome? Trace through assignments that feed the condition.
3. Write the test with an explicit expected result from the spec, not from what the code does.
4. If no input can reach it, you found dead code or a defect in an earlier condition; raise it.

## Example
```python
def fee(amount, member):
    if amount <= 0:               # B1 T/F
        raise ValueError
    rate = 0.02
    if member and amount > 100:   # B2 T/F
        rate = 0.0
    return round(amount * rate, 2)
```
Tests: `fee(0, False)` (B1 T), `fee(50, False)` (B1 F, B2 F), `fee(200, True)` (B2 T). Three tests reach 100% branch coverage (checked with coverage.py `--branch`; with only `fee(0, False)` and `fee(200, True)` it reports 91% and `5->7` as the partial branch); MC/DC would add `fee(200, False)` and `fee(50, True)`.

## Hidden branches
Short-circuit operators, ternaries, `?.` optional chaining, default parameters, implicit `else` on `if` without else, `for` loops that never iterate, `try` without exceptions. Coverage tools count most of these; read their docs for what is included.

## Gotchas
- Coverage shows a branch ran, not that a test asserted its effect; pair with mutation testing.
- Generated code and defensive asserts inflate the denominator; exclude deliberately and visibly.

## Verify
Branch report at the agreed target for the module, each new test with a spec-based expected result, unreachable branches logged as findings.
