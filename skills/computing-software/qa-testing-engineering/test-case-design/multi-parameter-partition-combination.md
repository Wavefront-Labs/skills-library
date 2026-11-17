---
id: computing-software.qa-testing-engineering.test-case-design.multi-parameter-partition-combination
name: multi-parameter-partition-combination
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [multi-parameter-partitions, equivalence-partitioning, combinatorial-strategy, each-choice-coverage, base-choice-coverage]
level: practitioner
status: docs-checked
description: "Combine equivalence partitions across several parameters: each-choice, base-choice and pairwise strategies, and when interactions require full combinations."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-analyst-ctal-ta-v4-0
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Combining partitions across parameters

**Goal:** choose how many combinations of partitions to test, based on how parameters interact. Input space partitioning criteria.

## Strategies (weakest to strongest)
- **Each choice**: every partition of every parameter used at least once. Tests = max(partitions per parameter). Cheap, misses interactions.
- **Base choice**: pick a base (typical) value per parameter; one base test, then vary one parameter at a time through all its other partitions. Tests = 1 + sum(partitions - 1). Good when there is a clear "normal" case and you want each deviation isolated.
- **Pairwise** (2-way): every pair of partitions across any two parameters appears at least once. Catches most interaction defects for far fewer tests than full (`pict-pairwise-generation`).
- **All combinations**: product of partition counts. Only for small spaces or critical interactions.

## Example
Parameters: user type (3), payment (4), delivery (3). All = 36; pairwise at least 12 (the product of the two largest parameter sizes is a lower bound); base choice 1 + 2 + 3 + 2 = 8; each choice 4.

## Choosing
- Rules described as interactions ("gold members get free express delivery") -> decision table or full combination of those parameters.
- Independent parameters -> each choice or base choice.
- Unknown interactions, configuration spaces -> pairwise, raise to 3-way for high risk.

## Gotchas
- Invalid partitions should not be paired with each other (masking); test them separately with base values.
- Constraints (express delivery not available internationally) remove impossible combinations; model them.

## Verify
The chosen strategy and resulting test count are documented per feature, with reasoning about interactions.

## Checked

2026-10-28 Confirmed against: arithmetic re-derived: 3 x 4 x 3 = 36 combinations; each choice = 4; base choice = 1 + 2 + 3 + 2 = 8. Removed or generalised: the ISTQB section number, the book citation, and the 'about 12' pairwise estimate (replaced by the derivable lower bound).

Method: documentation only; no commands were run.
