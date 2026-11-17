---
id: manufacturing-production.chemical-process-manufacturing.distillation-separation-operation.column-flooding-weeping-and-composition-control
name: column-flooding-weeping-and-composition-control
category: manufacturing-production
field: chemical-process-manufacturing
product: distillation-separation-operation
tags: [distillation-separation-operation, distillation, distillation-column, fractionation, column-operation, flooding, weeping, entrainment, foaming, differential-pressure, column-dp, reflux, reflux-ratio, reboiler, boilup, condenser, tray-temperature, sensitive-tray, composition-control, overhead, bottoms, energy-balance, crystallisation, filtration, separation, chemical-plant, refinery]
level: practitioner
status: draft
description: "Operate a distillation column: hold composition with tray temperature, read differential pressure for flooding and weeping, respond correctly to each, and balance reflux against energy use."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Distillation column operation: flooding, weeping and composition control

**Goal:** keep top and bottom products on spec with the least energy, and recognise
and correct hydraulic problems (flooding, weeping, foaming) before they wreck the
separation.

For design-side methods (Fenske–Underwood–Gilliland, tray sizing) see
engineering-technology.chemical-engineering.separation-processes.distillation-column-shortcut-design.
This skill is the operator's view.

## 1. What you control and what it does
- **Feed rate and condition** (temperature/vapour fraction) — set by upstream.
- **Reboiler duty (boilup)** — the vapour traffic up the column.
- **Reflux** — the liquid traffic down the top section.
- **Distillate and bottoms draws** — normally on level or as the composition handle.
- **Column pressure** — via condenser duty or vent/inerts; changes every boiling point.
Rule of thumb: **more reflux and boilup = better separation, more energy, more
hydraulic load.** You are always trading purity against energy against capacity.

## 2. Composition control by temperature
Online analysers are slow and fail; most columns control a **sensitive tray
temperature** — the tray where temperature changes most per unit composition change
(often a few trays from the feed in each section, found from step tests or design).
- Tray temperature depends on pressure: if pressure moves, temperature moves with no
  composition change. Good schemes use **pressure-compensated temperature**; if yours
  does not, hold pressure steady first.
- Use the analyser (or lab) to **trim** the temperature setpoint, not to fight it.
- **Mass balance beats energy:** if too much material leaves the top relative to the
  feed's light content, the top goes off spec however much reflux you add. Check
  distillate/feed ratio against feed composition before cranking reflux.

## 3. Reading hydraulics: differential pressure (ΔP)
Column (or section) ΔP is the best hydraulic indicator. Trend it with boilup.
- **Flooding:** liquid cannot drain against the vapour; liquid accumulates and is
  carried up. Signs: ΔP rising sharply (non-linearly) with small boilup increase,
  reflux drum level falling or erratic, bottoms level falling, heavy components
  appearing overhead, tray temperatures flattening.
  **Response:** cut boilup (and reflux with it) until ΔP drops back to its normal
  curve; then come back up more slowly. Check feed rate and feed temperature (a cold
  feed adds liquid load). If flooding occurs at lower rates than before, suspect
  fouling, damaged trays or foaming.
- **Foaming:** looks like flooding at loads that should be fine, often after a feed
  change or contamination. ΔP can be erratic. Antifoam use, if any, is per site
  procedure.
- **Weeping/dumping:** too little vapour; liquid drains through tray holes. Signs: low
  ΔP, poor separation despite reflux, unstable tray temperatures, often at low rates.
  **Response:** increase boilup to the minimum for good tray action; at turndown accept
  recycle or extra reflux rather than starving vapour.
- **Entrainment** (mild, below flood): rising heavies overhead with high but steady ΔP.

## 4. Energy balance sanity check
Reboiler duty ≈ condenser duty + heat out with products − heat in with feed (minus
losses). If the condenser is maxed out (cooling water at max, pressure rising), you
cannot boil more — the condenser is your constraint, not the reboiler.

## 5. Other separations, briefly
- **Crystallisers:** control cooling rate and seeding; crash cooling gives fines that
  blind filters. Watch for encrustation on cooled surfaces (falling heat transfer).
- **Filtration:** track cycle time and ΔP across the filter; a rising ΔP that builds
  faster each cycle signals fines or cloth blinding — investigate upstream crystal size
  before changing cloths.

## Gotchas
- A falling reflux drum level during flood tempts operators to cut distillate — the
  real fix is to cut vapour.
- Inerts in the condenser raise pressure and cut condenser capacity; vent them.
- Changing two handles at once (reflux and boilup) on a slow column makes it impossible
  to see which did what.

## Verify
- [ ] Sensitive tray identified and pressure effect accounted for.
- [ ] Distillate/feed ratio consistent with feed composition.
- [ ] ΔP trended against boilup; normal curve known so departures stand out.
- [ ] Flooding answered by cutting vapour, weeping by raising it.
- [ ] Energy per unit product tracked; reflux not higher than spec requires.

*Draft note:* general operating practice; column-specific limits come from vendor
hydraulic ratings and plant tests.
