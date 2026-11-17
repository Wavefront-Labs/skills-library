---
id: energy-mining-utilities.waste-management-recycling.incineration-energy-from-waste.grate-combustion-control-and-flue-gas-treatment
name: grate-combustion-control-and-flue-gas-treatment
category: energy-mining-utilities
field: waste-management-recycling
product: incineration-energy-from-waste
tags: [incineration-energy-from-waste, efw, energy-from-waste, waste-to-energy, wte, incinerator, mass-burn, moving-grate, bunker-crane, waste-mixing, calorific-value, primary-air, secondary-air, combustion-control, 850c-two-seconds, ied, industrial-emissions-directive, auxiliary-burner, carbon-monoxide, oxygen-trim, sncr, urea-injection, ammonia-slip, dry-scrubber, lime, sodium-bicarbonate, activated-carbon, bag-filter, cems, bottom-ash, apc-residue, loss-on-ignition]
level: advanced
status: draft
description: "Operate a moving-grate EfW line: mix the bunker for steady calorific value, trim feed and air to hold temperature and CO, run SNCR, scrubber and bag filter, and keep bottom ash burnt out."
sources:
  - "EU Industrial Emissions Directive 2010/75/EU, Chapter IV operating conditions (850 °C for 2 s; burnout limits), summarised; general grate-plant operating practice, paraphrased"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Grate combustion control and flue-gas treatment in an EfW plant

**Goal:** burn a variable fuel (mixed waste) steadily enough to hold legal combustion
conditions and emission limits, make steady steam, and produce well burnt-out ash.
Plant control systems vary (many lines run automatic combustion control); the operator
still sets it up for success and catches what it can't. Your permit and the plant's
operating instructions govern all limits.

## 1. The bunker is the first control loop
- Waste calorific value (CV) swings by load type: wet food waste vs dry
  commercial/plastics. Unmixed loads give temperature and steam swings and CO spikes.
- **Crane operator:** mix incoming waste in the bunker (lift, drop, re-stack), keep
  fresh deliveries away from the feed area until mixed, and feed from blended zones.
  Pull out bulky items, gas cylinders and anything that could jam the feed chute.
- Watch for **bunker fires** (thermal cameras, smell, smoke): water cannons/foam
  per procedure; don't feed a burning grab into the hopper without control-room agreement.

## 2. Combustion on the grate
- **Feed rate** (ram/feeder strokes) and **grate speed** set how much waste burns and
  how long it stays on the grate. Too fast → unburnt material in the ash; too slow →
  fire moves back toward the feed chute.
- **Primary (under-grate) air** zoned along the grate: drying, main burning, burnout.
  **Secondary air** above the grate mixes and completes combustion of gases.
- Operator targets typically include steam flow, furnace temperature and flue-gas
  oxygen (often several percent dry; plant-specific). Low O₂ with CO spikes =
  not enough air or a rich slug of waste; high O₂ and falling temperature = wet
  or low-CV waste.
- **Legal combustion condition (EU):** flue gas must reach **at least 850 °C for
  at least 2 seconds** after the last combustion air injection (1100 °C if waste
  contains >1% halogenated organics as chlorine). **Auxiliary burners** must cut in
  automatically if temperature drops below this, and waste feed must stop if it
  can't be maintained, including during start-up and shutdown. Other jurisdictions
  have similar rules; check yours.

## 3. Flue-gas treatment
Typical train (configurations vary):
1. **SNCR:** urea or ammonia sprayed in the furnace temperature window to cut NOx.
   Too much reagent → **ammonia slip** (emission and fouling); too little → NOx
   excursion. Injection level must follow where the temperature window actually is.
2. **Acid-gas removal:** lime or sodium bicarbonate dosed to neutralise HCl and SO₂;
   dose trimmed on outlet HCl/SO₂ readings.
3. **Activated carbon** for mercury and dioxins/furans; keep the dosing feeder
   reliable, as a blocked feeder isn't seen by the HCl analyser.
4. **Bag filter:** watch differential pressure; a sudden fall can mean a burst bag,
   a rise means blinding or poor cleaning. Keep flue gas above acid dew point to
   avoid corrosion and wet cake.
- **CEMS** (continuous emissions monitors): treat a drifting or failed analyser as
  urgent — you can't show compliance without valid data. Log abnormal operation.

## 4. Ash
- **Bottom ash** should be well burnt out (EU limit: TOC < 3% or loss on ignition
  < 5%). Sample per permit; unburnt material points back to grate speed/air.
- Metals are recovered downstream (magnets, eddy-current). **APC residue**
  (filter ash) is hazardous waste: handle in closed systems, separately.

## 5. Abnormal events
Feed blockage, grate fire behind the feed, boiler tube leak (rising make-up water,
steam plume, falling drum level), ID fan trip. Know which trip the line
automatically and which you must act on, and the shutdown sequence that keeps
temperature compliance until waste on the grate has burnt out.

## Verify
- [ ] Bunker mixed; feeding only from blended waste; bulky items removed.
- [ ] 850 °C / 2 s (or local rule) maintained; burners auto-start tested.
- [ ] O₂, CO and steam stable; feed, grate speed and air trimmed to them.
- [ ] Reagent dosing tracking NOx, HCl, SO₂; ammonia slip in range; carbon feeder working.
- [ ] Bag-filter dP normal; CEMS valid; bottom-ash burnout sampled.
