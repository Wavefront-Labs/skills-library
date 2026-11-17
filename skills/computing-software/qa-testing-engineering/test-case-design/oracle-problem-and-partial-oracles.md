---
id: computing-software.qa-testing-engineering.test-case-design.oracle-problem-and-partial-oracles
name: oracle-problem-and-partial-oracles
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [partial-oracles, test-oracles, oracle-problem, implicit-oracles, metamorphic-testing]
level: practitioner
status: draft
description: "Handle the oracle problem when exact expected results are unknown: implicit, consistency, statistical, metamorphic and human oracles, and combining them."
sources:
  - https://ieeexplore.ieee.org/document/6963470
  - https://glossary.istqb.org/
  - https://www.satisfice.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# The oracle problem and partial oracles

**Goal:** still find defects when nobody can say exactly what the output should be (ML models, simulations, search ranking, complex reports, scientific code).

## Partial oracles
| Oracle | Checks | Example |
|---|---|---|
| Implicit | universal failure signs | crash, exception, 5xx, timeout, memory leak, assertion in logs |
| Consistency | agreement with itself or similar | same query twice gives same result; API and UI show the same total; previous version gives same output (regression) |
| Invariant/property | rules that always hold | sorted, non-negative, sums balance |
| Metamorphic | relation between outputs of related inputs | search for "shoes red" is a subset of "shoes"; adding an irrelevant record does not change a statistic |
| Statistical | distribution properties | mean of 10,000 simulated rolls within tolerance; A/B metrics within control limits |
| Plausibility (sanity) | magnitudes and types | age 0-130, price > 0, date not in future |
| Human/heuristic | expert judgement with heuristics (HICCUPPS: history, image, comparable products, claims, user expectations, product, purpose, standards) | exploratory review of a report |

## Combining them
1. Start with implicit oracles everywhere (cheap, automatic).
2. Add invariants and plausibility checks to every automated test.
3. Use metamorphic relations for core algorithms.
4. Reserve human review for samples, rotated across areas.
5. Use differential testing against a previous version or competitor where available.

## Gotchas
- Partial oracles miss consistent-but-wrong output; one example-based test with a hand-verified result anchors the rest.
- Statistical oracles are flaky if tolerance is too tight; derive bounds from variance, fix seeds where possible.
- Document which oracles each test uses, so passing is not overinterpreted.

## Verify
For each component without a complete oracle, the test approach names the partial oracles used and at least one anchored example.
