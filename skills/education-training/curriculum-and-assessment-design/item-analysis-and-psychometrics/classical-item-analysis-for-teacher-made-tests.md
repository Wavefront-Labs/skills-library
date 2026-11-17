---
id: education-training.curriculum-and-assessment-design.item-analysis-and-psychometrics.classical-item-analysis-for-teacher-made-tests
name: classical-item-analysis-for-teacher-made-tests
category: education-training
field: curriculum-and-assessment-design
product: item-analysis-and-psychometrics
tags: [item-analysis-and-psychometrics, item-analysis, psychometrics, classical-test-theory, ctt, item-difficulty, p-value, facility-index, item-discrimination, discrimination-index, upper-lower-27, point-biserial, corrected-item-total-correlation, distractor-analysis, reliability, cronbachs-alpha, kr-20, standard-error-of-measurement, sem, standard-setting, angoff, modified-angoff, bookmark-method, cut-score, pass-mark, spreadsheet, excel, google-sheets, test-review]
level: practitioner
status: draft
description: "Check whether a classroom test worked: item difficulty, discrimination and distractor stats in a spreadsheet, reliability and SEM, fixing bad items, and setting a defensible pass mark."
sources:
  - "Crocker, L. & Algina, J. Introduction to Classical and Modern Test Theory (1986/2008)"
  - "Ebel, R. L. & Frisbie, D. A. Essentials of Educational Measurement, 5th ed. (1991) — discrimination guidelines"
  - "Cizek, G. J. & Bunch, M. B. Standard Setting (2007)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Classical item analysis for teacher-made tests

**Goal:** after a test, find the items that didn't measure what you meant, fix the scoring
before results go out, and improve the item bank — with nothing more than a spreadsheet.

*For research-grade tests, IRT calibration and DIF, see
social-sciences.education-research.educational-measurement.item-analysis-and-irt-calibration.*

## 1. Set up the data
One row per student, one column per item, cells = item score (1/0 for MCQ; for MCQ also keep a
second sheet with the **option chosen**, A/B/C/D). Add a total column. You need at least ~30
students for the statistics to mean much; with fewer, treat them as hints. Many platforms export
this layout directly (see
education-training.curriculum-and-assessment-design.assessment-platforms.authoring-delivering-and-analysing-digital-assessments).

## 2. Difficulty (p-value / facility)
p = proportion who got the item right (`=AVERAGE(B2:B61)` for a 0/1 column).
- p > 0.90: very easy — fine for core must-knows, adds little information.
- p < 0.30: very hard — check the key, the wording and whether it was taught.
- For partial-credit items: mean score ÷ max score.
A mid-range spread (most items 0.3–0.9) usually gives the most information. *These bands are
common guidelines, not rules; a mastery test can legitimately have many easy items.*

## 3. Discrimination
Does the item separate stronger from weaker students?
- **Upper–lower index:** sort by total; take the top and bottom 27% (or thirds for small classes).
  D = p(upper) − p(lower).
- **Corrected item–total correlation** (point-biserial with the item removed from the total):
  `=CORREL(B2:B61, $Z2:$Z61 - B2:B61)` where Z is total.
Rough guidelines (Ebel): ≥ 0.40 very good; 0.30–0.39 good; 0.20–0.29 marginal, review;
< 0.20 poor; **negative** = stronger students did worse — almost always a miskeyed or ambiguous item.

## 4. Distractor analysis
For each MCQ, count choices by option for upper and lower groups.
- Each distractor should attract **some** students (often ≥ ~5%) and more lower- than upper-group
  students.
- A distractor nobody picks is dead — replace it.
- A distractor that attracts the upper group may be arguably correct — re-read it.

## 5. Reliability and SEM
- **Cronbach's alpha** (KR-20 for 0/1 items): α = k/(k−1) × (1 − Σ item variances / total-score
  variance). In a sheet: `=VAR.P` per item column, sum them, divide by `=VAR.P(total)`.
- Rough targets: ≥ 0.70 for classroom tests, ≥ 0.80–0.90 for high-stakes decisions.
  Short tests have lower alpha; alpha also assumes one underlying construct.
- **SEM** = SD × √(1 − α). A student 2 marks below the pass mark with SEM = 3 is within error;
  build that into borderline decisions (e.g. review or reassess).

## 6. Act on it — before releasing results
1. **Negative or near-zero discrimination:** check the key first. If miskeyed, rescore. If
   ambiguous, accept two answers or drop the item for everyone.
2. Dropping items changes totals — rescore all students consistently and document the change.
3. Flag items for revision in the bank with their stats and date.
4. Note topics with low p across several items: that's a teaching issue, not an item issue.

## 7. Setting a pass mark (standard setting)
Avoid an arbitrary 50%. A **modified Angoff** is practical: 4–8 judges estimate, per item, the
probability a *minimally competent* candidate answers correctly; average across judges and sum
across items for the cut score. Discuss items with large disagreement, then re-rate. Apply SEM
when interpreting borderline scores.

## Gotchas
- **Small samples** make discrimination unstable; don't drop items based on 15 students alone.
- **Speeded tests**: unanswered final items look hard and discriminating for the wrong reason.
- High alpha doesn't mean validity — a test can reliably measure the wrong thing.
- Changing scoring after release needs a clear, fair policy; check institutional rules.

## Verify
- [ ] Difficulty and corrected item–total discrimination computed for every item.
- [ ] Every negative or < 0.20 item was checked for key errors and ambiguity.
- [ ] Dead and upper-group-attracting distractors identified.
- [ ] Alpha and SEM reported; borderline candidates considered in light of SEM.
- [ ] Any rescoring was applied to all students and documented before results went out.
