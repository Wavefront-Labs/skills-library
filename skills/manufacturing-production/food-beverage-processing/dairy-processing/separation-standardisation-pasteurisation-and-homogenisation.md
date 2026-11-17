---
id: manufacturing-production.food-beverage-processing.dairy-processing.separation-standardisation-pasteurisation-and-homogenisation
name: separation-standardisation-pasteurisation-and-homogenisation
category: manufacturing-production
field: food-beverage-processing
product: dairy-processing
tags: [dairy-processing, milk-processing, raw-milk-reception, antibiotic-testing, separator, cream-separation, standardisation, inline-standardisation, fat-content, protein, pasteurisation, htst, 72c-15s, flow-diversion-valve, fdv, holding-tube, regeneration, plate-heat-exchanger, phosphatase-test, alp, homogeniser, homogenisation, two-stage-homogenisation, cultured-dairy, yoghurt, cheese-making, milk-powder, spray-dryer, pmo, grade-a-pmo, dairy-plant, food-processing]
level: practitioner
status: gated
description: "Core liquid-milk line: raw milk reception tests, separation and fat standardisation, HTST pasteurisation with flow diversion, homogeniser settings, and the checks that prove it."
sources: ["21 CFR 1240.61 Mandatory pasteurization for all milk and milk products in final package form (eCFR)", "US FDA Grade \"A\" Pasteurized Milk Ordinance"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Separation, standardisation, pasteurisation and homogenisation

**Goal:** turn raw milk into safe, standardised milk at the declared fat level, with a
stable emulsion — the base for liquid milk and for cultured, cheese and powder lines.

## 1. Raw milk reception
- Tanker sample before unloading: temperature (commonly ≤6–7 °C on arrival (gated: unconfirmed, source is paywalled or blocked); local rules
  vary), **antibiotic/beta-lactam rapid test** (e.g. Charm, SNAP, Delvotest) — a positive
  tanker is rejected and must not touch the silo, plus composition, acidity, sensory.
- Record seal numbers and the silo it went into (traceability).

## 2. Separation
- Centrifugal separators split milk into skim and cream; separation efficiency is best
  warm (often ~45–55 °C after regeneration heating (gated: unconfirmed, source is paywalled or blocked); cold separation exists for quality reasons).
- Watch skim fat (target typically ≤0.05% (gated: unconfirmed, source is paywalled or blocked)), back pressure on outlets, and the
  **desludging** (partial discharge) interval — sludge build-up drops efficiency.
- Bowl vibration alarm = stop. Separators run at several thousand rpm; never open covers
  until the bowl has fully stopped.

## 3. Standardisation
- **Inline**: a controller remixes cream into skim to hit the target fat, using
  density/flow meters or NIR. Calibrate against lab results (Gerber, Röse-Gottlieb or
  mid-IR milk analyser) at start and per frequency.
- **Batch**: calculate with the Pearson square, mix in a tank, sample, adjust.
- Declared fat is legal; overshoot gives away cream (the plant's most valuable stream).

## 4. HTST pasteurisation
- Minimum for milk: **72 °C for 15 s** (US 21 CFR 1240.61 lists 161 °F (72 °C) for 15 s, with a higher temperature or 191 °F/1 s options, and a higher figure for milk products with 10% fat or more; EU/UK equivalence unconfirmed (gated: unconfirmed, source is paywalled or blocked)). Plants often run a few degrees higher for margin.
- Sections: regeneration (incoming cold milk heated by outgoing hot milk) → heating →
  **holding tube** → regeneration (cooling) → cooling to ≤4–6 °C.
- **Flow diversion valve (FDV)**: if temperature at the end of the holding tube drops
  below set point, milk is diverted back to the balance tank. Check the FDV cut-in/cut-out
  test as scheduled (in the US, regulatory seals and tests per PMO).
- **Pressure**: pasteurised milk side kept at higher pressure than raw side in the
  regeneration section, so any leak contaminates raw milk, not pasteurised (the US PMO sets the exact differential and test rules (gated: unconfirmed, source is paywalled or blocked)). A booster pump
  and differential-pressure controls enforce this.
- **Verification**: alkaline phosphatase (ALP) test on pasteurised milk (negative = adequate
  heat); recording thermometer charts signed per run.

## 5. Homogenisation
- High-pressure pump forces milk through a narrow gap, breaking fat globules (to ~<1 µm)
  so cream doesn't rise.
- Two-stage: first stage e.g. 150–200 bar, second ~20–50 bar (gated: unconfirmed, source is paywalled or blocked) (breaks clusters) — settings
  depend on product (higher for UHT and cream liqueur style emulsions; lower for cream).
- Temperature ≥ ~55–60 °C (gated: unconfirmed, source is paywalled or blocked); cold milk homogenises poorly.
- Check: **creaming test** (leave a sample, measure fat in top vs bottom layer) or
  particle-size analysis; listen for knocking (valve/seat wear, air in feed).

## 6. Downstream lines (pointers)
- **Yoghurt/cultured**: heat milk harder (e.g. 90–95 °C for several minutes (gated: unconfirmed, source is paywalled or blocked)) to denature
  whey proteins for body; inoculate at incubation temperature; track pH to the break point.
- **Cheese**: milk standardised on protein/fat ratio; rennet and cutting time govern yield.
- **Powder**: evaporator then spray dryer; outlet temperature controls moisture; watch for
  powder fires (explosion-relief and CO2 systems).

## Gotchas
- Unloading a tanker before the antibiotic result is back.
- Raw milk pressure higher than pasteurised in regeneration after a booster pump trip.
- FDV in manual/inspect mode left on after maintenance.
- Standardisation controller "drifting" because the lab result used for calibration was from a stale sample.

## Verify
- [ ] Every tanker antibiotic-negative before unloading; records traceable to silo.
- [ ] Fat content within declared tolerance, controller calibrated today.
- [ ] Pasteuriser chart shows holding temperature above legal minimum all run; FDV checks done.
- [ ] Pressure differential correct in regeneration; ALP test negative.
- [ ] Homogenisation pressures logged; creaming test passed.
