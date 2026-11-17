---
id: energy-mining-utilities.renewable-energy-field-operations.biogas-plant-operations.biogas-digester-feeding-and-gas-cleanup
name: biogas-digester-feeding-and-gas-cleanup
category: energy-mining-utilities
field: renewable-energy-field-operations
product: biogas-plant-operations
tags: [renewable-energy-field-operations, biogas-plant-operations, biogas, anaerobic-digestion, ad-plant, farm-biogas, food-waste-digestion, feedstock, silage, slurry, manure, organic-loading-rate, fos-tac, vfa, ammonia-inhibition, mesophilic, thermophilic, h2s, desulphurisation, biological-desulphurisation, iron-dosing, activated-carbon, gas-dryer, chiller, siloxane, chp, gas-engine, flare, methane-slip, biomethane, digestate]
level: practitioner
status: draft
description: "Run an agricultural or food-waste biogas plant: feedstock mix and loading, FOS/TAC and temperature, H2S and moisture removal, and keeping the CHP engine fed and protected."
sources:
  - "KTBL / FNR Biogas guides (Germany) on process monitoring, concepts paraphrased"
  - "Gas-engine manufacturers' fuel gas quality requirements, general practice paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Biogas digester feeding and gas cleanup

**Goal:** keep the digester biology stable on a changing diet and deliver clean, dry gas to
the engine — the two things that decide whether a biogas plant earns money.

(For sewage-sludge digesters see
`energy-mining-utilities.wastewater-sewerage.sludge-biosolids-handling.anaerobic-digester-monitoring-and-dewatering`.)

## 1. Feeding
- **Consistency beats quantity.** Same mix, many small feeds per day. Feed changes
  (new silage clamp, new food-waste contract) are introduced over 1–3 weeks.
- Track **organic loading rate** (kg oDM/m³·d) — many farm plants run ~2–4; know your
  design figure and stay under it.
- Keep a feed log: tonnes per feedstock, dry matter (DM%) and organic DM — DM varies a
  lot between silage clamps and loads.
- Nitrogen-rich feeds (poultry litter, some food waste) raise **ammonia**; free ammonia
  inhibits methanogens, worse at higher temperature and pH. Blend with low-N material.
- Remove contaminants (plastics, grit, stones) at reception; they fill digesters and wreck
  pumps and mixers.

## 2. Watching the biology
- **FOS/TAC** (volatile acids to buffer ratio) weekly or more; many plants are stable
  around 0.2–0.4 — *your* stable baseline is what matters. A rising trend = feed less.
- **Temperature**: mesophilic ~38–42 °C on many farm plants, thermophilic ~50–55 °C;
  keep within ~±1 °C/day.
- **Gas yield per tonne fed** and **CH4%** (online analyser): falling methane with
  constant feed is a warning.
- Foam: sudden foaming often follows feed changes (e.g. sugar beet, certain food waste);
  have antifoam and a plan.
- Trace elements (Co, Ni, Se, Mo) deficiencies appear on mono-feed (e.g. maize-only)
  plants; analysis and supplements per adviser.

## 3. Gas cleanup
- **H2S**: corrodes engines and produces SO2. Methods: biological desulphurisation by tiny
  controlled air injection into the gas space (typically a few % of gas flow — too much
  air risks explosive mixtures and oxygen in the engine fuel), iron salts dosed into the
  digester, and/or an activated-carbon polishing filter. Measure H2S before and after.
- **Moisture**: cool the gas (chiller/condensate trap underground pipe) so it is dry at
  the engine; drain condensate traps regularly — a full trap blocks gas.
- **Siloxanes** (mainly food/sewage): carbon filters; they form abrasive silica deposits in
  engines.
- Check engine maker's gas spec (H2S ppm, relative humidity, CH4 minimum) and log.

## 4. Engine/CHP and flare
- Engine running hours, oil analysis for acidity (TBN/TAN) shows H2S problems.
- Gas storage level control: engine load follows gas production; flare must start
  automatically when storage is full — test it.
- Methane slip at the engine and leaks from roofs/membranes are both lost money and
  greenhouse emissions; leak-survey with a gas camera or detector.

## 5. Safety
Biogas: flammable, H2S toxic, CO2 asphyxiant. ATEX zones around digesters and gas
handling, gas detectors, no ignition sources, confined-space rules for tanks and pits.

## Verify
- [ ] Feed log with DM% kept; changes introduced gradually.
- [ ] FOS/TAC, temperature, CH4% and gas yield trended.
- [ ] H2S after cleanup within engine spec; air injection limited and controlled.
- [ ] Condensate traps drained; flare auto-start tested.
- [ ] Gas detection and ATEX controls in place.

*Uncertain:* the numerical ranges are typical for European farm plants; your process
adviser's values take precedence.
