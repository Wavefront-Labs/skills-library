---
id: social-sciences.food-science-research.sensory-science.descriptive-analysis-panel-training-and-performance
name: descriptive-analysis-panel-training-and-performance
category: social-sciences
field: food-science-research
product: sensory-science
tags: [sensory-science, sensory-evaluation, descriptive-analysis, qda, quantitative-descriptive-analysis, spectrum-method, generic-descriptive-analysis, trained-panel, panel-training, lexicon, reference-standards, panel-performance, panelcheck, senspanel, mixed-model-anova, product-by-assessor-interaction, discrimination, repeatability, consensus, pca, sensory-profile, iso-13299, iso-8586, compusense, redjade, fizz, cata]
level: practitioner
status: draft
description: "Run a research-grade descriptive sensory analysis: recruit and train a panel, build a lexicon with references, design balanced sessions, check panel performance and analyse with mixed ANOVA and PCA."
sources:
  - "Lawless & Heymann, Sensory Evaluation of Food: Principles and Practices (2nd ed.)"
  - "Stone, Bleibaum & Thomas, Sensory Evaluation Practices (5th ed.)"
  - "ISO 13299 (descriptive profiling) and ISO 8586 (selection and training of assessors)"
  - "Tomic et al. (2010), PanelCheck software paper, Food Quality and Preference"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Descriptive analysis: panel training and performance

**Goal:** produce a quantitative sensory profile of products (intensity of each
attribute) from a trained panel that behaves like a calibrated instrument — and prove it
did. For discrimination tests (triangle, duo-trio) and basic trained-panel set-up see
hospitality-culinary.sensory-evaluation.tasting-panel-methods.running-triangle-tests-and-trained-panels.

## 1. Pick the method
- **QDA®-style / generic descriptive analysis**: panel develops its own vocabulary,
  unstructured line scales, products compared relative to each other. Most common in
  research.
- **Spectrum™**: absolute intensity scales anchored to universal references; heavier
  training, better cross-study comparability.
- **Rapid methods** (CATA, flash profile, napping, RATA) trade precision for speed —
  fine for screening, weaker for small differences.

## 2. Panel recruitment and screening (ISO 8586 guidance)
- Recruit ~12–20 candidates to end with **8–12 panelists**.
- Screen for basic taste and odour recognition, ranking intensities, ability to
  describe, availability for the whole study, no relevant allergies.

## 3. Training (often 10–40 hours, depending on product complexity)
1. **Lexicon generation**: panel tastes the full product range and lists attributes;
   leader consolidates synonyms and removes hedonic/vague terms ("nice", "natural").
2. **Definitions and reference standards** for each attribute and for scale anchors
   (e.g. a defined sucrose solution for "sweet", a specific commercial product for a
   texture anchor). Write the evaluation protocol: order of attributes, bite/sip size,
   palate cleanser (water, unsalted cracker), wait times.
3. **Calibration sessions**: rate products, show each panelist their scores against
   the panel mean, discuss outliers with references in hand.
4. Proceed to formal evaluation only when performance checks (below) pass on a practice run.

## 4. Formal evaluation design
- Booths with controlled lighting (red/coloured light if colour differences must be
  masked), 3-digit random codes, samples at standardised temperature and portion.
- **Balanced presentation** (Williams Latin square for carry-over); **2–3 replicates**
  per product, ideally in separate sessions.
- Limit products per session (sensory fatigue; ~4–6 for strong flavours is a rough cap).
- Software: Compusense, RedJade, FIZZ, EyeQuestion — or paper with careful data entry.

## 5. Panel performance checks
Using PanelCheck (free) or R (`SensoMineR`), per attribute:
- **Discrimination**: does each panelist separate products (assessor-level F for product)?
- **Repeatability**: low replicate error (MSE plots).
- **Agreement / consensus**: product × assessor interaction; profile plots and
  Tucker-1 plots show who disagrees.
Retrain or drop attributes, not just panelists, when an attribute fails broadly.

## 6. Analysis
- Mixed-model ANOVA per attribute: product (fixed), assessor (random), product ×
  assessor (random), replicate/session. Treating assessor as random tests product
  against the interaction — more conservative and appropriate for generalising.
- Post-hoc (Tukey HSD or Fisher LSD, stated) on significant attributes.
- **PCA** on the product × attribute mean matrix for a sensory map; link to
  instrumental or consumer data with PLS regression or preference mapping.

## Gotchas
- **Halo and dumping**: if a salient attribute is missing from the ballot, panelists
  dump it into others. Include it or add an "other" check.
- Panel drift over weeks — re-calibrate with references at the start of each session.
- Ballot order effects: keep a logical order (appearance → aroma → flavour → texture →
  aftertaste) and fixed across products.
- Uncertain: hours of training and product limits vary widely; justify yours.

## Verify
- [ ] Lexicon has written definitions and physical references for each attribute.
- [ ] Balanced serving order, coded samples, ≥ 2 replicates.
- [ ] Discrimination, repeatability and agreement checked before analysis.
- [ ] Mixed ANOVA with assessor random; PCA map interpretable against the lexicon.
