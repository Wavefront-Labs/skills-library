---
id: natural-sciences.agricultural-science.animal-science-research.livestock-feeding-trial-design
name: livestock-feeding-trial-design
category: natural-sciences
field: agricultural-science
product: animal-science-research
tags: [agricultural-science, animal-science-research, animal-science, feeding-trial, nutrition-trial, experimental-unit, pen, pseudoreplication, randomised-block, latin-square, crossover-design, adaptation-period, feed-intake, dry-matter-intake, average-daily-gain, adg, feed-conversion-ratio, fcr, feed-efficiency, body-weight, shrunk-weight, power-analysis, animal-ethics, iacuc, arrive-guidelines, mixed-model, repeated-measures, welfare-assessment, broilers, pigs, cattle]
level: practitioner
status: draft
description: "Design a livestock feeding trial that survives review: the right experimental unit, weight blocking, adaptation, accurate intake and weights, power, ethics approval and mixed models."
sources: [St-Pierre 2007 J Dairy Sci (experimental unit and statistics), ARRIVE 2.0 guidelines, FASS Guide for the Care and Use of Agricultural Animals in Research and Teaching (4th ed.), NRC/NASEM nutrient requirement series]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Livestock feeding trial design

**Goal:** test a diet, additive or feeding strategy on growth, efficiency or product
output with a design whose statistics are valid — the most common reason animal
nutrition papers are rejected is getting the experimental unit wrong.

## 1. Identify the experimental unit
The **experimental unit** is the smallest unit to which a treatment is independently
applied. If ten pigs share a pen and a feeder that receives the diet, the **pen** is the
unit (n = pens, not pigs). Individual animals are units only when individually fed
(e.g. electronic feeders like Calan gates or GrowSafe/Insentec bins, tie stalls,
metabolism crates) *and* randomised individually. Counting animals in group pens as
replicates is pseudoreplication.

## 2. Choose a design
- **Randomised complete block:** block by initial body weight, sex, parity or room;
  assign treatments within blocks. The workhorse for growth trials.
- **Latin square / crossover:** each animal receives every treatment in sequence (e.g.
  4×4 Latin square in dairy cows with 21-day periods). Efficient for short-term
  responses like rumen fermentation or milk composition; requires adequate washout and
  is unsuitable for outcomes with carryover (growth, reproduction, health).
- **Factorial** for two factors (e.g. energy × additive) — check for interaction before
  interpreting main effects.

## 3. Power and sample size
Use prior CVs for your outcome (from the literature or your herd). ADG and feed
efficiency often have CVs ~8–15% per pen; detecting a 5% improvement may need 8–12
pens per treatment. Underpowered trials produce "no significant difference" that
means nothing. Ethics committees also require justified numbers (reduction principle).

## 4. Running the trial
- **Ethics approval** (IACUC or national equivalent) before animals arrive; welfare
  monitoring and humane endpoints written in the protocol.
- **Adaptation:** typically 7–14 days to the facility and 14–21 days to new diets for
  ruminants (rumen microbes adapt slowly) before data collection; shorter for poultry.
- **Diets:** formulate to meet requirements (NASEM/NRC) except the tested factor;
  sample and **analyse each batch** (DM, CP, NDF, energy, the tested nutrient) and
  report analysed, not just formulated, values.
- **Intake:** weigh feed offered and refused daily (or per period); sample refusals for
  DM. Intake = offered DM − refused DM.
- **Body weight:** weigh at consistent times; for cattle use consecutive-day weights
  at start and end, or a standard shrink (e.g. overnight off feed/water or a 4% pencil
  shrink — practice varies), because gut fill swings weight several percent.
- Record health events and removals with reasons; decide exclusion rules in advance.
- **Blind** staff to treatment where possible (coded feeds).

## 5. Analysis
- Mixed model with treatment fixed, block random (or fixed), unit = pen/animal; initial
  weight as a covariate where appropriate.
- Repeated measures (weekly weights, milk yield) need a covariance structure (AR(1),
  unstructured) chosen by AIC — not separate ANOVAs per week.
- **FCR** is a ratio — analyse it at the unit level (total feed / total gain per pen),
  and consider analysing gain:feed (G:F) which behaves better statistically.
- Report LSMeans ± SEM, P-values and the n per treatment with the unit stated.
  Follow ARRIVE 2.0 reporting items.

## Gotchas
- Pen effects (location, ventilation, feeder space) confound treatment if treatments are
  clustered in one room — spread them across rooms/blocks.
- Feed wastage under feeders inflates intake; check and correct.
- A treatment that changes palatability changes intake — separate intake effects from
  efficiency effects in interpretation.

## Verify
- [ ] Experimental unit defined correctly and n counted in units.
- [ ] Blocking, randomisation and power calculation documented; ethics approval in hand.
- [ ] Adaptation period, analysed diet composition and intake/weight methods recorded.
- [ ] Mixed model with appropriate covariance; ARRIVE items reported.
