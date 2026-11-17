---
id: repair-maintenance.appliance-repair.laundry-appliance-repair.washer-wont-drain-or-spin-and-dryer-no-heat
name: washer-wont-drain-or-spin-and-dryer-no-heat
category: repair-maintenance
field: appliance-repair
product: laundry-appliance-repair
tags: [appliance-repair, laundry-appliance-repair, washing-machine, washer, dryer, tumble-dryer, drain-pump, pump-filter, lid-switch, door-lock, shock-absorbers, drum-bearings, unbalanced-load, heating-element, thermal-fuse, thermal-cutoff, high-limit-thermostat, dryer-vent, lint, multimeter, diagnostic-mode, error-codes, whirlpool, samsung, lg, bosch]
level: practitioner
status: docs-checked
description: "Diagnose a washer that won't drain or spin (filter, pump, lid lock, balance) and a dryer that tumbles but won't heat (vent, thermal fuse, element, thermostats)."
sources: ["https://www.usfa.fema.gov/downloads/pdf/publications/clothes_dryer_fire_safety_flyer.pdf", "https://www.energy.gov/sites/prod/files/2016/06/f32/NFPA_DryerWasherSafetyTips.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Washer won't drain/spin, dryer won't heat

**Goal:** find the failed part for the two most common laundry
complaints, using the machine's own tech sheet, a multimeter and logic. Always unplug
before opening; on gas dryers, also see the gas-appliance skill
(`repair-maintenance.appliance-repair.gas-appliance-service.combustion-and-leak-testing-gas-appliances`).

## Before anything: the tech sheet and error code
- Most machines have a **tech sheet** (wiring diagram, component resistances, service
  mode entry sequence) taped inside the console, behind the kickplate, or under the top.
- Read the displayed **error code** and look it up for that brand/model; many machines
  have a service/diagnostic mode (button sequence on the tech sheet) that runs the pump,
  motor and valves one at a time — the fastest way to localise a fault.

## 1. Washer won't drain or won't spin
Spin is blocked by the control if water is still in the drum, so a drain fault often
shows as "won't spin".
1. **Drain filter/coin trap** (front loaders: behind a small door at bottom front). Put
   towels and a low tray down; open slowly — it releases a lot of water. Remove socks,
   coins, hair pins. This fixes a large share of front-loader drain complaints.
2. **Drain hose:** kinked, crushed behind the machine, or pushed too far down the
   standpipe. Follow the maker's hose height and insertion limits so it cannot siphon or block.
3. **Drain pump test:** in service mode, run the pump; listen for hum.
   - Hums but no water moves → impeller jammed or broken; remove pump and check.
   - Silent → measure pump coil resistance against the tech sheet value. Open circuit = failed pump. Good coil but no voltage at the pump during drain
     → wiring or control board.
4. **Won't spin with an empty drum:**
   - Top-loaders: **lid switch / lid lock** — test continuity with the lid closed; a
     broken actuator tab on the lid is common.
   - Front-loaders: **door lock** must lock and confirm; test the lock switch and listen
     for the click.
   - **Unbalanced load** detection aborts spin: a single heavy item (bath mat, duvet)
     can't distribute. Retry with a balanced load before blaming the machine.
   - Belt (older machines) slipped/broken; motor brushes worn (commutator motors).
   - Drive-motor or inverter faults show as codes — follow the brand's flow chart.
5. **Noisy spin / roaring:** drum bearings. Rotate the empty drum by hand; grinding or
   play when you lift the drum = bearings (often a major job, sometimes uneconomic on
   sealed-tub designs). Banging = worn shock absorbers/suspension springs.

## 2. Dryer tumbles but no heat (electric)
1. **Vent first.** Disconnect the duct from the back; run the dryer: if it heats now,
   the duct is blocked. A restricted vent is the root cause of most thermal fuse failures
   — replacing the fuse without clearing the vent means it blows again (and it's a fire risk).
   Use rigid or flexible metal venting; lint should be cleaned out of the vent pipe once a year, or sooner if drying takes longer than normal (NFPA tip sheet). Check the outdoor vent flap opens when the dryer runs.
2. Check the supply: a tripped breaker or a missing supply leg can give "tumbles, no heat". Measure the supply voltage at the terminal block against the data plate.
3. Unplug, then test with the meter (resistance mode), components disconnected:
   - **Thermal fuse/thermal cutoff:** continuity = good; open = blown.
   - **Heating element:** resistance per the tech sheet;
     open = broken coil (often visible). Also check it isn't shorted to the housing.
   - **High-limit thermostat** and **cycling thermostat:** closed at room temperature.
4. Gas dryer, no heat: igniter glows? Glows but no flame → gas valve coils; no glow →
   igniter (very fragile — don't touch the element) or flame sensor.

## Gotchas
- Capacitors in inverter boards can hold charge; wait and don't probe boards live.
- Front-loader door boot mould and drain smells are separate issues (clean the filter
  and run a hot maintenance wash).
- Resistance values come from the tech sheet for your model; none are given here.
- Never dry items that have contacted cooking oil, gasoline, paint thinner or alcohol; do not leave a dryer running when you leave home or go to bed; keep the area clear of anything that can burn.

## Checked
2026-11-01. Confirmed in the USFA Clothes Dryer Fire Safety flyer and the NFPA/DOE Clothes Dryer and Washing Machine Safety tip sheet: clean lint filter each cycle, check the vent is not crushed or restricted, outdoor flap opens, yearly vent-pipe cleaning, rigid or flexible metal venting, professional gas-dryer inspection, never dry items with flammable substances. Removed: the 15 cm / 6 in standpipe depth, ohm ranges, 240 V figure, 30-minute goal. Tech-sheet and multimeter procedure is general practice, not a cited claim.
Method: documentation only; no commands were run.

## Verify
- [ ] Error code and tech sheet consulted; service mode used to isolate the part.
- [ ] Washer: filter cleared, hose not kinked/siphoning, pump and lock tested.
- [ ] Dryer: vent airflow confirmed before replacing any fuse.
- [ ] Failed part confirmed by measurement, not guess; test run completes a full cycle.
