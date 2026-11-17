---
id: computing-software.qa-testing-engineering.test-automation.choosing-what-to-automate
name: choosing-what-to-automate
category: computing-software
field: qa-testing-engineering
product: test-automation
tags: [automation-candidates, test-automation-strategy, automation-roi, test-automation, manual-vs-automated]
level: practitioner
status: draft
description: "Decide which tests to automate: frequency, stability, risk, determinism and cost, at which level, and what to keep manual, with a simple ROI calculation."
sources:
  - https://www.istqb.org/certifications/certified-tester-advanced-level-test-automation-engineering-ctal-tae
  - https://martinfowler.com/articles/practical-test-pyramid.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing what to automate

**Goal:** automate where it pays back; keep humans for what humans do better. CTAL-TAE (automation scope).

## Good candidates
- Run often (every commit/release): regression of stable features, smoke.
- Deterministic expected results; stable interface.
- Tedious or error-prone by hand: many data combinations, calculations, large data comparisons.
- High-risk paths needing fast feedback.
- Hard to do manually: load, concurrency, API contracts, long soak.

## Poor candidates
- Features still changing weekly (automate once stable, or at API level only).
- One-off checks, usability and visual judgement (aesthetics), exploratory investigation.
- Things needing physical interaction (hardware, real payments) unless simulated.

## Choose the level
Automate at the **lowest level that can detect the defect**: unit > API/service > component UI > E2E. Same rule in many cases is 100x cheaper to run at unit level.

## Simple ROI
```
Manual cost per run: M (hours)     Runs per year: N
Automation build cost: B           Maintenance per year: K
Payback when  M*N > B + K
```
Example: M = 3h, N = 50, B = 40h, K = 20h -> 150 > 60: automate. Add the value of faster feedback (bugs found minutes after commit), which this ignores.

## Gotchas
- 100% automation as a goal produces brittle E2E suites and kills exploratory testing.
- Automating a bad manual test case automates its weaknesses.

## Verify
For the backlog of candidates, a scored list (frequency, risk, stability, cost) with the chosen level for each.
