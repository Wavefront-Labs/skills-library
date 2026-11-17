---
id: social-sciences.anthropology.cross-cultural-comparison.hraf-sampling-coding-and-galtons-problem
name: hraf-sampling-coding-and-galtons-problem
category: social-sciences
field: anthropology
product: cross-cultural-comparison
tags: [cross-cultural-comparison, cross-cultural-research, hraf, ehraf, ehraf-world-cultures, ocm, owc, outline-of-cultural-materials, sccs, standard-cross-cultural-sample, probability-sample-files, psf, ethnographic-atlas, d-place, galtons-problem, phylogenetic-comparative-methods, non-independence, trait-coding, inter-rater-reliability, focal-time, focal-place, comparative-hypothesis-testing, holocene]
level: advanced
status: draft
description: "Testing cross-cultural hypotheses: eHRAF searching with OCM codes, sampling (SCCS, PSF), coding traits reliably and handling Galton's problem."
sources: ["Ember & Ember, Cross-Cultural Research Methods (2nd ed., 2009)", "Murdock & White, 'Standard Cross-Cultural Sample' (1969)", "HRAF, eHRAF World Cultures user guides", "Kirby et al., 'D-PLACE' PLoS ONE (2016)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HRAF sampling, coding and Galton's problem

**Goal:** test a hypothesis about human societies (e.g. "warfare frequency predicts
male-centred residence") on a defensible sample of cultures, with reproducible codes.

## 1. Frame a testable hypothesis
Name both variables, the unit (a society at a time and place), and the expected
direction. Write an operational definition for each variable before reading cases:
what counts as "frequent" warfare? Pre-registration is increasingly expected.

## 2. Choose a sample
- **eHRAF World Cultures:** full-text ethnography indexed by paragraph. Its
  **Probability Sample Files (PSF)** — 60 cultures, one randomly chosen per region —
  give a ready random sample.
- **Standard Cross-Cultural Sample (SCCS):** 186 well-described societies chosen to
  reduce historical relatedness; many variables already coded by others.
- **Ethnographic Atlas** (~1,290 societies) and **D-PLACE** (an open database
  linking cultural, linguistic and environmental data) for large-N coded variables.
Gotcha: pre-coded variables may not measure *your* concept; check the original
codebook definitions before reusing.

## 3. Search eHRAF properly
Paragraphs are tagged with **OCM** subject codes (Outline of Cultural Materials, e.g.
the 720s for war-related topics — *check the current OCM list for exact numbers*).
Combine OCM codes with keywords; keyword-only search misses paraphrase and older
spelling. Read surrounding context — a paragraph can be about a neighbouring group.

## 4. Fix focal time and place
Ethnographies describe different decades and communities. Pin each case to a
**focal time and place** and code only material that fits; otherwise you can code
warfare from 1890 against residence from 1960.

## 5. Coding
- Write ordinal scales with anchor examples ("1 = no mention of warfare in focal
  period... 4 = warfare almost constant, every year").
- Include a **data-quality** rating and a "not enough information" code — never
  guess a value to fill the cell.
- Use **two independent coders**, ideally blind to the hypothesis and coding each
  variable in separate passes. Report agreement (e.g. Cohen's kappa or correlation for
  ordinal codes); resolve disagreements by discussion and log changes.

## 6. Galton's problem (non-independence)
Societies share traits by common descent or diffusion, so they aren't independent
data points; naive tests overstate significance. Responses:
- Sampling that spaces cases (SCCS, one per region in the PSF).
- Control variables for region or language family.
- **Phylogenetic comparative methods** using language trees, or spatial/network
  autocorrelation models (common in D-PLACE-based work).
Report which you used and why.

## 7. Analysis and reporting
Report N after exclusions, missing data handling, effect sizes, and robustness to
dropping low-quality cases. Correlation across cultures is not causation within one.

*Uncertainty:* eHRAF access requires an institutional subscription; sample sizes above
are as commonly cited — confirm against current HRAF documentation.

## Verify
- [ ] Hypothesis and operational definitions written before coding.
- [ ] Sample named (PSF/SCCS/etc.) with exclusion log.
- [ ] Focal time/place recorded per case.
- [ ] Two coders, reliability statistic reported, "insufficient info" code used.
- [ ] Galton's problem explicitly addressed in the analysis.
