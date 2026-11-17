---
id: computing-software.qa-testing-engineering.test-case-design.path-coverage-and-infeasible-paths
name: path-coverage-and-infeasible-paths
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [path-coverage, infeasible-paths, white-box-testing, basis-path-testing, control-flow-graph]
level: practitioner
status: verified
description: "Understand path coverage and why full path coverage is impractical: enumerate paths, detect infeasible paths, and choose prime path or basis path subsets."
sources:
  - https://glossary.istqb.org/
  - "Ammann and Offutt, Introduction to Software Testing (book; the author's old cs.gmu.edu/~offutt/softwaretest page no longer hosts it)"
  - https://github.com/Z3Prover/z3
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Path coverage and infeasible paths

**Goal:** know what path coverage buys, how to approximate it, and how to spot paths no input can take.

## Path coverage
Every distinct entry-to-exit path through the control flow graph executed. With k sequential independent decisions there are 2^k paths; any loop makes the count unbounded. So 100% path coverage is only feasible for tiny loop-free code.

## Practical subsets
| Criterion | Idea |
|---|---|
| Basis path (McCabe) | cyclomatic complexity V(G) linearly independent paths |
| Prime path coverage (Ammann/Offutt) | tour every prime path; see the book for the exact definition and how loops are handled (not re-checked here) |
| Loop-bounded path coverage | paths with each loop executed 0, 1, and 2 times |
| Data-flow criteria (all-uses) | paths that connect definitions to uses |

## Infeasible paths
A path is infeasible when the conditions along it contradict each other:
```python
if x > 10:      # D1
    a = 1
if x < 5:       # D2
    b = 2
```
Path D1=T, D2=T is infeasible (x cannot be > 10 and < 5). Signs:
- Correlated conditions on the same variable.
- A flag set in one branch and tested later.
- Invariants guaranteed by earlier validation.

## Handling them
1. When a target path seems unreachable, write the path condition (conjunction of branch predicates with substitutions) and check satisfiability (by hand or with an SMT solver such as Z3: `x > 10 and x < 5` returned `unsat` in z3-solver; symbolic execution tools include KLEE for C and CrossHair for Python, which installs from PyPI as `crosshair-tool`).
2. Exclude proven-infeasible paths from the coverage denominator and document them.
3. Consider whether correlated conditions indicate a design smell; restructuring often removes both the infeasible path and the confusion.

## Gotchas
- Unreachable by today's callers is not infeasible; a new caller may reach it. Prefer defensive handling over deleting.
- Path explosion makes path coverage a poor CI metric; use branch/MC/DC targets and path thinking for critical functions.

## Verify
For critical functions, the selected path set is listed with infeasible paths and the contradiction proving each.
