---
id: mathematics.statistics.spss.syntax-driven-analysis-in-spss
name: syntax-driven-analysis-in-spss
category: mathematics
field: statistics
product: spss
tags: [statistics, spss, ibm-spss, spss-syntax, paste-button, variable-view, measurement-level, missing-values, recode, compute, select-if, filter, split-file, weight-cases, frequencies, descriptives, crosstabs, t-test, oneway, unianova, glm-repeated-measures, regression, reliability, cronbach-alpha, output-viewer, social-science]
level: intro
status: draft
description: "Use SPSS reproducibly: set up variables and missing codes, paste menu choices into syntax, recode and filter safely, run common tests, and read the output tables correctly."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Syntax-driven analysis in SPSS

**Goal:** do the usual social-science analyses in SPSS while keeping a syntax file
that reproduces every number — the menus are fine for exploring, syntax is the record.

## 1. Use Paste, not OK
Every dialog has a **Paste** button. It writes the command into a Syntax Editor
window instead of running it. Save that `.sps` file next to the data; run with
Run › All (or select lines and Ctrl+R). Add comments: `* Recode age into bands.`
(comment lines start with `*` and end with a full stop). Every command ends with a
**full stop** — a missing one is the commonest syntax error.

## 2. Set up variables (Variable View)
- **Measurement level** (Nominal / Ordinal / Scale) controls what Chart Builder and
  some procedures allow. Set it honestly.
- **Value labels** (`1 = Female`, `2 = Male`) and **user-missing codes**:
```spss
VALUE LABELS sex 1 'Female' 2 'Male'.
MISSING VALUES income (-99, -98).
```
If −99 ("refused") is not declared missing, it gets averaged into the mean. Check
with `FREQUENCIES` on every key variable before analysis.

## 3. Transform safely
```spss
RECODE age (18 thru 34=1) (35 thru 54=2) (55 thru HIGHEST=3) (ELSE=SYSMIS) INTO age_band.
COMPUTE bmi = weight / (height/100)**2.
EXECUTE.
```
- Always `RECODE ... INTO` a **new** variable; recoding in place destroys the original.
- `ELSE=COPY` vs `ELSE=SYSMIS` matters — be explicit.
- Transformations are pending until a procedure or `EXECUTE.` runs.

## 4. Subsets: FILTER, not SELECT IF
```spss
COMPUTE adults = (age >= 18).
FILTER BY adults.
* ... analyses ...
FILTER OFF.
```
`SELECT IF` **permanently deletes** unselected cases from the active dataset (unless
preceded by `TEMPORARY.`). `SPLIT FILE` and `WEIGHT BY` stay on until you turn them
off — forgetting `SPLIT FILE OFF.` or `WEIGHT OFF.` silently changes every later
result. Check the status bar ("Filter On", "Weight On", "Split File On").

## 5. Common procedures
```spss
FREQUENCIES VARIABLES=sex age_band /STATISTICS=MEAN MEDIAN.
CROSSTABS /TABLES=smoker BY sex /STATISTICS=CHISQ /CELLS=COUNT ROW EXPECTED.
T-TEST GROUPS=sex(1 2) /VARIABLES=score.
ONEWAY score BY age_band /STATISTICS=DESCRIPTIVES WELCH /POSTHOC=GH.
REGRESSION /STATISTICS COEFF CI(95) R ANOVA COLLIN /DEPENDENT score
  /METHOD=ENTER age sex income.
RELIABILITY /VARIABLES=q1 TO q8 /MODEL=ALPHA /SUMMARY=TOTAL.
```

## 6. Read the output correctly
- **Independent-samples t-test:** SPSS prints two rows, "Equal variances assumed" and
  "not assumed" (Welch). Report the **Welch row** by default rather than choosing via
  Levene's test.
- Recent versions report one- and two-sided p; "Sig. (2-tailed)" is the usual one.
- `Sig. = .000` means p < .001 — report it that way, never as p = 0.
- **Crosstabs:** check the footnote "x cells have expected count less than 5"; if
  more than ~20% do, use Fisher's exact test (`/STATISTICS=CHISQ` gives it for 2×2).
- **Regression:** use the *Unstandardized B* and its CI for interpretation; Beta is
  standardised. VIF > ~5–10 in the Collinearity column flags instability.
- **Reliability:** "Cronbach's Alpha if Item Deleted" shows items that hurt the scale;
  reverse-score negatively worded items first.

## 7. Save outputs
Export the Output Viewer to PDF/Word for sharing (`OUTPUT EXPORT`), and keep the
`.spv` file. Archive data, syntax and output together with the SPSS version number.

## Gotchas
- Variable names are case-insensitive; `q1 TO q8` uses **file order**, not names.
- Dates are seconds since 14 Oct 1582 — compute differences with `DATEDIFF`.
- Default "exclude cases analysis by analysis" vs "listwise" changes n between
  tables; set it deliberately in the Options dialog.
- Uncertain: exact output labels and the one-/two-sided p display vary by SPSS
  version (the dual display arrived around v27); confirm against your release.

## Verify
- [ ] Every result in the report can be regenerated from the saved `.sps`.
- [ ] User-missing codes declared; frequencies show no stray −99s.
- [ ] Recodes went INTO new variables.
- [ ] No unintended FILTER/SPLIT/WEIGHT left on.
- [ ] Welch row reported for t-tests; expected-count warnings checked in crosstabs.
