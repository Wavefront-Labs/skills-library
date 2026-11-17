---
id: repair-maintenance.heavy-equipment-industrial-machinery-repair.bearing-lubrication-maintenance.rolling-bearing-mounting-removal-and-regreasing
name: rolling-bearing-mounting-removal-and-regreasing
category: repair-maintenance
field: heavy-equipment-industrial-machinery-repair
product: bearing-lubrication-maintenance
tags: [bearing-lubrication-maintenance, rolling-bearings, bearing-fitting, bearing-removal, induction-heater, bearing-puller, hydraulic-nut, oil-injection, tapered-bore, adapter-sleeve, radial-internal-clearance, feeler-gauge, drive-up-method, interference-fit, regreasing, grease-quantity, relubrication-interval, grease-compatibility, nlgi-2, lithium-complex, polyurea, ultrasonic-greasing, spalling, brinelling, fluting, skf, timken]
level: practitioner
status: draft
description: "Fit and remove rolling bearings with induction heaters, pullers and hydraulic nuts, set tapered-bore clearance, calculate regrease quantity and interval, and read failure marks."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rolling bearings: fitting, removal and regreasing

**Goal:** get a bearing onto and off a shaft without damaging it, set clearance on
tapered seats, grease it the right amount at the right interval, and read a failed
bearing for the cause. For whole-machine oil programmes see
`repair-maintenance.reliability-engineering-failure-analysis.oil-analysis.oil-sampling-and-interpreting-lab-results`.

## 1. Before fitting
- Lockout the machine. Clean the work area — a grain of grit in a bearing is a
  pre-made spall.
- Measure the shaft and housing seats with micrometers at two positions and two
  angles; compare to the fit on the drawing (e.g. shaft k5/m5, housing H7 for typical
  rotating-shaft loads). Out-of-round or worn seats must be repaired, not loctited.
- Leave the bearing in its wrapping until use; the preservative is compatible with
  most greases and oils.

## 2. Mounting
- **Never transmit force through the rolling elements.** Push only on the ring with
  the interference fit (inner ring on a shaft fit).
- **Small bearings, cold**: fitting tool kit (impact sleeve and ring) and a dead-blow
  hammer. Never hit the bearing directly with a steel hammer.
- **Hot mounting**: induction heater with temperature probe and auto-demagnetising.
  Heat to roughly 80–90 °C above shaft temperature, never over about 120 °C (125 °C
  absolute for standard bearings) — it softens the steel and damages seals/grease
  in sealed bearings. No open flame. Wear heat-resistant gloves and push home
  in one motion; hold it against the shoulder until it grips as it cools.
- **Tapered bore on adapter sleeve or tapered shaft**: drive up with a hydraulic nut
  and measure either the reduction in radial internal clearance with feeler gauges
  (spherical roller bearings, between the outer ring and unloaded rollers) or the
  axial drive-up distance from the maker's table or app. (Draft note: values depend on
  bearing series and size — use the manufacturer's table, e.g. SKF Drive-up Method.)
  Then lock the nut and tab washer.

## 3. Removal
- Use a puller on the ring with the tight fit (three-jaw or a backing plate behind the
  inner ring), or a hydraulic puller for large sizes.
- Large tapered-seat bearings: **oil injection** through the shaft ducts to expand the
  ring, with the nut left on a few threads as a stop — the bearing releases suddenly
  and can fly off.
- Induction heaters with removal attachments work on cylindrical roller inner rings.
- Keep a removed bearing for failure analysis; don't wash away evidence before looking.

## 4. Lubrication — quantity and interval
- **Initial fill**: open bearings ~30–50% of the free space in the bearing; housing
  partly filled. Overfilling causes heat from churning.
- **Regrease quantity** (common rule): G = 0.005 × D × B, grams, with D = outside
  diameter and B = width in mm. A 6316 bearing (170 × 39 mm) → about 33 g.
- **Interval**: from the maker's chart using speed factor (n × dm) and temperature;
  halve the interval for each 15 °C over 70 °C. Contaminated, wet or vertical shafts
  need shorter intervals.
- Know your grease gun's output: weigh 10 strokes on a scale — often 1–1.5 g per stroke.
- **Compatibility**: do not mix thickeners (lithium-complex, polyurea, calcium
  sulphonate, clay) without checking; incompatible mixes can soften and run out.
- Ultrasonic monitoring (listening to decibel drop as grease goes in) prevents
  overgreasing on critical motors.
- Electric motors with relief plugs: open the relief, grease, run 10–20 minutes, then
  refit the plug.

## 5. Reading failed bearings
- **Spalling** in the load zone: fatigue (end of life, overload or poor fit).
- **True brinelling** (dents at roller pitch): impact during mounting.
- **False brinelling**: vibration while stationary (transport, standby machines).
- **Fluting** (washboard pattern): electrical current through the bearing, often VFDs.
- **Blue/brown discolouration**: overheating — lack of lubricant or preload.
- **Fretting corrosion** on the bore or OD: seat too loose.

## Gotchas
- Mounting cold with a hammer on the outer ring to fit a shaft: instant brinelling.
- A sealed bearing must never be heated above its seal and grease limit.
- (Draft note: fits, heating limits and intervals here are typical; follow the bearing
  maker's catalogue for the specific bearing.)

## Verify
- [ ] Seats measured and within fit tolerance before mounting.
- [ ] Bearing heated within limits or cold-mounted only through the tight ring.
- [ ] Tapered-bore clearance or drive-up recorded and within the table.
- [ ] Grease type and grams per interval documented on the lube route.
- [ ] Run-in temperature stabilises (typical rise settles within an hour).
