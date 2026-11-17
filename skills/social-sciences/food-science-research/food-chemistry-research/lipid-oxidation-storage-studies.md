---
id: social-sciences.food-science-research.food-chemistry-research.lipid-oxidation-storage-studies
name: lipid-oxidation-storage-studies
category: social-sciences
field: food-science-research
product: food-chemistry-research
tags: [food-chemistry-research, food-chemistry, lipid-oxidation, rancidity, peroxide-value, pv, tbars, malondialdehyde, hexanal, p-anisidine, totox, conjugated-dienes, rancimat, oxidative-stability-index, osi, accelerated-storage, arrhenius, q10, headspace-gc-ms, spme, antioxidants, tocopherols, rosemary-extract, omega-3, aocs-methods, flavour-chemistry, storage-study]
level: practitioner
status: draft
description: "Design a lipid-oxidation storage study for foods: primary vs secondary markers (PV, TBARS, hexanal, p-anisidine), sampling schedule, accelerated tests, controls and pitfalls in interpretation."
sources:
  - "Frankel, Lipid Oxidation (2nd ed., 2005)"
  - "AOCS Official Methods (e.g. Cd 8b-90 peroxide value, Cd 18-90 p-anisidine, Cd 12b-92 OSI)"
  - "Shahidi & Zhong (2005), Lipid oxidation: measurement methods, Bailey's Industrial Oil and Fat Products"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Lipid oxidation storage studies

**Goal:** quantify how fast fats in a food oxidise under storage (and whether an
antioxidant, packaging or formulation change slows it), using markers that capture the
whole oxidation pathway rather than a single misleading number.

## 1. Know what each marker measures
Lipid oxidation runs initiation → propagation (hydroperoxides build up) → termination
(hydroperoxides break down into aldehydes, ketones — the rancid off-flavours).
- **Primary products**
  - *Peroxide value (PV)*: iodometric titration (AOCS Cd 8b-90) or the more sensitive
    ferric thiocyanate / ferrous xylenol orange methods for low-fat or small samples.
  - *Conjugated dienes*: UV absorbance ~233 nm; quick, less specific.
- **Secondary products**
  - *TBARS*: malondialdehyde-type compounds reacting with thiobarbituric acid,
    ~532 nm. Cheap and common, but **non-specific** (sugars and other aldehydes react).
  - *p-Anisidine value*: aldehydes, mainly 2-alkenals; used with PV as TOTOX = 2·PV + AV.
  - *Hexanal* (from omega-6) or *propanal* (from omega-3) by headspace SPME-GC-MS —
    the most flavour-relevant marker.
- **Stability tests**: Rancimat / OSI measure induction time at high temperature with
  airflow — useful for ranking oils/antioxidants, not for predicting shelf life directly.

**Key interpretive rule:** PV rises then *falls* as hydroperoxides decompose, so a low
PV can mean fresh *or* heavily oxidised. Always pair a primary and a secondary marker,
and ideally sensory evaluation.

## 2. Study design
- **Samples and controls**: test formulation(s), a no-antioxidant negative control, and
  where relevant a positive control (e.g. a known synthetic antioxidant). Same batch of
  raw material for all.
- **Storage conditions**: realistic temperature (and light, if retail-lit), plus
  optionally an accelerated condition (e.g. elevated temperature). Control oxygen
  exposure: headspace volume, packaging, how often containers are opened (prefer one
  sealed unit per time point per replicate).
- **Time points**: more frequent early on (e.g. 0, 3, 7, 14, 28, 56 days for an
  accelerated study), extending to end of intended shelf life.
- **Replication**: ≥ 3 independent replicate units per treatment × time; analytical
  duplicates within each.

## 3. Lab practice
- Extract lipid gently (cold solvent methods such as Bligh & Dyer or Folch variants)
  without heat; flush with nitrogen, store extracts at −20 °C or below, analyse promptly.
- Express results per gram of **fat** (and per gram of product) — stated clearly.
- Run blanks and a reference oil each batch; build calibration curves (TEP/MDA
  standard for TBARS, internal standard for hexanal).
- Check fatty-acid profile at t0 (GC-FAME) to justify which aldehyde to track.

## 4. Analysis
- Plot each marker over time per treatment; fit kinetic models (zero/first order) only
  where the curve shape supports it.
- Compare treatments with two-way ANOVA (treatment × time) or mixed models; report lag
  phase / induction period where visible.
- **Accelerated-to-real extrapolation** with Arrhenius or Q10 assumes the same mechanism
  at both temperatures — often false (e.g. fat melting, water activity, Maillard
  interactions). Validate with at least one real-time point.

## Gotchas
- Pro-oxidant metals (iron, copper), light and water activity can dominate formulation
  effects; record and control them.
- Some "natural antioxidant" extracts interfere with TBARS colour; run sample blanks.
- Emulsions: oxidation often starts at the interface; method of extraction matters.
- Uncertain: method numbers above should be checked against the current AOCS edition.

## Verify
- [ ] At least one primary and one secondary marker (plus sensory where possible).
- [ ] Controls from the same raw-material batch; one sealed unit per time point.
- [ ] Results expressed per g fat; calibration and blanks run per batch.
- [ ] Accelerated extrapolation checked against a real-time point, or not claimed.
