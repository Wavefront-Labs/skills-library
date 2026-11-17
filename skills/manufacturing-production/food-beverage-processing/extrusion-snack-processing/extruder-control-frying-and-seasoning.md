---
id: manufacturing-production.food-beverage-processing.extrusion-snack-processing.extruder-control-frying-and-seasoning
name: extruder-control-frying-and-seasoning
category: manufacturing-production
field: food-beverage-processing
product: extrusion-snack-processing
tags: [extrusion-snack-processing, food-extrusion, extruder, twin-screw-extruder, single-screw-extruder, wenger, clextral, buhler, sme, specific-mechanical-energy, barrel-temperature, moisture, die-pressure, expansion, bulk-density, texture, puffed-snacks, cereals, pellets, fryer, continuous-fryer, frying-oil, oil-turnover, free-fatty-acids, ffa, polar-compounds, tpm, acrylamide, seasoning, tumble-drum, oil-slurry, electrostatic-seasoning, salt-content, crisps, chips, food-processing]
level: practitioner
status: draft
description: "Run food extruders and snack fryers: control moisture, screw speed and temperature for expansion and density, manage frying oil quality, and get seasoning coverage consistent."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Extruder control, frying and seasoning

**Goal:** produce snacks or cereal pieces at target bulk density, texture, moisture,
oil and seasoning level, and keep them there across a long run.

## 1. How the extruder makes expansion
Inside the barrel, starch is cooked by heat and shear under pressure; at the die,
superheated water flashes to steam and the piece expands. Expansion depends mostly on:
| Lever | Effect (typical direction) |
|---|---|
| **Feed moisture** ↑ | Less expansion, denser, harder; lower die pressure |
| **Screw speed** ↑ | More shear/SME, more expansion (to a point), lower viscosity |
| **Barrel temperature** ↑ | More cooking, lower melt viscosity, can reduce or increase expansion depending on regime |
| **Feed rate** ↑ at fixed speed | Higher fill, higher pressure, lower SME |
| **Die open area** ↓ | Higher pressure, more expansion until it surges |
**SME** (specific mechanical energy, kWh/t) = motor power used ÷ throughput — a single number
that tracks how cooked the product is. Keep it in the recipe window rather than chasing one setting.

## 2. Running checks
- **Bulk density** (fixed-volume cup weighed) every check — the primary expansion measure.
- Piece size/shape against standard; **moisture** after dryer (often ~1–3% for crunchy products).
- **Die pressure and motor load trends**: a slow rise can be die blockage; sudden spikes
  can be a foreign body or feed moisture change.
- **Surging** (pulsing output, density swinging): unstable feed (bridging in hopper,
  water dosing pump), or running near a pressure/fill boundary.
- Start-up and shut-down: run on a wetter start-up mix where specified to avoid
  burning on; never let the barrel run empty at high temperature (product chars and seizes).

## 3. Frying
- Oil temperature per product (crisps often ~170–185 °C in; extruded fried pellets per spec).
  Lower temperature = higher oil pickup; higher = darker colour and more acrylamide.
- **Oil quality**: aim for high **turnover** (fresh oil added as fried product removes oil
  — fast turnover keeps oil fresh). Monitor **FFA** and/or **total polar compounds**
  (e.g. Testo 270; many jurisdictions/brand limits around 24–27% TPM). Remove fines
  continuously — burnt fines degrade oil.
- **Acrylamide** mitigation (EU Regulation 2017/2158 benchmarks for crisps): control
  frying temperature, colour (use colour standards/vision), potato sugar levels.
- Fryer fires: know the suppression system and the shutdown. Never use water.

## 4. Seasoning
- **Tumble drum** with oil spray then dry powder, or oil slurry. **Electrostatic**
  applicators improve adhesion and reduce dust.
- Seasoning rate is ratioed to product flow — calibrate the **powder feeder** (catch test
  over set time) and confirm product flow from weigh belt.
- Check **seasoning %** (weigh unseasoned vs seasoned sample, or salt by titration/
  conductivity) and coverage visually.
- Seasoning adheres best to warm, freshly fried/oiled product; long conveyors before seasoning cut adhesion.
- **Allergens** in seasonings (milk, soy, mustard, celery) → changeover cleaning per
  manufacturing-production.food-beverage-processing.haccp-food-safety.ccp-monitoring-and-allergen-changeovers.

## Gotchas
- Raising water to fix "too hard" while flour moisture had already risen.
- Topping fryer with a different oil type without approval (labelling).
- Seasoning feeder bridging — product runs plain for minutes before anyone notices.
- Breaking pieces in conveyors after seasoning (drop heights) — fines also overload the dust collector.

## Verify
- [ ] SME, die pressure and bulk density inside the recipe window at each check.
- [ ] Final moisture in spec.
- [ ] Fryer temperature logged; oil quality (FFA/TPM) under limit; fines removed.
- [ ] Colour/acrylamide indicators within standards.
- [ ] Seasoning % and coverage checked; feeder calibrated this shift.
