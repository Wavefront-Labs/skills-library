---
id: energy-mining-utilities.oil-gas-extraction.field-gas-processing.operating-a-glycol-dehydrator-and-amine-unit
name: operating-a-glycol-dehydrator-and-amine-unit
category: energy-mining-utilities
field: oil-gas-extraction
product: field-gas-processing
tags: [field-gas-processing, gas-processing, gas-plant-operator, gas-conditioning, dehydration, glycol-dehydration, teg, triethylene-glycol, glycol-contactor, reboiler, still-column, stripping-gas, water-dew-point, hydrates, methanol-injection, amine, amine-sweetening, mdea, dea, sour-gas, h2s, co2-removal, foaming, antifoam, lean-amine, rich-amine, compressor, reciprocating-compressor, hydrocarbon-dew-point, jt-valve]
level: practitioner
status: draft
description: "Operate field gas conditioning: TEG dehydration (circulation, reboiler, water dew point) and amine sweetening (foaming, lean loading, H2S safety), plus compressor rounds."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Operating a glycol dehydrator and amine unit

**Goal:** deliver gas that meets the pipeline's water, H₂S/CO₂ and hydrocarbon dew-point
specifications, with glycol and amine systems running steadily and cheaply.

> Status: draft. Typical values are given as ranges seen in industry literature (e.g.
> GPSA-style guidance) and are not your plant's setpoints. Sales gas specifications are
> set by the pipeline contract.

## 1. TEG dehydration
- Wet gas flows up the **contactor**, lean triethylene glycol flows down and absorbs
  water. Rich glycol goes through a flash tank, filters, a heat exchanger and the
  **reboiler/still**, where water is boiled off, then back as lean glycol.
- **Water dew point** of the dry gas is the key spec (often expressed as lb/MMscf or a
  dew point at pressure). If it's off:
  - **Glycol purity too low** — reboiler temperature low (TEG reboilers commonly run
    near 190–200 °C; above about 204 °C TEG degrades), or not enough stripping gas.
  - **Circulation rate** off — too low and the gas isn't dried; too high wastes fuel and
    can carry over. A common rule of thumb is a few gallons TEG per lb of water removed;
    check your design.
  - **Contactor temperature** too high (hot gas carries more water) or foaming.
- **Glycol losses:** carryover from the contactor (foaming, high gas rates), vaporisation
  from the still, leaks. Track makeup volumes.
- Keep glycol clean: filters changed on differential pressure, pH in range, no
  hydrocarbon contamination (skim the flash tank).
- Hydrates: if dehydration is down, methanol injection may be needed upstream to stop
  hydrates plugging lines and chokes.

## 2. Amine sweetening
- Sour gas contacts lean amine (e.g. MDEA, DEA) in the absorber; rich amine is
  regenerated in a stripper with a reboiler, releasing acid gas (H₂S/CO₂) to a sulphur
  unit, incinerator or flare per permit.
- Watch: treated gas H₂S/CO₂ against spec; **lean amine loading**; amine strength;
  reboiler duty; absorber differential pressure.
- **Foaming** is the classic upset — sudden rise in absorber ΔP, amine carryover,
  off-spec gas. Causes: hydrocarbons, solids, degradation products, excess antifoam.
  Respond with antifoam per procedure, then find the cause (filters, carbon bed,
  inlet separator performance).
- Keep lean amine temperature a few degrees above the gas inlet temperature to avoid
  hydrocarbon condensation in the absorber (a widely used rule).
- **H₂S safety:** personal monitors, buddy system, breathing apparatus for sampling and
  line breaks. H₂S deadens the sense of smell at dangerous levels.

## 3. Compression rounds
- Reciprocating compressors: check suction/discharge pressures and temperatures per
  stage, lube oil pressure and level, cylinder lubricator feed, vibration, and
  scrubber dumps (liquid carried into a cylinder breaks it).
- Unusual knocking, high discharge temperature or rising vibration → shut down and
  investigate rather than run to failure.

## 4. Hydrocarbon dew point
Where heavier hydrocarbons must be removed, a JT valve, refrigeration or turbo-expander
chills the gas to drop out liquids. Watch chiller outlet temperature and the separator
levels.

## Gotchas
- Glycol reboiler fire tubes fail from scale and hot spots — keep glycol clean.
- Amine plants drift slowly; record trends daily, not just alarms.
- Dehydrator still vents can emit BTEX — follow emission controls.

## Verify
- [ ] Dry gas water content / dew point within spec.
- [ ] TEG reboiler temperature and circulation in range; losses tracked.
- [ ] Treated gas H₂S/CO₂ in spec; no signs of foaming.
- [ ] H₂S precautions followed for sampling and maintenance.
- [ ] Compressor readings logged; scrubbers dumping.
