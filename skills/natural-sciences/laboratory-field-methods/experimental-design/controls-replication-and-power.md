---
id: natural-sciences.laboratory-field-methods.experimental-design.controls-replication-and-power
name: controls-replication-and-power
category: natural-sciences
field: laboratory-field-methods
product: experimental-design
tags: [experimental-design, controls, positive-control, negative-control, vehicle-control, replication, biological-replicate, technical-replicate, pseudoreplication, experimental-unit, randomisation, blinding, blocking, confounding, power-analysis, sample-size, effect-size, cohens-d, alpha, statistical-power, g-power, pwr, pre-registration, factorial-design, arrive-guidelines]
level: practitioner
status: verified
description: "Design a lab experiment that answers its question: identify the experimental unit, pick controls, avoid pseudoreplication, randomise and blind, and size it with a power analysis."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Controls, replication and power

**Goal:** before any sample is touched, a written design whose result — either way —
will be interpretable: the right comparison, enough independent replicates, and no
confound that could explain the effect instead of your treatment.

## 1. State the question as a comparison
One sentence: "Does treatment X change outcome Y in system Z, compared with C?"
If you cannot name C, you don't have an experiment yet. Write down the **primary
outcome** and the analysis you will run *now*, before data exist (pre-register if the
field supports it). Secondary outcomes are exploratory.

## 2. Controls
| Control | Answers |
|---|---|
| **Negative / untreated** | What happens without the intervention? |
| **Vehicle** | Is it the drug or the DMSO/saline it's dissolved in? |
| **Positive** | Could the assay have detected an effect at all? |
| **Procedural / sham** | Is it the handling (surgery, injection, transfection reagent)? |
| **Specificity** (e.g. second siRNA, rescue, knockout) | Is it on-target? |
A negative result without a working positive control is uninterpretable.

## 3. Find the experimental unit
The **experimental unit** is the smallest thing that independently received the
treatment. Its count is your *n*.
- Treat a cage of mice through their water → the cage is the unit, not each mouse.
- Treat one flask, then split into 3 wells → 1 biological replicate with 3 technical
  replicates.
- Measure 50 cells from one animal → 1 animal, not n = 50.
Treating technical replicates or sub-samples as independent is **pseudoreplication**; it
shrinks error bars and inflates false positives. Average technical replicates, or model
the nesting (mixed-effects model).
For cell lines, independent replicates are usually separate experiments on different
days/passages with fresh reagents.

## 4. Randomise, block, blind
- **Randomise** allocation to treatment with a generator (R `sample()`, a spreadsheet
  `RAND()` sort), not "first five out of the cage".
- **Block** on known nuisance variables (day, plate, litter, batch): put every treatment in
  every block and include block in the analysis. Never run all controls on Monday and
  all treated on Tuesday.
- Randomise position too (plate edges evaporate; incubator shelves differ).
- **Blind** the person measuring the outcome: coded sample labels, key held by a colleague.

## 5. Power analysis
You need four of: effect size, variability (SD), α (usually 0.05), power (usually 0.8),
n. Solve for n.
- Two-group comparison, rule of thumb: n per group ≈ 16 ÷ d², where d = difference ÷ SD
  (Lehr's approximation for α 0.05, power 0.8). d = 1 → ~16 per group; d = 0.5 → ~64. Exact two-sample t-test power (statsmodels, two-sided) gives 16.7 and 63.8, so round up to 17 and 64.
- Get the SD from a pilot or published data; choose the effect size as the **smallest
  difference that would matter**, not the one you hope for.
- Tools: G*Power (free GUI from Heinrich Heine University Duesseldorf), R `pwr::pwr.t.test(d = 1, power = 0.8, sig.level = 0.05)` (argument names confirmed in the pwr manual).
- For complex designs (repeated measures, mixed models), simulate: generate fake data
  under your assumptions, analyse, repeat 1000× and count significant results.
- Add margin for expected attrition/failure.

## 6. Factorial designs
To test two factors (drug × genotype), use a full factorial with all combinations; the
interaction term answers "does the drug work differently in mutants?" — which two
separate experiments cannot answer. Interactions need roughly four times the sample size
of a main effect of similar magnitude: in a balanced 2x2 the interaction contrast has twice the standard error of a main effect, so detecting an equal-sized effect needs 4x the n (derived; depends on design).

## Gotchas
- Changing the analysis after seeing the data (outlier removal, switching tests, adding
  samples until p < 0.05) invalidates the p-value. Define exclusion rules in advance.
- An underpowered study that finds an effect usually overestimates it.
- "n = 3" by convention is not a power analysis.
- Report following your field's checklist (e.g. ARRIVE 2.0 from NC3Rs for animal work).

## Verify
- [ ] Comparison, primary outcome and analysis written before data collection.
- [ ] Negative, vehicle/sham and positive controls included where applicable.
- [ ] Experimental unit identified; n counts units, not sub-samples.
- [ ] Allocation randomised, blocks balanced, outcome assessment blinded.
- [ ] Sample size justified by a power calculation with sources for SD and effect size.
