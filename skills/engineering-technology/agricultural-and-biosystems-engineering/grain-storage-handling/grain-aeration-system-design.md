---
id: engineering-technology.agricultural-and-biosystems-engineering.grain-storage-handling.grain-aeration-system-design
name: grain-aeration-system-design
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: grain-storage-handling
tags: [agricultural-and-biosystems-engineering, grain-storage-handling, grain-aeration, aeration-fan, airflow-rate, cfm-per-bushel, equilibrium-moisture-content, emc, modified-henderson, chung-pfost, asabe-d245, asabe-d272, shedd-curves, static-pressure, grain-bin, silo, natural-air-drying, cooling-front, aeration-controller, grain-temperature-cables, safe-storage-moisture, mwps-13, post-harvest, stored-grain, grain-entrapment]
level: practitioner
status: verified
description: "Design bin or silo aeration: safe storage moisture, EMC of ambient air, airflow rate by purpose (cooling, holding, natural-air drying), static pressure and fan selection, and control rules."
sources:
  - "MidWest Plan Service MWPS-13, Grain Drying, Handling and Storage Handbook"
  - "ASABE D245 Moisture Relationships of Plant-Based Agricultural Products"
  - "ASABE D272 Resistance to Airflow of Grains, Seeds, Other Agricultural Products"
  - "Brooker, Bakker-Arkema & Hall, Drying and Storage of Grains and Oilseeds"
  - "Grains Research and Development Corporation (Australia), grain storage fact sheets"
  - "Purdue Extension GQTF-38 Temporary Grain Storage Considerations (https://www.extension.purdue.edu/extmedia/gq/gqtf38/gqtf-38.html)"
  - "Purdue Extension AED-20 Managing Dry Grain in Storage (https://www.extension.purdue.edu/extmedia/aed/aed-20.html)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Grain aeration system design — airflow, pressure, fan and control

**Goal:** keep stored grain cool and uniform (or dry it slowly with air) by sizing
airflow and fans to the bin depth, and running them only on useful air.

## 1. Know the storage target
Safe moisture (wet basis) for long-term storage in cool climates, per Purdue Extension AED-20: corn 14 % for 6-12 months and 13 % beyond a year, soybeans 12 % up to a year and 11 % beyond, wheat 14 % up to 6 months and 13 % beyond (1 point lower for poor-quality grain); canola about 8 % (gated: unconfirmed, source is paywalled or blocked). Short-term winter
storage tolerates about 1–2 points more. Allowable storage time falls sharply with
temperature; keep grain within roughly 5–10 °C of average ambient and near 0–5 °C in
winter where climate allows.

## 2. Equilibrium moisture content (EMC)
Air at a given temperature and RH drives grain toward its EMC. ASABE D245 fits the
modified Henderson or Chung-Pfost equation per crop, e.g. modified Henderson:
`1 − RH = exp[−K (T + C) M^N]` (M % dry basis, T °C; constants per crop in D245).
Approximate values at 10 °C (gated: unconfirmed, source is paywalled or blocked) (check D245 tables; not recomputed here):

| RH | Maize EMC (% wb) | Wheat EMC (% wb) | Soybean EMC (% wb) |
|---|---|---|---|
| 60 % | ~13.5 | ~13 | ~10.5 |
| 70 % | ~15 | ~14 | ~12.5 |
| 80 % | ~17 | ~16 | ~15 |

Running fans on air with EMC above grain moisture rewets the grain near the inlet.

## 3. Airflow rate by purpose
| Purpose | US units (cfm/bu) | SI (L/s per tonne, approx.) |
|---|---|---|
| Cooling / maintenance aeration | 0.05–0.2 | 1–3 |
| Holding wet grain briefly | 0.5–1 | 9–18 |
| Natural-air / low-temperature drying | 1–2 (more for wetter grain) | 18–35+ |

Conversion: 1 cfm/bu ≈ 0.80 m³/min per m³ of grain. Natural-air drying rates depend on
harvest moisture and local weather; use regional extension tables or simulation.

Cooling-front time rule of thumb: **hours ≈ 15 ÷ (cfm/bu)**, so 0.1 cfm/bu needs about
150 fan hours per cooling cycle (Purdue GQTF-38: minimum 150 hours at 0.1 cfm/bu, halving airflow doubles it; varies with season and RH). Unit check (computed): 5,000 cfm = 2.36 m3/s; 1 cfm/bu = 0.80 m3/min per m3; 3-4 in. water = 747-996 Pa.

## 4. Static pressure and fan selection
1. Compute total airflow: e.g. 50,000 bu at 0.1 cfm/bu = 5,000 cfm (≈ 2.4 m³/s).
2. Superficial velocity = airflow ÷ floor area. Read pressure drop per metre (or foot)
   of grain from **Shedd's curves** (ASABE D272), multiply by depth.
3. Add a packing factor (fines and spreader compaction raise resistance, often
   1.3–1.5× (gated: unconfirmed, source is paywalled or blocked)) and duct/floor losses.
4. Pick a fan whose **performance curve** delivers the flow at that pressure: axial fans
   below about 750–1,000 Pa (3–4 in. water), centrifugal or inline-centrifugal above (practice rule (gated: unconfirmed, source is paywalled or blocked)).

Depth matters non-linearly: at constant cfm/bu, doubling depth doubles both velocity and
path length, so pressure and fan power rise several-fold. Tall silos favour low
aeration rates; drying in deep bins becomes uneconomic.

## 5. Air distribution
- Full perforated floors suit drying; ducts suffice for aeration. Keep perforated duct
  face velocity low (commonly cited ≤ 0.15 m/s, 30 fpm (gated: unconfirmed, source is paywalled or blocked)) and duct air velocity moderate
  (vendor tables) to avoid uneven flow and noise.
- Longest air path should not exceed about 1.5× the shortest (gated: unconfirmed, source is paywalled or blocked), or the far zones are under-aerated.
- Level the grain surface and core out fines from the centre after filling; a peaked
  cone of fines starves the middle of air.
- Provide roof vents of at least 1 square foot per 1000 cfm (Purdue GQTF-38) so the roof does not over-pressurise or
  draw vacuum (and to limit condensation).

## 6. Control
Run cooling aeration when ambient air is **5–10 °C below grain temperature** (rule of thumb (gated: unconfirmed, source is paywalled or blocked)) and its EMC
is near or below the target moisture. Automatic controllers use temperature and RH
windows; temperature cables in the bin show whether a cooling front has passed.
Stop once the front exits the top.

## Gotchas
- Pushing (positive) vs pulling (negative) aeration: pulling draws solar-warmed
  headspace air down through the grain and can condense moisture in cold ducts and the
  fan; pushing adds fan heat (often ~1 °C (gated: unconfirmed, source is paywalled or blocked)) and condenses under a cold roof.
- Fan heat and humid nights can rewet grain at the inlet layer if run blindly.
- Moisture migration in winter: warm centre, cold walls causes crusting at the top centre.
- **Entrapment and confined space**: never enter a bin with unloading equipment running;
  lock out, test the atmosphere, use a harness and attendant. Follow local regulations.
- Bin structural loads (unsymmetric discharge, aeration with wet grain swelling) need a
  qualified structural engineer and the manufacturer's limits.

## Verify
- [ ] Storage target moisture and temperature are set per crop and climate.
- [ ] Airflow rate matches the purpose (cool, hold, dry) and grain depth.
- [ ] Static pressure was derived from airflow resistance data with a packing factor.
- [ ] Selected fan curve meets flow at that pressure; roof venting is adequate.
- [ ] Controller logic uses temperature difference and EMC, and cable readings confirm fronts pass.
