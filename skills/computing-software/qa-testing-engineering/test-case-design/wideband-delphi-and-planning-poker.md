---
id: computing-software.qa-testing-engineering.test-case-design.wideband-delphi-and-planning-poker
name: wideband-delphi-and-planning-poker
category: computing-software
field: qa-testing-engineering
product: test-case-design
tags: [test-estimation, wideband-delphi, planning-poker, expert-based-estimation, istqb, expert-estimation]
level: practitioner
status: docs-checked
description: "Estimate test effort with expert-based techniques: Wideband Delphi rounds and planning poker, including how to run them and reach convergence."
sources:
  - https://www.istqb.org/certifications/certified-tester-foundation-level
  - https://www.mountaingoatsoftware.com/agile/planning-poker
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Wideband Delphi and planning poker

**Goal:** credible test estimates from collective expertise.

## Wideband Delphi
1. Facilitator shares scope (features, risks, test approach) and assumptions.
2. Each expert estimates independently (hours or days per work item: analysis, design, automation, execution, retest, reporting).
3. Facilitator collects and shares anonymised results with ranges.
4. Experts with outliers explain reasoning (often reveals missing assumptions).
5. Repeat rounds until estimates converge.
6. Record final estimate, range and assumptions.

## Planning poker (agile)
- Whole team estimates stories in points (Fibonacci 1, 2, 3, 5, 8, 13, 20...) including testing effort.
- Everyone reveals cards at once; highest and lowest explain; re-vote.
- Testers' role: surface test complexity (data setup, environments, combinations, non-functional tests) so it is in the number.

## Gotchas
- Anchoring: a senior voice saying a number first biases everyone; reveal simultaneously.
- Estimating testing separately after dev estimates makes testing look like overhead; estimate the story as a whole.

## Verify
Track estimate vs actual for a few releases; adjust with the ratio (see `ratio-and-extrapolation-estimation`).

## Checked

2026-10-28. Confirmed: Mountain Goat planning-poker page: typical deck 0, 1, 2, 3, 5, 8, 13, 20, 40, 100; private choice then simultaneous reveal; differing estimates are discussed. Removed: Syllabus section number, the "within 20% or 3 rounds" convergence rule; fixed a broken cross-reference.

Method: documentation only; no commands were run.
