---
id: agriculture-environment.irrigation-water-management.water-storage-harvesting.farm-dam-and-tank-water-budget
name: farm-dam-and-tank-water-budget
category: agriculture-environment
field: irrigation-water-management
product: water-storage-harvesting
tags: [water-storage-harvesting, farm-dam, dugout, pond, reservoir, water-tank, rainwater-harvesting, roof-runoff, catchment-yield, runoff-coefficient, water-budget, dam-volume, evaporation-loss, seepage, depth-gauge, drought-planning, storage-capacity, stock-water, irrigation-allocation, dam-safety, spillway, blue-green-algae]
level: practitioner
status: gated
description: "Budget farm water storage across a season: dam volume from a survey, evaporation and seepage losses, roof-runoff tank sizing and monthly draw-down tracking."
sources: ["FAO Water harvesting manuals (e.g. Critchley & Siegert, 1991)", "State agriculture department farm dam and stock water budgeting guides (e.g. NSW DPI, Agriculture Victoria)", "https://www.fao.org/4/x0490e/x0490e08.htm"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Farm dam and tank water budget

**Goal:** know how many usable litres you have, how fast they disappear, and how many
days of demand they cover — so you destock, cart water or cut irrigation *before* the
dam is mud.

## 1. Measure what's in storage
**Tanks:** volume = area of base × water depth. Round tank: `V (L) = π × r² × h × 1000`
(r, h in metres). A 3.6 m diameter tank with 1.8 m of water: π × 1.8² × 1.8 × 1000 ≈ 18,300 L (recomputed 18,322).
Mark a dipstick or fit a gauge in 10% steps.

**Dams:** the shape is rarely regular. Options, best first:
1. Survey once when low or empty (GPS/levels, or drone photogrammetry) → build a
   depth-to-volume table.
2. Prismoidal approximation for a roughly rectangular dug dam:
   `V ≈ (D/6) × (A_top + 4 × A_mid + A_bottom)` with D = water depth, areas at the
   current water surface, half depth and floor (checked exactly against a square frustum, 20 m top, 10 m floor, 2 m deep: 466.7 m³ both ways).
3. Rough rule for irregular excavated dams: `V ≈ 0.4 × surface area × max depth`
   (estimate only; the 0.4 factor and the ±30% error are not confirmed (gated: unconfirmed, source is paywalled or blocked)).
Install a **staff gauge** (graduated post) in the deepest part and read it on the same
day each week; convert with your depth–volume table.

**Usable** volume is less than total: allow for **dead storage** (bottom ~0.3–0.5 m is
often too muddy or too low to pump/draw cleanly).

## 2. Losses
- **Evaporation:** roughly 0.7-0.8 × pan evaporation (Class A pan figures from your
  met service; the factor is local practice (gated: unconfirmed, source is paywalled or blocked). FAO-56 Table 5 pan coefficients of 0.35-0.85 apply to reference crop ET, ETo = Kp × Epan, not to open water). In a hot dry summer, 6–10 mm/day off the surface is common — on a
  0.5 ha dam that is 30-50 m³ (30,000-50,000 L) a day (recomputed), often more than stock drink.
  Shallow, wide dams lose the largest share; deep, narrow ones last longer.
- **Seepage:** measure by comparing the staff gauge fall over a week with no inflow
  or draw against the expected evaporation. A difference of more than a few mm/day
  suggests leakage (dispersive soils, poor compaction, yabby/crayfish burrows).

## 3. Demand
List every draw in litres/day: stock (see
agriculture-environment.irrigation-water-management.stock-water-systems.stock-water-reticulation-and-trough-checks
for per-head figures), household, spraying, irrigation. Increase stock figures in hot
weather — they can double.

## 4. The budget
Monthly table (or spreadsheet):
```
Usable_end = Usable_start + inflow − evaporation − seepage − demand
Days_left = Usable_now ÷ (daily demand + daily losses)
```
Set **trigger points** in advance, e.g. "at 90 days left, sell X; at 60 days, start
carting or move stock". Recheck after every rain event.

## 5. Harvesting: sizing roof and catchment supply
**Roof runoff:** `Yield (L) = roof area (m²) × rainfall (mm) × runoff coefficient`.
Metal roofs ~0.8–0.9 after first-flush and gutter losses. A 200 m² shed in a
500 mm/year district: 200 × 500 × 0.85 ≈ 85,000 L/year (recomputed). The 0.8-0.9 coefficient is a typical figure (gated: unconfirmed, source is paywalled or blocked). Size the tank to carry you
through the longest typical dry gap: monthly rainfall × yield vs monthly demand;
storage must cover the cumulative deficit. Fit **first-flush diverters**, leaf guards
and mosquito-proof screens.

**Dam catchment:** runoff coefficient varies wildly — cropped or bare ground in an
intense storm may run 20–40%, deep well-grassed soils in light rain close to 0. Local
"runoff per ha" guides from your agriculture department are better than any national
figure.

## 6. Keep it usable
- Fence the dam and pump to troughs: stock wading fouls water and damages batters.
- Watch for **blue-green algae** (cyanobacteria) in warm, nutrient-rich, still water —
  green paint-like scums. Toxic blooms kill stock; stop access and test before use.
- Keep spillways clear and grassed; check walls for cracks, slumps, wet patches and
  trees growing on the bank. Larger dams may be regulated (dam safety and water-take
  licensing) — check local rules before building or enlarging.

## Gotchas
- Staff gauge readings lie if the post moves; set it in concrete or on a stable pipe.
- "Full" dams often aren't — measure after the dry season, not once at fill.
- Figures above are illustrative ranges, **not site-tested**; use local pan
  evaporation and runoff guides.

## Verify
- [ ] Depth–volume table exists for each dam; usable volume excludes dead storage.
- [ ] Weekly gauge readings logged and converted to litres.
- [ ] Losses estimated from evaporation data and checked against gauge fall.
- [ ] Days-of-water figure calculated with trigger actions written down.
- [ ] Water checked for algae and access fenced.
