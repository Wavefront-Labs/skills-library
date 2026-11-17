---
id: repair-maintenance.automotive-repair.transmission-drivetrain-repair.clutch-replacement-and-automatic-fluid-diagnosis
name: clutch-replacement-and-automatic-fluid-diagnosis
category: repair-maintenance
field: automotive-repair
product: transmission-drivetrain-repair
tags: [automotive-repair, transmission-drivetrain-repair, clutch, clutch-replacement, flywheel, dual-mass-flywheel, dmf, release-bearing, concentric-slave-cylinder, alignment-tool, automatic-transmission, atf, fluid-level-check, cvt, dct, slipping, shift-flare, cv-axle, cv-joint, differential, gear-oil, transmission-adaptations, solenoids]
level: practitioner
status: draft
description: "Diagnose and replace a manual clutch (slip test, DMF check, alignment, bedding in) and triage automatic/CVT complaints through correct fluid-level checks, scan data and CV/driveline noises."
sources: ["LuK/Schaeffler and Sachs clutch installation and DMF inspection guides (general practice)", "Manufacturer ATF check procedures (temperature-dependent level checks)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Clutch replacement and automatic fluid diagnosis

**Goal:** confirm a driveline fault before a costly gearbox job, and do the commonest
manual-transmission job, the clutch, correctly first time. Gearbox internal rebuilds are
specialist work; most "transmission" complaints turn out to be fluid, software, mounts,
CV joints or the clutch.

## 1. Manual clutch: confirm the diagnosis
- **Slip test:** warm engine, 3rd or 4th gear at ~ 30–50 km/h, full throttle: rpm rising
  without matching road-speed increase = slipping. (Or handbrake test at standstill —
  harsh on components; avoid.)
- **Drag (won't disengage, crunchy gear selection):** hydraulics first — fluid level, air in
  the system, leaking master/slave cylinder (concentric slave cylinders leak inside the
  bell housing: look for fluid at the bell housing drain hole).
- **Judder on take-off:** oil-contaminated friction disc (rear main seal or gearbox input
  seal leak), worn DMF, engine/gearbox mounts.
- **Noise:** whir with pedal down = release bearing; rattle at idle that stops with pedal
  down = input shaft bearing or DMF.

## 2. Clutch replacement (front-wheel-drive transverse, general)
1. Battery disconnected; car on a lift or quality stands; drain gearbox oil if the axles
   must come out of the differential (some designs require it).
2. Remove driveshafts/CV axles, starter, gearbox mounts, linkage/cables, hydraulic line
   (clamp the hose), sensors; support the engine and gearbox (transmission jack).
3. Separate the gearbox squarely — don't let its weight hang on the input shaft (bends
   the disc hub).
4. Inspect:
   - **Dual-mass flywheel (DMF):** free play and rock against the manufacturer limits
     (often with a gauge — measured in degrees or teeth of movement). Worn DMF = replace
     with the clutch kit, never re-use beyond limits.
   - Solid flywheel: heat spots/cracks; resurfacing must remove the same amount from the
     step on stepped flywheels.
   - Rear main seal and gearbox input seal for oil leaks.
5. Fit new disc (note "flywheel side" marking) with an **alignment tool**; tighten
   pressure-plate bolts evenly in a crisscross in stages to torque.
6. Replace the release bearing (and concentric slave cylinder where fitted). Lightly
   grease the input shaft splines with the specified high-melting-point grease (thin film
   only) and the release fork pivot.
7. Refit the gearbox without forcing; use new axle circlips/seals as required; refill gear
   oil to spec; bleed the hydraulics.
8. Clutch bite point adaptation via scan tool on some models; bed in gently for the first
   few hundred km (avoid hard launches and riding the clutch).

## 3. Automatic and CVT complaints: start with fluid and data
1. **Fluid level, done correctly:** many modern automatics have no dipstick; the level is
   checked at a **specified fluid temperature** (e.g. 35–45 °C, read on a scan tool) with the
   engine running, by removing a fill/check plug until fluid drips. Wrong temperature =
   wrong level by a large margin.
2. **Fluid type:** exact OEM spec (e.g. Dexron VI, Mercon LV, Toyota WS, CVT NS-3, DCT
   specific). Wrong fluid causes shudder and clutch failure; "universal" fluids are a risk.
3. **Fluid condition:** burnt smell and black colour = overheated clutches; debris on the
   magnet in the pan is normal in small amounts (fine paste), not chunks.
4. **Scan data:** transmission DTCs, line pressure, solenoid commands, gear ratio
   errors, slip rpm per gear, fluid temperature. **Adaptations:** after fluid service or
   valve body/solenoid work, many units need a relearn/reset per the manufacturer.
5. Software updates (TSBs) commonly fix harsh shifts and flares.

## 4. Driveline noises
- Clicking on full-lock turns under power → **outer CV joint** (check boot torn, grease flung).
- Clunk on take-off → inner CV, mounts, or excess driveline lash.
- Vibration under acceleration that goes away on coast → inner CV (tripod) joint or propshaft angles.
- Whine changing with speed (not rpm) → differential or wheel bearing.

## Gotchas
- Don't press the clutch pedal with the slave cylinder removed (pops pistons out).
- Overfilling an automatic causes foaming and slipping, as does underfilling.
- Uncertain: fluid-check temperatures and DMF limits vary per model; use the manual.

## Verify
- [ ] Slip/drag/judder cause confirmed (hydraulics, oil contamination, DMF) before teardown.
- [ ] DMF measured against limits; disc aligned, pressure plate torqued evenly.
- [ ] Gear oil refilled to spec; clutch hydraulics bled; adaptation done if required.
- [ ] Automatic fluid level checked at specified temperature with correct fluid.
- [ ] Road test: no slip, judder, flare or driveline noise.
