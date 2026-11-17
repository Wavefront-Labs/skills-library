---
id: social-sciences.education-research.educational-measurement.item-analysis-and-irt-calibration
name: item-analysis-and-irt-calibration
category: social-sciences
field: education-research
product: educational-measurement
tags: [educational-measurement, psychometrics, item-analysis, classical-test-theory, ctt, p-value, item-difficulty, item-discrimination, point-biserial, distractor-analysis, irt, item-response-theory, rasch, 1pl, 2pl, 3pl, graded-response-model, partial-credit-model, mirt, tam, winsteps, item-fit, infit, outfit, dif, differential-item-functioning, mantel-haenszel, test-information, equating, linking, unidimensionality, validity-argument]
level: advanced
status: gated
description: "Analyse a research test's items with classical statistics then IRT: difficulty, discrimination, distractors, Rasch/2PL/3PL fit, local dependence, DIF and test information, using R mirt or Winsteps."
sources:
  - "AERA, APA & NCME, Standards for Educational and Psychological Testing (2014)"
  - "de Ayala, The Theory and Practice of Item Response Theory (2nd ed., 2022)"
  - "Chalmers (2012), mirt: a multidimensional item response theory package, J. Statistical Software"
  - "Kolen & Brennan, Test Equating, Scaling, and Linking (3rd ed.)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Item analysis and IRT calibration

**Goal:** turn pilot responses on a research test (e.g. a 30-item fractions test used as
a study outcome) into evidence about which items work, a calibrated score scale, and
support for a validity argument.

## 1. Data prep
- Score responses (keep the raw option chosen for distractor analysis); code
  not-reached items at the end separately from skipped items — treating not-reached as
  wrong biases difficulty for late items.
- Pilot sample: CTT is usable with ~100+; Rasch calibration often from ~150–250;
  2PL/3PL need considerably more (3PL often 1,000+). Rough guides — more for polytomous
  items and DIF work.

## 2. Classical item analysis (first pass)
- **Difficulty** (p-value): proportion correct. Very easy (> .90) or very hard (< .20)
  items add little information for most of the sample.
- **Discrimination**: corrected item–total (point-biserial) correlation; < ~.20 flags
  a problem item; negative means likely miskey.
- **Distractor analysis**: each wrong option should attract some low scorers and fewer
  high scorers. A distractor chosen by high scorers often signals ambiguity or a second
  correct answer.
- **Reliability**: alpha/omega for the total; item-deleted statistics.
```r
library(psych); alpha(scored)     # r.drop = corrected item-total
```

## 3. IRT calibration
- **Model choice**: Rasch/1PL (equal discrimination; strong measurement properties,
  sample-independent person ordering); 2PL (item discrimination varies); 3PL (adds
  guessing for multiple-choice). Polytomous: partial credit (Rasch family) or graded
  response model.
- **Dimensionality**: check before IRT — scree/parallel analysis, CFA fit, or bifactor
  explained common variance. Unidimensional models on multidimensional tests distort.
- **Fit** and assumptions:
  - Rasch: infit/outfit mean squares (roughly 0.7–1.3 for MC tests, wider for
    rating scales — conventions vary).
  - 2PL/3PL: S-X² item fit, M2 global fit, RMSEA.
  - **Local dependence**: Yen's Q3 or LD-χ² (items sharing a passage often violate it;
    use testlet models or combine them).
```r
library(mirt)
m2 <- mirt(scored, 1, itemtype = "2PL")
coef(m2, IRTpars = TRUE, simplify = TRUE)   # a (discrimination), b (difficulty)
itemfit(m2); residuals(m2, type = "Q3"); plot(m2, type = "info")
```
- **Test information / SEM curve**: is measurement precise where your study population
  sits? A test built for average Year-8 pupils may be imprecise for low attainers.
- Winsteps, ConQuest, TAM (R) and flexMIRT are common alternatives.

## 4. Fairness: DIF
Test whether items function differently across groups (gender, language, country) for
people of equal ability: Mantel–Haenszel (with ETS A/B/C effect-size classification),
logistic regression DIF, or IRT likelihood-ratio tests (`mirt::DIF`, `multipleGroup`).
Statistical DIF is a flag for expert review, not automatic deletion.

## 5. Scores and linking
- Report EAP/ML ability estimates with standard errors, or summed scores if justified.
- Pre/post or multi-form designs need **linking/equating** through common (anchor)
  items — e.g. concurrent calibration or Stocking–Lord; check anchor-item drift.

## Gotchas
- Dropping misfitting items until fit is perfect can narrow the construct — weigh
  content coverage against statistics and document every removal.
- Score gain studies with ceiling effects underestimate growth.
- Sample sizes, p-value cut-offs, the < .20 discrimination flag and the 0.7-1.3 infit range are conventions (gated: unconfirmed, source is paywalled or blocked); cite the source used. R calls were confirmed against the CRAN manuals: psych::alpha reports r.drop (item-whole correlation without the item), mirt(data, 1, itemtype = "2PL"), coef(..., IRTpars = TRUE, simplify = TRUE), itemfit (default S_X2), residuals(type = "Q3") and DIF()/multipleGroup.

## Verify
- [ ] Not-reached vs omitted coded distinctly; key checked via negative discriminations.
- [ ] Dimensionality examined before choosing a unidimensional model.
- [ ] Item fit, local dependence and test information reviewed.
- [ ] DIF analysed for key subgroups and flagged items reviewed by experts.
- [ ] Linking design in place for any cross-form or pre/post comparison.
