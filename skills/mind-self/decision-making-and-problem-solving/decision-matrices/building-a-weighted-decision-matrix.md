---
id: mind-self.decision-making-and-problem-solving.decision-matrices.building-a-weighted-decision-matrix
name: building-a-weighted-decision-matrix
category: mind-self
field: decision-making-and-problem-solving
product: decision-matrices
tags: [decision-making-and-problem-solving, decision-matrix, weighted-scoring, weighted-decision-matrix, pugh-matrix, multi-criteria-decision-analysis, mcda, criteria-selection, weighting, sensitivity-analysis, trade-off-analysis, option-comparison, spreadsheet, job-offer-comparison, buying-decision, vendor-selection, prioritisation, gut-check]
level: intro
status: draft
description: "Compare options on weighted criteria: choosing independent criteria, weighting before scoring, scoring scales, sensitivity checks, Pugh-style baseline comparison and the gut-check at the end."
sources: ["Pugh, Total Design (1991)", "Hammond, Keeney & Raiffa, Smart Choices (1999)", "Keeney, Value-Focused Thinking (1992)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building a weighted decision matrix

**Goal:** turn a messy multi-factor choice — job offers, flats, cars, suppliers, which
project to fund — into a comparable, explainable decision, and find out which factors
are really driving it.

## 1. Define the decision and options
Write one line: "Choose a flat to rent from these four by Friday." List 3–6 real options.
Include the status quo if it's an option. If you have only one option, you're not
deciding yet — look for alternatives.

## 2. Choose the criteria
- Start from what you actually care about (Keeney's "value-focused thinking"): cost,
  commute time, space, light, safety, landlord quality…
- **Keep them independent** — "rent" and "total monthly cost" double-count.
- **Make them measurable or clearly judgeable.** "Nice" is too vague; "natural light in
  the living room" is better.
- 4–8 criteria is plenty.
- Separate **must-haves** (deal-breakers) from **wants**. Eliminate any option failing a
  must-have *before* scoring.

## 3. Weight before you score
Assign weights that sum to 100 (or 1–5 importance). Do this **before** looking at how
options score — otherwise you'll unconsciously tilt weights toward your favourite.
A useful check: "Would I trade 10 extra minutes of commute for a bigger second bedroom?"
Trade-off questions reveal true weights better than gut numbers.

## 4. Score each option on each criterion
- Use a consistent scale, e.g. 1–5 or 0–10, with anchors written down ("commute: 10 =
  under 20 min, 5 = 40 min, 0 = over 60 min").
- Score across a row (one criterion, all options) rather than down a column — it keeps
  scores comparable.
- Use real data where you have it (prices, minutes, square metres).

## 5. Calculate
Weighted score = Σ (weight × score). In a spreadsheet: one row per criterion, one column
per option, `=SUMPRODUCT(weights, scores)` at the bottom.

## 6. Sensitivity check
- Change the top weight by ±20%. Does the winner change?
- Swap any score you were unsure of to its plausible alternative.
- If the ranking flips easily, options are near-equal — pick on a deciding factor, or the
  cheaper/more reversible option. If it's robust, you can be confident.

## Pugh variant (comparing designs or proposals)
Pick one option (often the current solution) as the **baseline**. Score every other option
on each criterion as **+ (better), S (same), – (worse)** than baseline. Sum the pluses and
minuses. Useful early on, when precise scores would be fake precision; also good for
spotting hybrids that combine the best features.

## 7. The gut-check
Look at the winner. If you feel disappointed, that's data: a criterion is missing or a
weight is wrong. Find it and update the matrix — don't just override the result silently.

## Gotchas
- **Fake precision:** a score of 7.3 vs 7.1 is a tie.
- **Backwards engineering:** fiddling weights until your favourite wins. Lock weights first
  and record any later change with a reason.
- **Missing criteria** (resale value, how a partner feels, exit costs) are the commonest
  source of a "wrong" answer.
- Matrices handle trade-offs; they don't handle uncertainty well. For outcomes that
  depend on chance, see
  `mind-self.decision-making-and-problem-solving.decision-trees-and-expected-value`.

## Verify
- [ ] Must-haves were applied before scoring.
- [ ] Weights were set before options were scored, and sum correctly.
- [ ] Each scale has written anchors.
- [ ] You ran a sensitivity check and know whether the winner is robust.
- [ ] The final choice survived the gut-check, or the matrix was updated to explain it.
