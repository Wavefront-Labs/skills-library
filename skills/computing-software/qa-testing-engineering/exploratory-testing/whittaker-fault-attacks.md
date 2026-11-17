---
id: computing-software.qa-testing-engineering.exploratory-testing.whittaker-fault-attacks
name: whittaker-fault-attacks
category: computing-software
field: qa-testing-engineering
product: exploratory-testing
tags: [fault-attacks, software-attacks, exploratory-testing, experience-based-testing, error-guessing, input-attacks]
level: practitioner
status: draft
description: "Run Whittaker-style software attacks: target inputs, outputs, stored data and computation with deliberate attack patterns that force error handling and boundary failures."
sources:
  - https://www.istqb.org/certifications/test-analyst
  - https://www.oreilly.com/library/view/how-to-break/9780201796193/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fault attacks (Whittaker attack patterns)

**Goal:** find defects fast by attacking the places software typically fails, instead of confirming happy paths. Source: James Whittaker, *How to Break Software*; ISTQB CTAL-TA experience-based techniques.

## The attack catalogue (pick per feature)
**Input attacks**
- Force every error message to appear (invalid, empty, too long, wrong type). Check each message is correct and the system recovers.
- Force defaults: clear fields, submit untouched forms, remove optional params.
- Explore allowable character sets: unicode, emoji, RTL text, `'";<>&%00`, leading/trailing spaces.
- Overflow input buffers: 10x the max length, 1 MB paste.
- Find inputs that interact: combine values that are individually valid but jointly invalid (start date after end date).
- Repeat the same input many times (double submit, 50x click).

**Output attacks**
- Force different outputs for one input (refresh, back, cached vs fresh).
- Force invalid outputs (negative totals, NaN, dates in 1900).
- Force properties of an output to change (resize, rename, change currency mid-flow).
- Force screen refresh (resize window, rotate device, zoom 400%).

**Stored data attacks**
- Apply inputs with different initial conditions (empty DB, 10k records, corrupted record).
- Force a data structure over/under its limits (0 items, max items + 1).
- Modify data via a side door (DB, API, second tab) and see if the UI notices.

**Computation attacks**
- Operands that cause overflow/rounding (max int, 0.1+0.2, divide by zero).
- Feature interaction: run two features on the same data at once.

**File system / environment attacks**
- Full disk, read-only file, locked file, missing permissions, network drop mid-save.

## How to run
1. Pick a feature; list its inputs, outputs, stored data and computations.
2. Choose 3-6 attacks most likely to hurt this feature; timebox 60-90 minutes.
3. Record each attack, the data used, and what happened; raise defects with exact data.
4. Feed hits back into a defect taxonomy / checklist so the attack becomes regression.

## Gotchas
- Attacks without an oracle are noise; know what "correct failure" looks like (clear error, no data loss, no 500).
- Do not attack production or systems you do not own.

## Verify
Every attack used is logged with input and outcome, and each defect has a reproducible data set.
