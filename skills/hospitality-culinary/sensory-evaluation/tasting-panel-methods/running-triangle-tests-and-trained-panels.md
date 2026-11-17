---
id: hospitality-culinary.sensory-evaluation.tasting-panel-methods.running-triangle-tests-and-trained-panels
name: running-triangle-tests-and-trained-panels
category: hospitality-culinary
field: sensory-evaluation
product: tasting-panel-methods
tags: [tasting-panel-methods, sensory-panel, sensory-science, triangle-test, duo-trio, paired-comparison, discrimination-test, descriptive-analysis, qda, panel-training, panel-calibration, panelist-screening, blind-coding, randomisation, three-digit-codes, binomial, significance, iso-4120, iso-8589, tasting-booth, quality-control, product-development]
level: practitioner
status: draft
description: "Run sensory panels: screen and train tasters, set up blind coded samples, run triangle and paired tests with the right significance count, build descriptive panels, and keep panels calibrated."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running triangle tests and trained panels

**Goal:** get sensory answers you can trust — "is there a difference?", "what is the
difference?" — rather than one person's opinion. Methods follow standard sensory
practice (e.g. ISO 4120 triangle test, ISO 8589 test-room design); consult the
standards for formal work.

## 1. Pick the right test for the question
| Question | Test |
|---|---|
| Is there *any* perceptible difference (e.g. new supplier, cheaper ingredient)? | **Triangle** or duo-trio |
| Which is *more* X (sweeter, more bitter)? | **Paired comparison** (2-AFC) |
| What exactly differs, and by how much? | **Descriptive analysis** (trained panel) |
| Do consumers prefer/like it? | **Hedonic/acceptance** test with untrained consumers (many more people) |
Don't ask a trained panel if they "like" things, and don't ask consumers to describe
attributes precisely.

## 2. Test-room protocol
- Quiet, odour-free, neutral lighting; booths or separated seating; no talking.
- **Coded samples**: random **three-digit codes**, never "A/B".
- **Randomise and balance** presentation order across panellists (for triangle: all
  six orders AAB, ABA, BAA, ABB, BAB, BBA equally often).
- Identical portion, temperature, container. Use coloured light if appearance would
  give away the answer.
- Palate cleansers (water, unsalted crackers) and rest between sets; limit samples to
  avoid fatigue.
- Panellists avoid smoking, coffee, strong food and fragrance for ~30–60 min before.

## 3. Triangle test step by step
1. Each panellist gets three coded samples: two the same, one different. Task: pick
   the odd one (forced choice, must guess if unsure).
2. Chance of guessing right is **1/3**.
3. Count correct answers and compare to the **minimum correct for significance**
   (one-tailed binomial, p = 1/3). At α = 0.05:
   - 12 panellists → **8** correct
   - 18 → **10**
   - 24 → **13**
   - 30 → **15**
   - 36 → **18**
   (Computed from the binomial; matches published tables to within rounding.)
4. "Not significant" doesn't prove "no difference" — small panels lack power. For
   "similarity" claims (e.g. supplier swap), use more panellists and a similarity design
   with stated β and proportion of distinguishers per the standard.

## 4. Screening and training panellists
- **Screen** for basic taste recognition (sweet, sour, salty, bitter, umami at
  threshold-level concentrations), odour recognition, and ability to rank intensity.
- **Train** with reference standards for each attribute (e.g. a defined sucrose
  solution = "sweetness 5"), building a shared **lexicon**.
- Typical descriptive panels: ~8–12 trained panellists, trained over many sessions.

## 5. Descriptive analysis
1. Panel generates attributes with references, agrees definitions.
2. Panellists rate each attribute on a line or numeric scale, in replicate.
3. Analyse with ANOVA (product × panellist × replicate); visualise with spider plots
   or PCA.

## 6. Calibration and monitoring
- Include **blind replicates** and a known reference; track each panellist's
  repeatability and agreement with the panel.
- Retrain or recalibrate panellists who drift; rotate references regularly.
- Record session conditions; illness, colds and medications affect results.

## Gotchas
- Leaking the answer (different cups, uneven pours, temperature differences).
- Too many samples in one session — fatigue, carry-over.
- Same people always tasting their own products (bias).
- Reporting "no difference" from 6 people.

## Verify
- [ ] Question matched to the right test type.
- [ ] Samples blind-coded, orders balanced.
- [ ] Significance threshold taken from the binomial table for the panel size.
- [ ] Panel performance tracked over time with replicates.
