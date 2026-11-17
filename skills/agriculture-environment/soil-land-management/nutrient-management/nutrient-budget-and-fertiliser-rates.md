---
id: agriculture-environment.soil-land-management.nutrient-management.nutrient-budget-and-fertiliser-rates
name: nutrient-budget-and-fertiliser-rates
category: agriculture-environment
field: soil-land-management
product: nutrient-management
tags: [soil-land-management, nutrient-management, nutrient-budget, fertiliser, fertilizer, fertiliser-rates, 4r-stewardship, nitrogen, phosphorus, potassium, sulfur, urea, map, dap, muriate-of-potash, superphosphate, uan, split-application, topdressing, volatilisation, manure, slurry, effluent, crop-removal, yield-target, p2o5, k2o, nutrient-conversion, agronomy, pasture]
level: practitioner
status: gated
description: "Build a paddock nutrient budget (crop removal, soil supply, efficiency), convert to product rates (urea, MAP, potash, manure), and time N in splits to cut volatilisation and leaching losses."
sources: ["https://pubs.ext.vt.edu/SPES/SPES-201/SPES-201.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Nutrient budget and fertiliser rates

**Goal:** apply the nutrient the crop is actually short of, at a rate that pays,
at a time it can use it — the "4R" idea: right source, rate, time, place.

## 1. The budget: what goes out, what the soil supplies (gated: unconfirmed, source is paywalled or blocked)
`Fertiliser need = (crop demand or removal − soil supply) ÷ efficiency`

- **Removal** (what leaves in grain, hay or product). Typical figures per tonne of
  grain (check local tables — they shift with protein and variety):

  | Crop | N kg/t | P kg/t | K kg/t | S kg/t |
  |---|---|---|---|---|
  | Wheat (~11.5% protein) | ~20 | ~3 | ~4–5 | ~1.5 |
  | Barley | ~17 | ~3 | ~5 | ~1.5 |
  | Canola | ~35–40 | ~6 | ~9 | ~10 |
  | Hay (per t DM, grass) | ~15–20 | ~2.5 | ~15–20 | ~2 |

  Hay and silage strip K fast — a cut-and-carry paddock can be K-negative within a
  few years even when grain paddocks next door are fine.
- **Soil supply:** for N, a pre-sowing deep soil mineral-N test (0–60 or 0–90 cm)
  plus expected mineralisation; for P and K, the soil test decides whether you
  build, maintain or mine (see
  `agriculture-environment.soil-land-management.soil-testing.soil-sampling-and-test-interpretation`).
- **Efficiency:** crops recover only part of what you apply — roughly 40–60% of (gated: unconfirmed, source is paywalled or blocked)
  fertiliser N in-season and often <30% of fertiliser P in year one (gated: unconfirmed, source is paywalled or blocked). Budget for it.

## 2. Convert nutrient to product
Bags and labels may quote oxides. Convert first:
- P = P2O5 × 0.436; K = K2O × 0.83 (and back: P2O5 = P × 2.29, K2O = K × 1.20).

Common products (elemental %, approximate):

| Product | N | P | K | S |
|---|---|---|---|---|
| Urea | 46 | – | – | – |
| UAN (liquid, % w/w) | 28–32 | – | – | – |
| Ammonium sulfate | 21 | – | – | 24 |
| MAP | 10 | 22 | – | 1–2 |
| DAP | 18 | 20 | – | – |
| Single superphosphate | – | 8.8 | – | 11 |
| Muriate of potash (MOP) | – | – | 50 | – |

**Worked example:** 15 kg P/ha needed → 15 ÷ 0.22 = 68 kg MAP/ha, which also
delivers 6.8 kg N. A further 60 kg N/ha needed → (60 − 6.8) ÷ 0.46 ≈ 116 kg urea/ha.

## 3. Timing and placement
- **N: split it.** Some at sowing, the rest topdressed at the crop's high-demand
  stage (cereals: tillering to first node, GS22–GS31). Lets you cut the second
  split in a dry year.
- **Urea volatilisation:** surface urea on warm, moist soil with no rain can lose
  10–30%+ as ammonia (gated: unconfirmed, source is paywalled or blocked). Apply ahead of ≥10 mm forecast rain (gated: unconfirmed, source is paywalled or blocked), incorporate, or use a
  urease inhibitor (e.g. NBPT-treated urea). Don't spread onto dew-wet soil that
  then dries.
- **Leaching/denitrification:** avoid big N doses on sands before heavy rain or on
  waterlogged clays.
- **P:** place near the seed (banded at sowing) — it barely moves in soil. Keep
  ammonium phosphates within the safe seed-row rate for your seeder's row spacing
  and soil moisture; high N with the seed damages germination (canola is most
  sensitive).
- **K and S:** can be topdressed; sulfate-S is mobile and leaches on sands.

## 4. Manure and effluent
1. Get a lab analysis of *your* manure — nutrient content varies several-fold.
2. Count availability: slurry ammonium-N is largely available in year one; organic
   N in solid manures is much slower (often ~20–40% in year one (gated: unconfirmed, source is paywalled or blocked), rest over years).
3. Rate manure to the **most limiting** constraint — often P. Rating to N alone
   tends to overload P and raises run-off risk.
4. Calibrate the spreader (tray test: collect from a known area, weigh).
5. Respect local rules: setbacks from waterways, closed periods, maximum N loading.

## Gotchas
- Oxide vs elemental mix-ups produce 2× errors; always label your units.
- A yield target that's never achieved inflates every rate downstream — use a
  realistic, rainfall-based target.
- Spreader overlap and uncalibrated rates commonly add ±15% error (gated: unconfirmed, source is paywalled or blocked). Calibrate.
- Price per tonne of product is meaningless; compare **price per kg of nutrient**.

**Uncertainty:** removal figures and efficiencies are rounded generalisations from
extension literature; local crop-response trials and regulations override them.
Not field-verified by the author.

## Verify
- [ ] Budget written per paddock: removal, soil supply, efficiency, net need.
- [ ] Every rate converted from nutrient to product with units labelled.
- [ ] N split into at least two timings, with a weather check before urea goes out.
- [ ] Seed-row fertiliser within safe limits for the crop and row spacing.
- [ ] Manure rated on a lab analysis and the most limiting nutrient.

## Checked

- Date: 2026-10-25. Jurisdiction: no regulation involved; local manure and nutrient rules are named as the governing limits in the skill.
- Confirmed against: Virginia Tech Extension SPES-201 gives P2O5 to P = 0.4365 and K2O to K = 0.8301 (the skill's 0.436 and 0.83); fertiliser percentages follow from standard grades (MAP 11-52-0 is about 22.7% P, DAP 18-46-0 about 20% P, MOP 60% K2O is about 50% K) and the worked example was recomputed (15 / 0.22 = 68 kg MAP; (60 - 6.8) / 0.46 = 116 kg urea).
- Not confirmed: the crop removal table, nutrient recovery rates, manure availability, spreader error and ammonia loss and rain-timing figures (no free primary source reached).

Method: documentation only; no commands were run.
