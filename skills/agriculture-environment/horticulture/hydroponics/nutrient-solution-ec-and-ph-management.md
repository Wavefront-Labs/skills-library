---
id: agriculture-environment.horticulture.hydroponics.nutrient-solution-ec-and-ph-management
name: nutrient-solution-ec-and-ph-management
category: agriculture-environment
field: horticulture
product: hydroponics
tags: [horticulture, hydroponics, soilless-culture, nutrient-solution, ec, electrical-conductivity, ppm, tds, ph, ph-down, ph-up, a-and-b-nutrients, two-part-nutrients, stock-solution, nft, nutrient-film-technique, dwc, deep-water-culture, ebb-and-flow, drip-to-waste, rockwool, coco-coir, perlite, root-rot, pythium, dissolved-oxygen, reservoir, ec-meter, ph-meter, calibration, lettuce, tomatoes]
level: practitioner
status: draft
description: "Mix and manage hydroponic nutrient solution: two-part A/B stocks, target EC and pH per crop, meter calibration, daily checks, top-up vs change, water temperature and oxygen to keep roots healthy."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Nutrient solution EC and pH management

**Goal:** keep the root zone at the right strength (EC) and acidity (pH), with enough
oxygen and a safe temperature — the four variables that decide whether a hydroponic crop
thrives or crashes.

> Draft. EC/pH bands are common grower ranges; follow your nutrient manufacturer's chart
> for the actual recipe. "ppm" readings depend on the meter's conversion factor (500 or 700
> scale) — talk in EC (mS/cm) to avoid confusion.

## 1. Mixing from two-part (A/B) concentrates
- Two parts exist because calcium (part A, with nitrate) and sulfates/phosphates (part B)
  precipitate if mixed concentrated.
- **Never mix A and B concentrates directly.** Fill the reservoir with water, add A, stir,
  then add B, stir, then check EC, then adjust pH last.
- Start from your water: measure its EC first (soft water ~0.0–0.3, hard tap water can be
  0.5+ mS/cm and carry lots of Ca/Mg/bicarbonate). Reverse osmosis water may need Cal-Mag
  additions per the nutrient maker.

## 2. Target ranges (indicative)
| Crop | EC (mS/cm) | pH |
|---|---|---|
| Lettuce, leafy greens | 0.8–1.6 | 5.6–6.2 |
| Herbs (basil) | 1.0–1.8 | 5.6–6.4 |
| Strawberries | 1.2–2.0 | 5.6–6.2 |
| Tomatoes, cucumbers, peppers (fruiting) | 2.0–3.5 | 5.6–6.2 |
Seedlings/clones: start at ~half strength.
pH ~5.5–6.3 keeps most nutrients available; iron and manganese lock out above ~6.5, and
calcium/magnesium uptake suffers below ~5.5.

## 3. Meters — calibrate or don't bother measuring
- **pH meter:** two-point calibration (pH 7 then pH 4) weekly, store the probe wet in
  storage solution (never distilled water), replace probes ~yearly.
- **EC meter:** calibrate with a standard (e.g. 1.413 mS/cm) monthly; use temperature-compensated readings.

## 4. Daily routine
1. Check reservoir level, EC, pH, solution temperature.
2. **Top up** lost volume with plain water if EC has risen (plants drinking more than
   eating) or with half-strength nutrient if EC has fallen.
3. Adjust pH in small steps with pH down (phosphoric/nitric acid) or pH up (potassium
   hydroxide/carbonate); mix, wait 15–30 min, re-measure. Wear eye protection.
4. Look at roots: white/cream and fuzzy = healthy; brown, slimy, smelly = root rot.

## 5. Full changes
Recirculating solution drifts — some ions are taken up faster than others, so EC alone
stops telling the truth. Replace the full reservoir every **1–3 weeks** (smaller systems
more often), or run drain-to-waste and test runoff EC/pH instead.

## 6. Oxygen and temperature
- Keep solution **~18–22 °C**. Above ~24–26 °C dissolved oxygen drops and *Pythium* root
  rot thrives. Insulate/shade reservoirs, use a chiller in hot climates.
- **DWC:** air stones running 24/7. **NFT:** thin film, channel slope ~1:30–1:100, never
  let the film stop (roots die in minutes-hours in hot weather). Have a pump-failure alarm.
- Opaque reservoirs and covers stop algae.

## 7. System notes
- **Coco/rockwool drip:** pre-soak/buffer coco (calcium-magnesium), water to ~10–20% runoff,
  compare runoff EC to feed EC: runoff much higher → salts building up, increase runoff/flush.
- Clean and sterilise everything between crops.

## Gotchas
- Calibrating the pH meter is skipped more than anything else — and a 0.5 drift misleads every decision.
- Adding pH down straight into concentrate, or acid into a near-empty tank, overshoots.
- Warm, stagnant solution in a power cut kills NFT crops fastest; plan for it.

## Verify
- [ ] Meters calibrated on schedule; calibration date logged.
- [ ] EC and pH in the crop's band, logged daily with temperature.
- [ ] Solution 18–22 °C, aerated or flowing continuously; failure alarm in place.
- [ ] Full change or runoff test on schedule.
- [ ] Roots white and fuzzy at weekly inspection.
