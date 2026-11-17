---
id: computing-software.qa-testing-engineering.test-case-design.basis-path-testing
name: basis-path-testing
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [basis-path-testing, white-box-testing, cyclomatic-complexity, independent-paths, control-flow-graph, istqb-tta]
level: practitioner
status: verified
description: "Apply basis path testing: draw the control flow graph, compute cyclomatic complexity, select a set of linearly independent paths and derive inputs for each."
sources:
  - https://istqb.org/certifications/certified-tester-advanced-level-technical-test-analyst-ctal-tta/
  - https://www.mccabe.com/pdf/mccabe-nist235r.pdf
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Basis path testing

**Goal:** a test set exercising a basis of independent paths through a function: at least V(G) tests. McCabe & Watson, NIST SP 500-235 (chapter 6, the baseline method). For ISTQB syllabus section references, confirm them in the current CTAL-TTA syllabus.

## Procedure
1. Draw the control flow graph (nodes = statement blocks, edges = control transfer).
2. Compute V(G) = edges - nodes + 2 = decisions + 1 (`cyclomatic-complexity-control-flow`).
3. Choose a **baseline path** (NIST 500-235 6.3: a representative functional path, not just an error exit; the "simplified" algorithm instead starts from the shortest path) and generate further paths by flipping one decision at a time from the baseline (McCabe's method), until you have V(G) linearly independent paths.
4. For each path, derive inputs that drive execution along it; note infeasible paths and replace them.
5. Determine expected results from the spec, not the code.

## Example
```python
def grade(score, bonus):
    if score < 0 or score > 100:   # D1 (two conditions -> count 2 if counting conditions)
        raise ValueError
    if bonus:                      # D2
        score += 5
    if score >= 50:                # D3
        return "pass"
    return "fail"
```
Counting decisions (not conditions): V(G) = 4 (radon, which counts each `or`/`and` as a decision, reports 5 for this function). Paths:
1. valid, no bonus, pass (score 70, False)
2. flip D3: valid, no bonus, fail (30, False)
3. flip D2: valid, bonus, pass (70, True)
4. flip D1: invalid (-1, False) -> ValueError
Run with coverage.py `--branch`: the four paths plus (46, True) give 100% statement and branch coverage. Add the `score > 100` side and the bonus-crosses-50 boundary (46, True) as extra tests beyond the basis.

## Value
Guarantees branch coverage and at least V(G) tests; flipping one decision at a time localises failures.

## Gotchas
- Basis paths do not cover all combinations of decisions (loops, correlated conditions); complement with data-flow and boundary tests.

## Verify
Number of tests >= V(G), each mapped to a distinct path, with branch coverage 100% for the function.
