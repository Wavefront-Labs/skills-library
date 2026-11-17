---
id: manufacturing-production.metal-plastics-fabrication-production.thermoforming.sheet-heating-and-plug-assist-setup
name: sheet-heating-and-plug-assist-setup
category: manufacturing-production
field: metal-plastics-fabrication-production
product: thermoforming
tags: [thermoforming, vacuum-forming, pressure-forming, roll-fed-thermoforming, sheet-fed, heavy-gauge, thin-gauge, oven, heater-zones, ir-heaters, ceramic-heaters, quartz-heaters, sag, forming-window, plug-assist, syntactic-foam, material-distribution, wall-thickness, webbing, chill-marks, inline-trimming, trim-press, steel-rule-die, apet, rpet, pp, hips, abs, packaging, kiefel, illig, gn-thermoforming]
level: practitioner
status: draft
description: "Set heater zones and plug assist on a thermoformer to put material where the part needs it: read sag and sheet temperature, tune plug depth/timing, fix webbing and thin corners, and keep trim clean."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sheet heating and plug-assist setup

**Goal:** formed parts with enough wall in the corners and bottom (the thin spots in
almost every deep draw) at a stable cycle, then clean trimming. In thermoforming the
sheet only stretches once — wherever it's hottest and first touched last, it thins.

## 1. Know your forming window
Each material has a temperature range where it forms well: below it, the sheet
won't take detail and stresses; above it, it sags, webs or degrades. Get the range
from the sheet supplier (APET/RPET, PP, HIPS, PS, ABS, PC all differ, PP has a notably
**narrow** window). Measure the **actual sheet temperature** with an IR pyrometer or
line scanner at the exit of the oven — heater setpoints are not sheet temperatures.

## 2. Heater zones
- Ovens (ceramic, quartz, halogen) are divided into zones top and bottom. Map which
  zones heat which part of the sheet; usually more heat toward the **edges** because
  clamps/chains sink heat.
- **Cooler areas stretch less and stay thicker; hotter areas thin out.** Zoning can
  shift material a little, but the main tool for getting material into deep corners
  and bottoms is the plug (below).
- Watch **sag**: some sag is normal on sheet-fed; excess sag means overheated
  centre (reduce centre zones) and gives webbing and thin areas. Many roll-fed lines
  have sag/support controls.
- For thick sheet (heavy gauge), heat soak through the thickness matters — use
  lower power, longer cycles, and both sides; surface scorching with a cold core is the failure.
- Change zones in small steps and let the oven equilibrate a few cycles.

## 3. Plug assist
The plug pre-stretches sheet into the cavity before vacuum/pressure finishes the form.
- **Plug depth**: typically to most of the cavity depth (often quoted ~70–90 %,
  confirm per tool). Deeper → more material carried to the bottom.
- **Plug timing and speed**: plug moves before or with vacuum; fast plugs stretch
  sidewalls more evenly; vacuum too early pulls sheet off the plug prematurely.
- **Plug material and temperature**: syntactic foam plugs (low thermal conductivity)
  minimise chill marks; metal plugs need heating. A cold plug "freezes" the sheet
  where it touches → thick spots and chill marks.
- **Plug shape** and clearance to the cavity wall decide where sidewall thickness ends
  up; changing shape is a toolroom job.

## 4. Forming and cooling
Vacuum/pressure level and timing, mould temperature (temperature-controlled moulds
reduce warp and shrinkage variation), and cooling time before ejection. Pressure
forming gives sharper detail at higher cost.

## 5. Defect → first suspects
| Defect | Check |
|---|---|
| Thin corners/bottom | Plug depth/timing, sheet too hot there, plug too cold |
| **Webbing** (folds between cavities) | Overheating/sag, cavity spacing, missing web catchers/ring |
| Chill marks | Plug temperature/material, mould too cold |
| Incomplete detail | Sheet too cold, vacuum leak/blocked holes, too slow vacuum |
| Blisters/bubbles | Moisture in sheet (PC, PETG, ABS) — dry first, or overheating |
| Warp | Uneven cooling, demould too hot, uneven sheet temperature |

## 6. Inline trimming
Steel-rule or matched-metal trim dies: check registration of trim to the formed part
(index/position drift as sheet shrinks), knife sharpness and **angel hair**/fines on
PET. Skeleton (scrap web) handling must not jam.

## Verify
- [ ] Measured sheet temperature inside the material's forming window.
- [ ] Wall thickness at corners/bottom above minimum on sampled parts from each cavity.
- [ ] No webbing or chill marks; trim registration and edge quality in spec.
- [ ] Settings recorded with sheet lot and gauge.

*Draft: plug depth percentages and windows are rules of thumb; sheet supplier data and
tool designer guidance take precedence.*
