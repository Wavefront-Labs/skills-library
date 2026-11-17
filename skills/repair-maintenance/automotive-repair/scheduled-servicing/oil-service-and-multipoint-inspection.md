---
id: repair-maintenance.automotive-repair.scheduled-servicing.oil-service-and-multipoint-inspection
name: oil-service-and-multipoint-inspection
category: repair-maintenance
field: automotive-repair
product: scheduled-servicing
tags: [automotive-repair, scheduled-servicing, oil-change, engine-oil, oil-specification, acea, api, ilsac, vw-504-00, dexos, viscosity, 0w-20, oil-filter, drain-plug-washer, service-interval, service-reset, multipoint-inspection, coolant, brake-fluid, air-filter, cabin-filter, spark-plugs, wiper-blades, severe-service, maintenance-schedule]
level: intro
status: draft
description: "Do a correct oil-and-filter service and multipoint inspection: oil spec (not just viscosity), drain plug and filter torque, fluid checks, filters, service-light reset and a clear report for the owner."
sources: ["ACEA European Oil Sequences and API/ILSAC service categories", "Manufacturer maintenance schedules and owner's manuals (structure only)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Oil service and multipoint inspection

**Goal:** perform the most common workshop job without the common mistakes (wrong oil
spec, double gasket, over-tightened plug, forgotten reset), and use the visit to catch
problems early with a consistent inspection.

## 1. Look up before you start
- **Oil specification** from the owner's manual/service info: viscosity (e.g. 0W-20,
  5W-30) **and** the approval/spec (e.g. API SP/ILSAC GF-6, ACEA C3, VW 504 00/507 00,
  MB 229.51, GM dexos1 Gen 3, Ford WSS-M2C…). Using the right viscosity with the wrong
  approval can damage diesel particulate filters, timing chains and warranty standing.
- Capacity with filter; filter part number; drain plug torque and whether the **crush
  washer** must be replaced (almost always yes).
- Service schedule: normal vs **severe service** (short trips, towing, dusty roads, taxi use)
  — many real-world cars qualify for severe.
- Variable/long-life service systems (flexible intervals) need the right oil to keep that interval.

## 2. Oil and filter change
1. Engine warm (oil flows and carries contaminants), on level ground or a lift; wheels chocked.
2. Remove the drain plug (correct-size socket; many sumps are aluminium or plastic and
   strip easily). Let it drain fully; inspect oil for metal glitter, milky emulsion (coolant),
   fuel smell.
3. **Filter:**
   - Spin-on: remove, make sure the **old gasket came off with it** (a double gasket
     blows out and empties the engine in minutes). Lightly oil the new gasket; hand-tighten
     ~ 3/4 turn after contact (or as printed on the filter).
   - Cartridge in housing: replace O-rings supplied, torque the cap to spec (often ~ 25 N·m)
     — over-torque cracks plastic housings.
4. New crush washer, drain plug torqued to spec (commonly ~ 25–40 N·m for steel pans, lower
   for aluminium — check). No "gorilla tight".
5. Fill with ~ 90 % of capacity, start and run 30 s (oil light out within a few seconds),
   stop, wait 2–5 min, check the dipstick (or the electronic level check on cars with no
   dipstick — follow its procedure), top up to between min and max. Check for leaks under
   the car.
6. Reset the **service indicator** (menu or scan tool) and record mileage, oil and filter
   used on the service record/sticker.

## 3. Multipoint inspection (record each as green/amber/red)
**Fluids:**
- Coolant level (cold) and protection with a refractometer (e.g. to −35 °C); correct coolant type.
- Brake fluid level and moisture test/age (see
  `repair-maintenance.automotive-repair.brake-systems.pad-rotor-replacement-and-brake-bleeding`).
- Power steering (if hydraulic), washer fluid, transmission fluid where a check is possible.
**Filters and ignition:** engine air filter, cabin/pollen filter (due by time or mileage), spark
plugs at schedule (petrol, often 60,000–100,000 km for iridium).
**Under the car:** oil, coolant, fuel and exhaust leaks; CV boots; suspension bushings and
links; brake hoses and lines (corrosion); exhaust mounts.
**Brakes:** pad thickness all four, rotor condition (through the wheel or wheels off per schedule).
**Tyres:** tread depth at three points across, pressures set to placard, uneven wear, age;
spare/inflator kit.
**Belts and hoses:** cracks, glazing, soft/swollen hoses; timing belt due date (mileage *and*
age).
**Electrics:** battery test, all lights, horn, wipers (blades smearing), warning lamps on start.
**Scan:** quick scan for stored codes even with no lamp on.

## 4. Report to the owner
Prioritised list: safety now (red), soon (amber), fine (green), with measurements
(e.g. "front pads 3 mm, rear 7 mm") and photos where useful. Don't upsell items not due.

## Gotchas
- Overfilling oil (above max) causes aeration and seal leaks — drain to correct level.
- Mixing coolant types (e.g. OAT with silicate types) can gel; use the specified type.
- Uncertain: torque values and intervals are typical; vehicle-specific data rules.

## Verify
- [ ] Oil matches the manufacturer approval, not just viscosity; correct capacity used.
- [ ] Old filter gasket removed; new crush washer; plug and filter torqued; no leaks.
- [ ] Oil level correct after run-and-settle; service indicator reset; record updated.
- [ ] Every inspection item recorded with measurements; owner given prioritised report.
