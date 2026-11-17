---
id: humanities.archaeology.archaeological-dating.radiocarbon-sampling-and-calibration
name: radiocarbon-sampling-and-calibration
category: humanities
field: archaeology
product: archaeological-dating
tags: [archaeological-dating, archaeology, radiocarbon, carbon-14, c14, ams, calibration, intcal20, shcal20, marine20, oxcal, calib, bayesian-modelling, bayesian-chronology, cal-bc, bp, short-lived-samples, old-wood-effect, reservoir-effect, dendrochronology, osl, luminescence, relative-dating, seriation, terminus-post-quem, chronology]
level: practitioner
status: draft
description: "Choose and submit radiocarbon samples that actually date the event, calibrate correctly with IntCal20/SHCal20/Marine20 in OxCal, report results properly, and know when another method fits better."
sources:
  - "Reimer, P. et al. (2020) The IntCal20 Northern Hemisphere radiocarbon age calibration curve, Radiocarbon 62(4)"
  - "Bronk Ramsey, C. OxCal online manual"
  - "Historic England, Radiocarbon Dating and Chronological Modelling: Guidelines and Best Practice (2022)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Radiocarbon sampling and calibration

**Goal:** get a date that answers the question ("when was this pit filled?"), not just a
date for some carbon that happened to be in it.

## 1. Choose the sample for the event
- The sample must be **related to the event** you want to date and **securely stratified**.
- Prefer **short-lived, single-entity** material: one cereal grain, a hazelnut shell, a
  twig, an articulated animal bone, a human bone. Single entities avoid averaging mixed ages.
- Avoid bulk charcoal from long-lived trees: the **old-wood effect** — heartwood of an oak may
  be centuries older than the fire.
- Articulated bone (still joined when buried) was deposited fresh; loose bone may be residual.
- Collect with clean tools into foil or glass; no glue, consolidant, or labels touching it.
  Record context, position and why it dates the event.

## 2. Reservoir effects
- **Marine** carbon (shells, fish, seals, and people or animals that ate a lot of them) looks
  older than contemporary terrestrial material. Calibrate with **Marine20** plus a local
  ΔR correction, or a mixed curve based on δ13C/δ15N diet estimates.
- **Freshwater** reservoirs (hard-water lakes/rivers) can also add apparent age; no general
  curve — need local data.

## 3. Calibration
- Labs report a **conventional radiocarbon age** in **BP** (before AD 1950) ± 1σ, e.g.
  `3450 ± 30 BP (lab code)`. That is *not* a calendar date.
- Calibrate with the right curve: **IntCal20** (Northern Hemisphere terrestrial),
  **SHCal20** (Southern Hemisphere), **Marine20** (marine). OxCal (online, free) or CALIB.
- Report the calibrated **range** at 95.4% probability (and optionally 68.3%), e.g.
  "1880–1690 cal BC (95.4%)". The result is a probability distribution, often multi-peaked —
  don't quote the midpoint as "the date".
- **Plateaus** in the curve (notoriously ~800–400 BC, the "Hallstatt plateau") give wide
  ranges no matter how precise the measurement.

## 4. Bayesian modelling
With several dates and a known stratigraphic order (from the Harris matrix — see
`humanities.archaeology.stratigraphic-excavation.single-context-excavation-and-harris-matrix`),
OxCal can model phases, boundaries and sequences to narrow ranges dramatically. Outputs
are model-dependent: publish the model code and the agreement indices, and test
alternative models. *Consider getting a specialist to build models for publication.*

## 5. Other methods (brief)
- **Dendrochronology:** exact felling year if bark edge/sapwood survives and a regional
  master chronology exists. Needs ideally 50+ rings.
- **Luminescence (OSL/TL):** sediments' last exposure to light / ceramics' last heating;
  ranges typically ±5–10%. OSL samples must be taken in light-tight tubes, with in-situ
  dosimetry.
- **Relative:** seriation, typology, stratigraphy — only order, but cheap and often
  sufficient.

## Gotchas
- A date on residual material dates nothing useful; context integrity matters more than lab precision.
- Report lab codes, δ13C (if measured), curve, software version and probability level — a
  bare "c. 1800 BC" is unusable.
- Recalibrate old published dates with the current curve before comparing.

## Verify
- [ ] Each sample is short-lived/single-entity (or justified) and linked to the event.
- [ ] Reservoir risk assessed; correct curve chosen.
- [ ] Results reported as BP ± error with lab code, then calibrated range with curve, software and probability.
- [ ] Bayesian models published with code and agreement indices.
