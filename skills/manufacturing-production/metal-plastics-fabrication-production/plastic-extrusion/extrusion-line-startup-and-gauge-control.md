---
id: manufacturing-production.metal-plastics-fabrication-production.plastic-extrusion.extrusion-line-startup-and-gauge-control
name: extrusion-line-startup-and-gauge-control
category: manufacturing-production
field: metal-plastics-fabrication-production
product: plastic-extrusion
tags: [plastic-extrusion, extrusion, extruder, single-screw, twin-screw, pipe-extrusion, profile-extrusion, sheet-extrusion, film-extrusion, blown-film, cast-film, die, melt-pressure, melt-temperature, screen-changer, breaker-plate, haul-off, puller, vacuum-sizing, calibrator, gauge-control, wall-thickness, ultrasonic-gauge, beta-gauge, surging, die-lines, startup-scrap, purge, pvc, hdpe, pp]
level: practitioner
status: draft
description: "Start up an extrusion line with less scrap and hold gauge: heat soak, safe screw start, melt pressure and temperature watch, haul-off and sizing set-up, and diagnosing surging and die lines."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Extrusion line startup and gauge control

**Goal:** go from cold line to in-spec product quickly and safely, then keep wall
thickness/gauge steady. Startup is where most extrusion scrap is made, and over-pressure
at startup is the classic way to blow a rupture disc or damage a die.

## 1. Before heating
- Correct die, tooling (mandrel/pin for pipe, die lips for sheet/film), screen pack,
  breaker plate and sizing/calibration sleeve for the product.
- Material dried if hygroscopic (PET, PA, PC); for PVC, the compound and stabiliser
  package confirmed — degraded PVC releases HCl and is a safety issue.
- Rupture disc / melt-pressure alarm and interlock functional.

## 2. Heat soak
Bring barrel, adapter and die to setpoint and **hold (soak)** long enough that the
whole mass of the die is at temperature — a die that reads setpoint at the thermocouple
can still be cold inside. Soak time is per the line's procedure (often an hour or more
for big dies; confirm). Starting the screw on cold material is how screws and
gearboxes get damaged.

## 3. Starting the screw
1. Start at **low RPM**; watch **melt pressure** (before screen and at the die) and
   motor load. Pressure should rise gradually — a spike means frozen material
   somewhere: stop and wait.
2. Purge until the melt is clean and consistent (no degraded/discoloured material
   from the last run).
3. Thread the extrudate to the haul-off (puller) through sizing/cooling; increase screw
   speed and haul-off speed together in steps.

## 4. Getting to spec
- **Gauge/wall thickness = output ÷ line speed.** Increase screw RPM → thicker;
  increase haul-off speed → thinner. Make the gross correction with the haul-off/RPM
  ratio, then centre with die adjustment (pipe die centring bolts, sheet die lip bolts).
- **Pipe/profile**: vacuum sizing tank level and vacuum, water temperature, then check
  wall thickness around the circumference (ultrasonic gauge) and ovality.
- **Sheet/film**: thickness profile across the width (beta/X-ray gauges, automatic
  die-bolt control). Don't chase every bolt manually at once — adjust a few,
  wait for the change to travel through.
- Record the settings once stable and compare to the last good run sheet.

## 5. Watch items in production
| Symptom | Likely cause |
|---|---|
| **Surging** (periodic thickness/pressure cycle) | Feed problems (bridging in hopper, regrind ratio), screw speed/temperature profile, worn screw/barrel |
| Pressure rising slowly over hours | Screen pack blinding — change screens (screen changer) |
| **Die lines** | Degraded material or contamination hung up in die, die lip damage |
| Bubbles/voids | Moisture, volatiles, insufficient back pressure |
| Rough/sharkskin surface | Melt fracture — too high output for die gap/temperature |
| Ovality / poor sizing | Vacuum, water flow/temperature, haul-off pressure on soft pipe |
| Off-centre walls (pipe) | Die centring, uneven cooling, sag in large pipe (compensate per method) |

## 6. Shutdown
Purge with a stable material or purge compound if leaving heat on, especially after
PVC or other heat-sensitive materials. Leaving degradable material sitting hot in the
die is the next startup's die lines.

## Gotchas
- Never stand in front of the die at startup — pressure release can eject melt.
- A melt-pressure sensor reading zero while the motor load climbs: suspect a failed
  sensor, not "no pressure".
- Haul-off belt slippage gives thickness variation that looks like surging; check
  belt pressure and wear.

## Verify
- [ ] Heat soak completed; pressure rose smoothly at low RPM.
- [ ] Wall/gauge measured around/ across product within spec.
- [ ] Settings recorded and compared to the reference run sheet.
- [ ] Melt pressure and screen-pack differential trended during the run.

*Draft: soak times and temperature profiles are material- and line-specific; covers
pipe/profile/sheet in general terms.*
