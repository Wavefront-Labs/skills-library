---
id: computing-software.qa-testing-engineering.test-case-design.data-flow-analysis-define-use
name: data-flow-analysis-define-use
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [data-flow-analysis, define-use, static-analysis, du-pairs, dataflow-anomalies, white-box-testing, istqb-tta]
level: practitioner
status: verified
description: "Find data-flow anomalies (use before define, define-define, define without use) statically and design tests covering define-use pairs."
sources:
  - https://istqb.org/certifications/certified-tester-advanced-level-technical-test-analyst-ctal-tta/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Data flow analysis: define-use

**Goal:** detect variable-lifecycle defects and design tests around how data flows. Data-flow anomaly analysis appears in the ISTQB CTAL-TTA syllabus; confirm the section number and the exact two-letter anomaly labels (they differ between sources) in the current syllabus.

## Anomalies
- **ur (undefined then referenced; also written "uninitialised use")**: used before assignment. Example: variable assigned only in an `if` branch, used after.
- **dd (defined, defined)**: assigned twice without use in between; often a logic slip (wrong variable).
- **define without use (dead store; some sources write dk, define then kill)**: assigned and never used, maybe a missing use. Note `du` in the du-pair sense (definition then use) is the *normal* case, not an anomaly.

## Tools that flag them
- Compilers: `-Wall` includes `-Wuninitialized` in GCC (the GCC manual says which variables warn depends on the optimisation options; not run here, no C compiler), Clang `-Wuninitialized`, Java definite-assignment errors (JLS chapter 16), TypeScript `strict` (TS2454 "used before being assigned") + `noUnusedLocals` (TS6133); both TypeScript errors reproduced with tsc 5.
- Linters: ESLint `no-unused-vars`, `no-use-before-define` (flags use before a `function`/`const` declaration, not a conditionally assigned `var`); Ruff `F841` (unused local) and `F821` (undefined name, only for names that are never defined); Pylint `possibly-used-before-assignment` (E0606) for a variable assigned only in one `if` branch (`used-before-assignment`, E0601, is the definite case); SpotBugs `DLS_DEAD_LOCAL_STORE` (listed in its bug descriptions, not run). Run on a sample, none of ESLint, Ruff or Pylint flagged a define-define pair (`z = 5; z = 6`), so dd needs review or a dedicated analyser.

## Testing from data flow
1. For a variable, list each definition (assignment) and each use (computation use c-use, predicate use p-use).
2. Coverage criteria: all-defs (each def reaches some use), all-uses (each def reaches each reachable use), all-du-paths.
3. Design inputs that drive each def-use pair, especially defs in rarely taken branches.

```python
def fee(amount, vip):
    rate = 0.02                # d1
    if vip: rate = 0.01        # d2
    if amount > 1000: rate = rate / 2   # use of d1 or d2, then d3
    return amount * rate       # use of d1/d2/d3
```
All-uses needs: vip False/amount<=1000 (d1->return), vip True/amount<=1000 (d2->return), and both with amount>1000 (d1->d3, d2->d3).

## Gotchas
- Dynamic languages hide many anomalies until run time; enforce type checking (mypy/pyright, `strict`).
- Data flow through object fields and globals is poorly covered by local analysis.

## Verify
Linter run shows zero unused/undefined-variable findings, and tests exist for each def-use pair in high-risk functions.
