---
id: repair-maintenance.building-services-equipment-maintenance.hvac-plant-maintenance.ahu-and-chiller-preventive-maintenance
name: ahu-and-chiller-preventive-maintenance
category: repair-maintenance
field: building-services-equipment-maintenance
product: hvac-plant-maintenance
tags: [building-services-equipment-maintenance, hvac-plant-maintenance, hvac, ahu, air-handling-unit, rooftop-unit, rtu, chiller, vav, vav-box, filters, differential-pressure, belts, belt-tension, pulley-alignment, coils, coil-cleaning, condensate-drain, approach-temperature, superheat, subcooling, refrigerant, f-gas, epa-608, leak-check, condenser, evaporator, preventive-maintenance, ppm, sfg20]
level: practitioner
status: docs-checked
description: "Run AHU, RTU and chiller preventive maintenance: filter dP, belts and alignment, coils and drains, VAV checks, chiller approach temperatures, superheat/subcooling and leak-check logs."
sources: ["https://www.epa.gov/section608/section-608-technician-certification-requirements", "https://www.epa.gov/section608/epas-refrigerant-management-program-questions-and-answers-section-608-certified"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AHU and chiller preventive maintenance

**Goal:** keep air handlers and chillers efficient and reliable with a routine that
catches drift early. The numbers to watch are filter pressure drop, belt condition,
coil cleanliness, approach temperatures and refrigerant superheat/subcooling. Use the
OEM manual and your maintenance standard (e.g. SFG20 in the UK, ASHRAE/ACCA 180 in the US)
for frequencies; use the OEM values where they differ.

## Safety first
Isolate and lock out (LOTO) fans and compressors before opening panels; fans can be
started by the BMS. Refrigerant work needs certification (EPA 608 in the US, F-gas
certification in the UK/EU). Wear gloves and eye protection near coils and chemicals.

## 1. Air handling units and rooftop units (monthly/quarterly)
- **Filters:** read the differential pressure gauge (magnehelic or BMS point). Typical
  change at the maker's final dP, per the filter maker's final pressure drop (check filter data). Check seals: bypass round a filter frame wastes the
  filter. Record date and dP.
- **Belts:** check tension (to the belt maker's deflection value, or with a sonic tension meter), cracks, glazing. Check pulley alignment with a straight edge
  or laser. Replace matched sets on multi-belt drives.
- **Bearings and motor:** listen, feel for heat (or IR thermometer), grease to schedule
  with the correct grease and quantity — over-greasing kills bearings.
- **Coils:** inspect for dirt and fin damage; clean with low-pressure water/coil cleaner
  from the leaving-air side. Record coil air pressure drop if measured.
- **Condensate:** drain pan clean, trap primed and draining, no standing water (legionella
  and mould risk). Pan tablets per site policy.
- **Dampers and actuators:** stroke via BMS, watch linkage and blades move fully.
- **Frost/freeze stat** and fire/smoke damper interlocks tested per schedule.

## 2. VAV boxes (annual or on complaint)
Check the airflow sensor reading against min/max setpoints, damper actuator strokes,
reheat valve operates, and the space sensor reads correctly. A box stuck at max with a
cold room often has a failed actuator or a velocity sensor tube that's blocked or
reversed.

## 3. Chillers (daily log, quarterly, annual)
Log daily from the controller: chilled water in/out, condenser water in/out, evaporator
and condenser refrigerant saturation temperatures, % load, amps, oil pressure.
- **Approach temperatures:** evaporator approach = leaving chilled water − evaporator
  saturation temp; condenser approach = condenser saturation temp − leaving condenser
  water. Typical design approaches are a few K (compare to commissioning data). **Rising condenser approach = fouled tubes** → schedule tube
  brushing; rising evaporator approach = fouling or low charge.
- **Superheat and subcooling:** compared against OEM targets. High superheat + low
  subcooling → undercharge/leak; low superheat → overfeed/expansion valve problem.
- **Leak checks:** to legal schedule by charge size (F-gas / EPA rules), with a calibrated
  detector; record in the equipment log.
- **Annual:** oil analysis, condenser tube cleaning (water-cooled), eddy-current tube
  testing every few years, safety controls tested, electrical connections torqued/IR scanned.
- **Air-cooled:** condenser coils cleaned before summer; check fans and VSDs.

## Gotchas
- Filters replaced but dP unchanged → gauge tubes blocked or swapped.
- A chiller "lacking capacity" is often a water-side problem: flow low (strainer
  blocked), tower water hot, or tubes fouled — check before adding refrigerant.
- Never vent refrigerant; recover it and log quantities.

## Verify
- [ ] LOTO applied for every opened unit.
- [ ] Filter dP, belt condition, bearing temp recorded per unit.
- [ ] Drain pans clear and draining.
- [ ] Chiller log trended; approaches compared with last quarter and commissioning.
- [ ] Leak checks logged with date, detector and result.
- [ ] Work order closed with readings, not just "done".

## Checked

Date checked: 2026-10-25. Jurisdiction: United States (EPA Section 608) and United Kingdom/EU (F-gas) by name; the OEM manual governs.
EPA Section 608 pages: technicians must pass an EPA-approved certification test (types I, II, III and universal), and intentional venting of refrigerant is prohibited with a de minimis exception for good-faith recovery. F-gas certification and the SFG20 and ASHRAE/ACCA 180 maintenance standards are named only and were not read. Removed unconfirmed figures: filter change differential, belt deflection ratio, chiller approach range.

Method: documentation only; no commands were run.
