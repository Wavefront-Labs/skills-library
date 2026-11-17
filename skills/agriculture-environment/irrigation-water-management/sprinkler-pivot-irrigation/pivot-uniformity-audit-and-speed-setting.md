---
id: agriculture-environment.irrigation-water-management.sprinkler-pivot-irrigation.pivot-uniformity-audit-and-speed-setting
name: pivot-uniformity-audit-and-speed-setting
category: agriculture-environment
field: irrigation-water-management
product: sprinkler-pivot-irrigation
tags: [sprinkler-pivot-irrigation, centre-pivot, center-pivot, lateral-move, linear-move, sprinkler-irrigation, catch-can-test, uniformity, christiansen-uniformity, cu, cuh, heermann-hein, distribution-uniformity, du, nozzle-package, sprinkler-chart, percent-timer, pivot-speed, application-depth, end-gun, pressure-regulator, runoff, wheel-tracks, system-audit]
level: practitioner
status: gated
description: "Audit a centre pivot with a catch-can test, compute CU and DU, then set percent-timer speed for a target depth and spot nozzle-package faults."
sources: ["https://www.asabe.org/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pivot uniformity audit and speed setting

**Goal:** know what depth your pivot really applies at each speed setting and how
evenly, so the schedule's "25 mm" is 25 mm across the whole circle.

## 1. Speed vs depth: the arithmetic
A pivot's percent timer sets how much of each minute the end tower moves (e.g. 50% =
30 s moving, 30 s stopped). Depth is inversely proportional to speed:
```
Depth (mm) = depth at 100% ÷ (percent setting / 100)
Depth at 100% (mm) = 0.36 × Q × T100 / A      # Q in L/s, T100 = full-circle hours at 100%, A in ha
```
Simpler in practice: read the dealer's **sprinkler chart** — it gives system flow
(L/s or gpm) and design pressure for the nozzle package — and the hours per revolution
at 100%. Example: 50 ha circle, 60 L/s, 20 h/rev at 100%:
`60 L/s × 20 h × 3600 s = 4.32 ML = 4,320 m³ ÷ 500,000 m² = 8.6 mm` at 100%.
At 50% → 17.3 mm; at 25% → 34.6 mm. Make a laminated card of this for the panel.

**Check the real speed:** time the end tower over a measured distance (e.g. between two
pegs 30 m apart) at 100% — wheel slip and worn tyres make it slower than the brochure.

## 2. Catch-can test (simplified ASABE S436.1 style)
Equipment: 50–100 identical cans or rain gauges with straight sides, stakes, a
measuring cylinder, data sheet, wind meter.
1. Lay **two radial lines** of cans from the pivot point to beyond the end, spaced
   **3 m (10 ft)** or less apart (gated: unconfirmed, source is paywalled or blocked), rims level and above any crop canopy. Skip the first
   ~10% of radius if you must (small area) but note it.
2. Run the machine at a normal setting over the cans, in **wind < ~4.5 m/s (10 mph)** (gated: unconfirmed, source is paywalled or blocked),
   preferably early morning to cut evaporation. Read pressure at the pivot point and
   at the last tower.
3. Measure each can promptly (mL → mm using the can opening area).

## 3. Calculate uniformity
Because outer cans represent more area, the pivot formula weights each can by its
distance from the centre (Heermann-Hein CU):
```
CUh = 100 × [1 − Σ(Si × |Vi − Vw|) / Σ(Si × Vi)]
Vw = Σ(Si × Vi) / Σ Si        # Si = distance of can i from pivot, Vi = catch depth
```
Also compute a rough **DU (low quarter)** = mean of lowest 25% ÷ overall mean.
Rough interpretation: CUh ≥ 90% good for a modern low-pressure package; 85–90% fair (gated: unconfirmed, source is paywalled or blocked);
< 85% find the cause. Compare the overall mean against the depth from section 1 —
a big shortfall means leaks, wrong nozzles, low flow or evaporation/drift losses.

## 4. Reading the pattern
Plot catch depth vs distance; the shape tells you what's wrong.
- **One low spike at a single position** → blocked or missing nozzle, wrong nozzle
  size installed there (check against the chart, position by position).
- **Steadily low towards the end** → pressure too low (pump wear, wrong regulator
  rating, end-of-line pressure < regulator rating + ~35 kPa (gated: unconfirmed, source is paywalled or blocked)), or worn pump.
- **Wet near the centre, dry outer spans** → nozzle package doesn't match current flow.
- **Saw-tooth pattern** → sprinkler spacing too wide for the drop height, or
  regulators failing (weak ones stick).
- **End gun zone way off** → end gun arc/timing or booster pump issue.

## 5. Runoff check
Low-pressure spray nozzles apply at high instantaneous rates at the outer spans. If
you see ponding or runoff on the outer third, either **speed up** (lighter, more frequent
passes), add tillage pits/basins or boom-backs, or change to nozzles with a wider wetted
diameter. Deep wheel ruts are a sign of the same thing.

## Gotchas
- A pivot running at 5% to "catch up" puts on huge single doses that often run off;
  better to start earlier.
- Regulators wear out; a set of regulators 8–10+ years old (gated: unconfirmed, source is paywalled or blocked) is a usual suspect
  (rule of thumb, unconfirmed for any brand).
- Cans under crop canopy, tilted cans, or dew/evaporation errors bias results — repeat
  if wind was gusty.
- Formula above is the standard Heermann-Hein form (gated: unconfirmed, source is paywalled or blocked); the full S436.1 procedure has more
  requirements (can spacing, test conditions) than this field version.

## Verify
- [ ] Panel card shows mm applied at each % setting, based on measured flow and speed.
- [ ] Catch-can data plotted against distance; CUh and DU calculated.
- [ ] End-of-line pressure ≥ regulator rating + margin.
- [ ] Any low position matched to a nozzle checked against the sprinkler chart.
- [ ] No visible runoff at the normal operating speed.

## Checked

- Date: 2026-10-25. Jurisdiction: no regulation involved; ASABE S436.1 is the governing test procedure.
- Confirmed against: the depth arithmetic was recomputed (depth at 100% = 0.36 x Q x T / A, 60 L/s x 20 h on 50 ha = 8.6 mm; 17.3 mm at 50%); 3 m = 10 ft and 4.5 m/s = 10 mph.
- Not confirmed: the can spacing, wind limit, CUh bands, regulator age and end-pressure margin, and the Heermann-Hein attribution (the ASABE standard is paywalled).

Method: documentation only; no commands were run.
