---
id: computing-software.qa-testing-engineering.test-case-design.cyclomatic-complexity-control-flow
name: cyclomatic-complexity-control-flow
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [cyclomatic-complexity, control-flow-analysis, static-analysis, mccabe, cognitive-complexity, complexity-thresholds]
level: practitioner
status: docs-checked
description: "Measure cyclomatic and cognitive complexity, set thresholds in linters, and use complexity to size branch/basis-path tests and target refactoring."
sources:
  - https://docs.astral.sh/ruff/rules/complex-structure/
  - https://eslint.org/docs/latest/rules/complexity
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cyclomatic complexity and control-flow analysis

**Goal:** quantify control-flow complexity to find risky code and size testing effort.

## Definition
Cyclomatic complexity (McCabe) counts decision points in a function's control flow; tools differ in what they count (for
example `&&`/`||` or `case` branches), so compare numbers only within one tool and configuration. See `basis-path-testing`
for turning the number into test cases.

## Measuring
- Python: Ruff rule C901 (`complex-structure`), enabled with `ruff check --select C901`; the threshold is the setting
  `lint.mccabe.max-complexity`. The Ruff page's own example assumes a threshold of 5 or less to trigger on a function
  of complexity 6.
- JavaScript/TypeScript: the ESLint `complexity` rule, "enforce a maximum cyclomatic complexity allowed in a program";
  the default threshold is 20, configurable (for example `complexity: ["error", 10]`).
- Other languages: check your linter's documentation for its complexity rule and default threshold.

## Using it
- Rank functions by complexity, change frequency (`git log`) and defect history: the top items get the deepest
  white-box testing and refactoring.
- Gate new code with a lint threshold and baseline existing violations.
- Control-flow anomalies to watch: unreachable code, loops with multiple exits, deeply nested conditionals.

## Gotchas
- A `switch` with many trivial cases inflates the metric without real risk; judge by reading.
- Splitting one complex function into many small ones lowers the metric but not necessarily the total paths; test the
  composite behaviour too.

## Verify
A complexity report runs in CI, no new functions exceed the threshold, and the most complex functions have thorough
branch coverage.

## Checked
2026-10-28. Confirmed in the Ruff `complex-structure (C901)` and ESLint `complexity` rule pages: rule names, the Ruff
setting name, the ESLint default threshold of 20. Removed as unconfirmed: the V(G) = E - N + 2 formula, radon, PMD,
Checkstyle and Sonar claims, the threshold bands (1-10, 11-20, 21-50, over 50), the CTAL-TTA section reference (the ISTQB
page returned an error), the 90% branch coverage figure. The ISTQB link was dropped from `sources`.
Method: documentation only; no commands were run.
