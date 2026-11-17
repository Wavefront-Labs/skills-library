---
id: social-sciences.sociology.survey-research.secondary-analysis-of-gss-ess-and-panel-surveys
name: secondary-analysis-of-gss-ess-and-panel-surveys
category: social-sciences
field: sociology
product: survey-research
tags: [survey-research, sociology, secondary-analysis, gss, general-social-survey, ess, european-social-survey, issp, world-values-survey, psid, soep, understanding-society, ukhls, bhps, panel-data, survey-weights, complex-survey-design, strata, psu, clustering, design-effect, survey-package, stata-svy, fixed-effects, random-effects, hybrid-model, attrition, harmonisation, codebook, social-indicators]
level: practitioner
status: draft
description: "Do secondary analysis of social surveys (GSS, ESS, panel studies): find the right weights, handle complex design, harmonise waves and fit panel models correctly."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Secondary analysis of large social surveys and panels

**Goal:** answer a sociological question with an existing high-quality survey,
producing estimates that respect how the data were sampled and how variables changed
over time.

## 1. Pick the dataset
| Survey | Design | Good for |
|---|---|---|
| GSS (US) | Repeated cross-section since 1972; a panel component in some years | Long-run attitude trends |
| ESS | Biennial cross-national cross-sections since 2002 | Cross-country comparison in Europe |
| ISSP / WVS / EVS | Cross-national modules | Global comparisons, values |
| PSID, SOEP, Understanding Society (UKHLS, incl. BHPS) | Household panels | Within-person change, mobility, life events |
Download through the official archive (NORC GSS Data Explorer, ESS Data Portal, UK
Data Service, GESIS). Register, accept the user agreement, cite the dataset DOI.

## 2. Read the documentation before the data
- Questionnaire wording **for each year** — wording, response options or routing
  (who was asked) change. A "trend" can be a question change.
- Codebook missing-value codes (e.g. 8 "don't know", 9 "no answer", or negative codes
  in many panels). Recode them to missing explicitly — leaving 98/99 as numbers is the
  commonest silent error.
- Variable split-ballots: in the GSS many items were asked of only a random subset.

## 3. Weights and design
- Find the recommended weight for your analysis: the ESS provides design weights,
  post-stratification weights and population-size weights (analysis weight = combination
  depending on whether you pool countries — check current ESS guidance; recommendations
  were updated in later rounds). GSS has several weight variables with year-specific advice.
- Use **strata and PSU/cluster** variables to get correct standard errors:
```r
library(survey)
des <- svydesign(ids = ~psu, strata = ~stratum, weights = ~wt, data = d, nest = TRUE)
svymean(~trust, des, na.rm = TRUE); svyglm(trust ~ educ + age, design = des)
```
Stata: `svyset psu [pw=wt], strata(stratum)` then `svy:` prefix.
- Ignoring clustering understates SEs (design effects of 1.5–2+ are common).
- Subpopulation analysis: use `subset()` on the design object (R) or `svy, subpop()`
  (Stata), not filtering the data first — filtering breaks variance estimation.

## 4. Harmonisation across waves or countries
Build a crosswalk table: source variable per wave → harmonised variable, recodes, and
notes. For education and occupation, use standard schemes (ISCED, ISCO/ISEI, EGP/ESeC)
and document version changes (e.g. ISCO-88 → ISCO-08).

## 5. Panel models
- **Fixed effects (within-person):** controls all stable unobserved traits; estimates
  only from people whose X changes. `plm`, `fixest::feols(y ~ x | pid)`, Stata `xtreg, fe`.
- **Random effects:** more efficient but assumes unobservables are uncorrelated with X.
- **Hybrid / within-between** (Allison; Bell & Jones) gives both within and between
  effects in one model — often the most informative.
- Cluster SEs by person; consider lagged predictors for temporal ordering.
- **Attrition:** use the panel's longitudinal weights; compare stayers and leavers;
  note that weights correct only for observed predictors of dropout.

## 6. Reporting
Report the survey, waves, weights used, design variables, unweighted n and weighted
estimates, and missing-data handling. Share syntax so others can reproduce from the
public file.

## Gotchas
- Pooling countries with population weights vs not answers different questions
  (average person in Europe vs average country).
- Cross-national comparisons of attitudes need measurement invariance.
- Uncertain: weight variable names and recommendations differ by round/version —
  always check the latest user guide.

## Verify
- [ ] Question wording and routing confirmed for every year used.
- [ ] Missing-value codes recoded explicitly.
- [ ] Correct weight + strata + PSU specified; subpopulations handled on the design.
- [ ] Harmonisation crosswalk documented.
- [ ] Panel model choice (FE/RE/hybrid) justified and attrition addressed.
